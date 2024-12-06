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
        with self.metrics_lock:
            try:
                # Calculate packet size
                size = len(json.dumps(data).encode('utf-8'))
                self.packet_sizes.append(size)
                
                # Add send timestamp to data
                if isinstance(data, dict) and 'sensor_id' in data:
                    data['_send_timestamp'] = timestamp
                    logger.debug(f"Recorded send timestamp {timestamp} for sensor {data['sensor_id']}")
                
            except Exception as e:
                logger.error(f"Error in record_data_sent: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and 'sensor_id' in data and '_send_timestamp' in data:
                    send_time = float(data['_send_timestamp'])
                    size = len(json.dumps(data).encode('utf-8'))
                    
                    # Calculate metrics
                    latency = (timestamp - send_time) * 1000  # Convert to ms
                    if latency > 0:
                        throughput = (size * 8) / (latency / 1000)  # bits per second
                        
                        # Store metrics
                        self.latencies.append(latency)
                        self.throughputs.append(throughput)
                        
                        # Calculate jitter
                        if self.last_latency is not None:
                            jitter = abs(latency - self.last_latency)
                            self.jitters.append(jitter)
                        
                        self.last_latency = latency
                        
                        logger.debug(f"""Metrics recorded:
                            Sensor: {data['sensor_id']}
                            Latency: {latency:.2f} ms
                            Throughput: {throughput:.2f} bps
                            Size: {size} bytes""")
                    
            except Exception as e:
                logger.error(f"Error in record_data_received: {e}")

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            try:
                logger.debug(f"""Current metrics state:
                    Latencies: {list(self.latencies)}
                    Throughputs: {list(self.throughputs)}
                    Jitters: {list(self.jitters)}""")
                
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
                
            except Exception as e:
                logger.error(f"Error calculating metrics: {e}")
                return {
                    "latency": {"current_ms": 0, "avg_ms": 0, "min_ms": 0, "max_ms": 0},
                    "throughput": {"current_bps": 0, "avg_bps": 0, "min_bps": 0, "max_bps": 0},
                    "jitter": {"current_ms": 0, "avg_ms": 0, "min_ms": 0, "max_ms": 0},
                    "packet_size": {"current_bytes": 0, "avg_bytes": 0, "min_bytes": 0, "max_bytes": 0}
                }

    def reset(self):
        with self.metrics_lock:
            self.latencies.clear()
            self.throughputs.clear()
            self.jitters.clear()
            self.packet_sizes.clear()
            self.last_latency = None
            self.start_time = monotonic()