import threading
import statistics
import logging
import json
from collections import deque
from time import monotonic
from typing import Dict, Any, Optional, List, Union, Tuple

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Basic packet tracking
        self.packets = []  # List of (timestamp, size, direction, sensor_id) tuples
        self.send_timestamps = {}  # Dictionary to track send times by sensor_id
        self.latencies = deque(maxlen=window_size)  # Store calculated latencies
        self.jitter_buffer = deque(maxlen=window_size)  # For jitter calculation
        
        # Counters
        self.total_bytes = 0
        self.total_packets = 0
        self.total_readings = 0
        self.readings_lost = 0
        
        # Sensor-specific tracking
        self.readings_by_sensor = {}  # Track metrics per sensor
        self.last_packet_time = None
        self.sensor_intervals = deque(maxlen=30)  # For calculating reading rate
        
        logger.info("SensorMetricsCalculator initialized")

    def _calculate_packet_size(self, data: Any) -> int:
        """Calculate the size of data in bytes"""
        try:
            if isinstance(data, (dict, list)):
                return len(json.dumps(data).encode('utf-8'))
            elif isinstance(data, bytes):
                return len(data)
            else:
                return len(str(data).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error calculating packet size: {e}")
            return 0

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record when data is sent"""
        with self.metrics_lock:
            size = self._calculate_packet_size(data)
            self.total_bytes += size
            self.total_packets += 1
            
            if isinstance(data, dict) and 'sensor_id' in data:
                sensor_id = data['sensor_id']
                packet_id = data.get('_packet_id')
                
                # Store send timestamp with packet_id for matching with receive
                if packet_id:
                    self.send_timestamps[packet_id] = {
                        'timestamp': timestamp,
                        'sensor_id': sensor_id,
                        'size': size
                    }

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record when data is received"""
        with self.metrics_lock:
            size = self._calculate_packet_size(data)
            self.total_bytes += size
            self.total_packets += 1
            
            if isinstance(data, dict) and 'sensor_id' in data:
                packet_id = data.get('_packet_id')
                if packet_id and packet_id in self.send_timestamps:
                    send_info = self.send_timestamps[packet_id]
                    latency = timestamp - send_info['timestamp']
                    
                    if latency > 0:
                        self.latencies.append(latency)
                        
                        # Calculate jitter
                        if len(self.latencies) >= 2:
                            prev_latency = self.latencies[-2]
                            jitter = abs(latency - prev_latency)
                            self.jitter_buffer.append(jitter)
                        
                    # Clean up send timestamp
                    del self.send_timestamps[packet_id]

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = max(current_time - self.start_time, 0.001)
            
            # Calculate latency statistics
            latencies_ms = [l * 1000 for l in self.latencies]  # Convert to ms
            
            # Calculate throughput
            throughput = (self.total_bytes * 8) / (elapsed * 1_000_000)  # Mbps
            
            return {
                "throughput": {
                    "total_mbps": throughput,
                    "bytes_per_second": self.total_bytes / elapsed,
                    "total_bytes": self.total_bytes,
                    "total_packets": self.total_packets
                },
                "latency": {
                    "min_ms": min(latencies_ms) if latencies_ms else 0,
                    "max_ms": max(latencies_ms) if latencies_ms else 0,
                    "avg_ms": statistics.mean(latencies_ms) if latencies_ms else 0,
                    "jitter_ms": statistics.mean(self.jitter_buffer) * 1000 if self.jitter_buffer else 0
                },
                "sensor_metrics": {
                    "reading_rate": {
                        "total_readings": self.total_packets,
                        "readings_per_second": self.total_packets / elapsed
                    }
                }
            }

    def _calculate_jitter(self) -> float:
        """Calculate jitter based on collected jitter samples"""
        if not self.jitter_buffer:
            return 0.0
        return statistics.mean(self.jitter_buffer) * 1000  # Convert to ms


    def _get_sensor_metrics(self) -> Dict[str, Any]:
        """Get detailed metrics for each sensor"""
        sensor_metrics = {}
        for sensor_id, data in self.readings_by_sensor.items():
            sensor_metrics[sensor_id] = {
                "total_readings": data["total_readings"],
                "readings_lost": data["readings_lost"],
                "average_size": statistics.mean(data["sizes"]) if data["sizes"] else 0,
                "loss_percentage": (data["readings_lost"] / max(data["total_readings"], 1)) * 100
            }
        return sensor_metrics

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.packets.clear()
            self.send_timestamps.clear()
            self.latencies.clear()
            self.jitter_buffer.clear()
            self.total_bytes = 0
            self.total_packets = 0
            self.total_readings = 0
            self.readings_lost = 0
            self.readings_by_sensor.clear()
            self.last_packet_time = None
            self.sensor_intervals.clear()
            logger.info("Metrics reset complete")