import threading
import statistics
import logging
import json
from collections import deque
from time import monotonic
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Metrics storage
        self.latencies = deque(maxlen=window_size)
        self.throughputs = deque(maxlen=window_size)
        self.jitters = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        
        self.last_latency = None
        logger.info("SensorMetricsCalculator initialized")

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record when data is sent through open5gs.send_data"""
        with self.metrics_lock:
            try:
                # Calculate actual packet size from the data being sent
                if isinstance(data, dict):
                    size = len(json.dumps(data).encode('utf-8'))
                elif isinstance(data, bytes):
                    size = len(data)
                else:
                    size = len(str(data).encode('utf-8'))
                    
                self.packet_sizes.append(size)
                logger.debug(f"Recorded packet size: {size} bytes")

                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    self.send_timestamps[sensor_id] = {
                        'timestamp': timestamp,
                        'size': size  # Store size with timestamp
                    }
                
            except Exception as e:
                logger.error(f"Error in record_data_sent: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record when data is received and calculate metrics"""
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    
                    if sensor_id in self.send_timestamps:
                        send_info = self.send_timestamps[sensor_id]
                        send_time = send_info['timestamp']
                        packet_size = send_info['size']  # Get stored packet size
                        
                        # Calculate latency in milliseconds
                        latency = (timestamp - send_time) * 1000  # ms
                        
                        # Calculate throughput as packet_size_bits/latency_seconds
                        if latency > 0:
                            throughput = (packet_size * 8) / (latency / 1000)  # bits per second
                        else:
                            throughput = 0
                        
                        # Store metrics
                        self.latencies.append(latency)
                        self.throughputs.append(throughput)
                        
                        # Calculate jitter
                        if len(self.latencies) >= 2:
                            jitter = abs(latency - self.latencies[-2])
                            self.jitters.append(jitter)
                        
                        logger.debug(f"""Metrics for packet:
                            Size: {packet_size} bytes
                            Latency: {latency:.2f} ms
                            Throughput: {throughput:.2f} bps
                        """)
                        
                        del self.send_timestamps[sensor_id]
                        
            except Exception as e:
                logger.error(f"Error in record_data_received: {e}")

    def calculate_metrics(self) -> Dict[str, Any]:
        """Return the calculated metrics"""
        with self.metrics_lock:
            try:
                # Get current packet size metrics
                current_size = self.packet_sizes[-1] if self.packet_sizes else 0
                
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
                        "current_bytes": current_size,
                        "avg_bytes": statistics.mean(self.packet_sizes) if self.packet_sizes else 0,
                        "min_bytes": min(self.packet_sizes) if self.packet_sizes else 0,
                        "max_bytes": max(self.packet_sizes) if self.packet_sizes else 0
                    }
                }
                
            except Exception as e:
                logger.error(f"Error calculating metrics: {e}")
                raise

    def reset(self):
        with self.metrics_lock:
            self.latencies.clear()
            self.throughputs.clear()
            self.jitters.clear()
            self.packet_sizes.clear()
            self.last_latency = None
            self.start_time = monotonic()