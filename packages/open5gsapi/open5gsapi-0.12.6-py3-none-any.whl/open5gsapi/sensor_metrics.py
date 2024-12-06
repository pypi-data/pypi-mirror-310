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
        """Record when data is sent"""
        with self.metrics_lock:
            try:
                # Calculate size
                size = len(str(data).encode('utf-8'))
                
                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    self.send_timestamps[sensor_id] = {
                        'timestamp': timestamp,
                        'size': size
                    }
                    logger.info(f"SEND: Recorded sensor {sensor_id} at time {timestamp} with size {size}")
                    self.packet_sizes.append(size)
                    
            except Exception as e:
                logger.error(f"Error in record_data_sent: {e}")
                raise

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record when data is received"""
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    logger.info(f"RECEIVE: Got data for sensor {sensor_id} at time {timestamp}")
                    
                    if sensor_id in self.send_timestamps:
                        send_info = self.send_timestamps[sensor_id]
                        send_time = send_info['timestamp']
                        size = send_info['size']
                        
                        # Calculate metrics
                        latency = (timestamp - send_time) * 1000  # ms
                        throughput = (size * 8) / (latency/1000) if latency > 0 else 0  # bps
                        
                        logger.info(f"""
                        Calculating metrics for {sensor_id}:
                        Send time: {send_time}
                        Receive time: {timestamp}
                        Latency: {latency} ms
                        Size: {size} bytes
                        Throughput: {throughput} bps
                        """)
                        
                        # Store metrics
                        self.latencies.append(latency)
                        self.throughputs.append(throughput)
                        
                        if len(self.latencies) >= 2:
                            jitter = abs(latency - self.latencies[-2])
                            self.jitters.append(jitter)
                            logger.info(f"Calculated jitter: {jitter} ms")
                        
                        # Clean up
                        del self.send_timestamps[sensor_id]
                    else:
                        logger.warning(f"No send timestamp found for sensor {sensor_id}")
                        
            except Exception as e:
                logger.error(f"Error in record_data_received: {e}")
                raise

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate metrics from stored values"""
        with self.metrics_lock:
            try:
                # Log current state
                logger.info(f"""
                Current state:
                Latencies: {list(self.latencies)}
                Throughputs: {list(self.throughputs)}
                Jitters: {list(self.jitters)}
                Packet sizes: {list(self.packet_sizes)}
                """)
                
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
                
                logger.info(f"Calculated metrics: {metrics}")
                return metrics
                
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