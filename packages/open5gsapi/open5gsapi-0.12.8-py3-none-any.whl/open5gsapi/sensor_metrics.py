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
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Use relative timestamps instead of absolute
        self.latencies = deque(maxlen=window_size)
        self.throughputs = deque(maxlen=window_size)
        self.jitters = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        
        # Track last latency for jitter calculation
        self.last_latency = None

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record sent data with timestamp"""
        with self.metrics_lock:
            try:
                size = len(json.dumps(data).encode('utf-8'))
                self.packet_sizes.append(size)
                
                if isinstance(data, dict) and 'sensor_id' in data:
                    # Add relative timestamp (milliseconds since start)
                    relative_time = (timestamp - self.start_time) * 1000
                    data['_send_time_ms'] = relative_time
                    logger.info(f"Recording sent data - sensor: {data['sensor_id']}, relative_time: {relative_time}ms")
                    
            except Exception as e:
                logger.error(f"Error recording sent data: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record received data and calculate metrics"""
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and 'sensor_id' in data and '_send_time_ms' in data:
                    size = len(json.dumps(data).encode('utf-8'))
                    
                    # Calculate relative receive time
                    receive_time_ms = (timestamp - self.start_time) * 1000
                    send_time_ms = data['_send_time_ms']
                    
                    # Calculate latency (should now be in reasonable range)
                    latency = receive_time_ms - send_time_ms
                    
                    # Sanity check - ignore clearly wrong values
                    if latency > 0 and latency < 1000:  # Typical latency should be < 1000ms
                        # Calculate throughput (bps)
                        throughput = (size * 8) / (latency / 1000)
                        
                        logger.info(f"Valid metrics - Latency: {latency:.2f}ms, Throughput: {throughput:.2f}bps")
                        
                        # Store metrics
                        self.latencies.append(latency)
                        self.throughputs.append(throughput)
                        
                        # Calculate jitter
                        if self.last_latency is not None:
                            jitter = abs(latency - self.last_latency)
                            self.jitters.append(jitter)
                        
                        self.last_latency = latency
                    else:
                        logger.warning(f"Ignoring suspicious latency value: {latency}ms")
                    
            except Exception as e:
                logger.error(f"Error recording received data: {e}")

    def calculate_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        with self.metrics_lock:
            try:
                # Only use last 10 values to get more current metrics
                recent_latencies = list(self.latencies)[-10:] if self.latencies else []
                recent_throughputs = list(self.throughputs)[-10:] if self.throughputs else []
                recent_jitters = list(self.jitters)[-10:] if self.jitters else []
                
                return {
                    "latency": {
                        "current_ms": recent_latencies[-1] if recent_latencies else 0,
                        "avg_ms": statistics.mean(recent_latencies) if recent_latencies else 0,
                        "min_ms": min(recent_latencies) if recent_latencies else 0,
                        "max_ms": max(recent_latencies) if recent_latencies else 0
                    },
                    "throughput": {
                        "current_bps": recent_throughputs[-1] if recent_throughputs else 0,
                        "avg_bps": statistics.mean(recent_throughputs) if recent_throughputs else 0,
                        "min_bps": min(recent_throughputs) if recent_throughputs else 0,
                        "max_bps": max(recent_throughputs) if recent_throughputs else 0
                    },
                    "jitter": {
                        "current_ms": recent_jitters[-1] if recent_jitters else 0,
                        "avg_ms": statistics.mean(recent_jitters) if recent_jitters else 0,
                        "min_ms": min(recent_jitters) if recent_jitters else 0,
                        "max_ms": max(recent_jitters) if recent_jitters else 0
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