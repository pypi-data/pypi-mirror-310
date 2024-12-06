import json
import threading
import statistics
import logging
from collections import deque
from time import monotonic
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.metrics_lock = threading.Lock()
        
        # Store timestamps and sizes for calculating metrics
        self.send_timestamps = {}  # {sensor_id: (timestamp, size)}
        self.latencies = deque(maxlen=window_size)  # Store latency values
        self.throughputs = deque(maxlen=window_size)  # Store throughput values
        self.jitters = deque(maxlen=window_size)  # Store jitter values
        self.packet_sizes = deque(maxlen=window_size)  # Store packet sizes

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record sent data with timestamp"""
        with self.metrics_lock:
            try:
                size = len(json.dumps(data).encode('utf-8'))
                self.packet_sizes.append(size)
                
                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    logger.info(f"Recording sent data - sensor: {sensor_id}, time: {timestamp}, size: {size}")
                    self.send_timestamps[sensor_id] = (timestamp, size)
                    
            except Exception as e:
                logger.error(f"Error recording sent data: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record received data and calculate metrics"""
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and 'sensor_id' in data and '_send_timestamp' in data:
                    send_timestamp = data['_send_timestamp']
                    size = len(json.dumps(data).encode('utf-8'))
                    
                    # Calculate latency in milliseconds
                    latency = (timestamp - send_timestamp) * 1000
                    
                    # Calculate throughput (bits per second)
                    throughput = (size * 8) / (latency/1000) if latency > 0 else 0
                    
                    logger.info(f"Calculating metrics - Latency: {latency}ms, Throughput: {throughput}bps")
                    
                    # Store metrics
                    self.latencies.append(latency)
                    self.throughputs.append(throughput)
                    self.packet_sizes.append(size)
                    
                    # Calculate jitter
                    if len(self.latencies) >= 2:
                        jitter = abs(latency - self.latencies[-2])
                        self.jitters.append(jitter)
                        
            except Exception as e:
                logger.error(f"Error recording received data: {e}")

    def calculate_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        with self.metrics_lock:
            try:
                return {
                    "latency": {
                        "current_ms": self.latencies[-1] if self.latencies else 0,
                        "avg_ms": statistics.mean(self.latencies) if self.latencies else 0,
                        "min_ms": min(self.latencies) if self.latencies else 0,
                        "max_ms": max(self.latencies) if self.latencies else 0
                    },
                    "throughput": {
                        "current_bps": self.throughputs[-1] if self.throughputs else 0,
                        "avg_bps": statistics.mean(self.throughputs) if self.throughputs else 0,
                        "min_bps": min(self.throughputs) if self.throughputs else 0,
                        "max_bps": max(self.throughputs) if self.throughputs else 0
                    },
                    "jitter": {
                        "current_ms": self.jitters[-1] if self.jitters else 0,
                        "avg_ms": statistics.mean(self.jitters) if self.jitters else 0,
                        "min_ms": min(self.jitters) if self.jitters else 0,
                        "max_ms": max(self.jitters) if self.jitters else 0
                    },
                    "packet_size": {
                        "current_bytes": self.packet_sizes[-1] if self.packet_sizes else 0,
                        "avg_bytes": statistics.mean(self.packet_sizes) if self.packet_sizes else 0,
                        "min_bytes": min(self.packet_sizes) if self.packet_sizes else 0,
                        "max_bytes": max(self.packet_sizes) if self.packet_sizes else 0
                    }
                }
            except Exception as e:
                logger.error(f"Error calculating metrics: {e}")
                raise

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.send_timestamps.clear()
            self.latencies.clear()
            self.throughputs.clear()
            self.jitters.clear()
            self.packet_sizes.clear()