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
        """Record when data is sent"""
        with self.metrics_lock:
            try:
                # Calculate size for JSON data properly
                if isinstance(data, (dict, list)):
                    size = len(json.dumps(data).encode('utf-8'))
                else:
                    size = len(str(data).encode('utf-8'))
                
                # Store packet size
                self.packet_sizes.append(size)
                
                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    self.send_timestamps[sensor_id] = {
                        'timestamp': timestamp,
                        'size': size  # Store size with timestamp
                    }
                    logger.debug(f"Recorded send: sensor_id={sensor_id}, time={timestamp}, size={size}")

            except Exception as e:
                logger.error(f"Error in record_data_sent: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record when data is received"""
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and 'sensor_id' in data:
                    sensor_id = data['sensor_id']
                    
                    if sensor_id in self.send_timestamps:
                        send_info = self.send_timestamps[sensor_id]
                        send_time = send_info['timestamp']
                        packet_size = send_info['size']
                        
                        # Calculate latency (ms)
                        latency = (timestamp - send_time) * 1000
                        
                        if latency > 0:
                            # Calculate throughput: packet_size_bits / latency_seconds
                            throughput = (packet_size * 8) / (latency / 1000)  # bits per second
                            
                            # Store metrics
                            self.latencies.append(latency)
                            self.throughputs.append(throughput)
                            
                            # Calculate jitter if we have previous latency
                            if self.last_latency is not None:
                                jitter = abs(latency - self.last_latency)
                                self.jitters.append(jitter)
                            
                            self.last_latency = latency
                            
                            logger.debug(f"""
                                Calculated metrics:
                                Packet Size: {packet_size} bytes
                                Latency: {latency:.2f} ms
                                Throughput: {throughput:.2f} bps
                                """)
                        
                        del self.send_timestamps[sensor_id]
                        
            except Exception as e:
                logger.error(f"Error in record_data_received: {e}")

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
        with self.metrics_lock:
            self.latencies.clear()
            self.throughputs.clear()
            self.jitters.clear()
            self.packet_sizes.clear()
            self.last_latency = None
            self.start_time = monotonic()