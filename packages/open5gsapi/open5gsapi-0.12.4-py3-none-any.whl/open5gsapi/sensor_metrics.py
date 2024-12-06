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
        """Record timestamp when data is sent"""
        with self.metrics_lock:
            if isinstance(data, (dict, list)):
                size = len(str(data).encode('utf-8'))
            else:
                size = len(str(data))
                
            if isinstance(data, dict) and 'sensor_id' in data:
                sensor_id = data['sensor_id']
                self.send_timestamps[sensor_id] = (timestamp, size)
                logger.debug(f"Recorded send timestamp for sensor {sensor_id}: {timestamp}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record timestamp when data is received and calculate metrics"""
        with self.metrics_lock:
            if isinstance(data, dict) and 'sensor_id' in data:
                sensor_id = data['sensor_id']
                
                if sensor_id in self.send_timestamps:
                    send_time, packet_size = self.send_timestamps[sensor_id]
                    
                    # Calculate latency (ms)
                    latency = (timestamp - send_time) * 1000  # Convert to milliseconds
                    
                    # Calculate throughput (bits per second)
                    throughput = (packet_size * 8) / (latency / 1000) if latency > 0 else 0
                    
                    # Store metrics
                    self.latencies.append(latency)
                    self.throughputs.append(throughput)
                    self.packet_sizes.append(packet_size)
                    
                    # Calculate jitter only if we have at least 2 latencies
                    if len(self.latencies) >= 2:
                        jitter = abs(self.latencies[-1] - self.latencies[-2])
                        self.jitters.append(jitter)
                    
                    # Clean up send timestamp
                    del self.send_timestamps[sensor_id]
                    
                    logger.debug(f"Metrics calculated for sensor {sensor_id}:")
                    logger.debug(f"Latency: {latency}ms")
                    logger.debug(f"Throughput: {throughput} bps")
                    logger.debug(f"Packet size: {packet_size} bytes")

    def calculate_metrics(self) -> Dict[str, Any]:
        """Return the calculated metrics"""
        with self.metrics_lock:
            metrics = {
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
            
            logger.debug(f"Calculated metrics: {metrics}")
            return metrics

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.send_timestamps.clear()
            self.latencies.clear()
            self.throughputs.clear()
            self.jitters.clear()
            self.packet_sizes.clear()