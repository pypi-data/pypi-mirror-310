import threading
import statistics
import logging
import re
import psutil
import socket
import subprocess
from collections import deque
from time import monotonic, sleep
from typing import Dict, Any, Optional, Deque, Union
import json

logger = logging.getLogger(__name__)

# class SensorMetricsCalculator:
#     def __init__(self, window_size: int = 100):
#         self.window_size = window_size
#         self.metrics_lock = threading.Lock()
#         self.start_time = monotonic()
        
#         # Packet metrics with timestamps
#         self.packet_timestamps = deque(maxlen=window_size)
#         self.packet_sizes = deque(maxlen=window_size)
#         self.total_packets = 0
#         self.total_bytes = 0
        
#         # Sensor specific metrics
#         self.sensor_readings = deque(maxlen=window_size)
#         self.sensor_intervals = deque(maxlen=30)
#         self.total_readings = 0
#         self.readings_lost = 0
#         self.last_reading_time = None
#         self.last_sequence_number = -1
#         self.readings_by_sensor = {}  # Track readings per sensor ID
#         self.sensor_timestamps = deque(maxlen=30)
        
#         # Interface monitoring
#         self._interfaces = {}
#         self._prev_stats = {}
#         self._last_update = monotonic()
#         self._update_interfaces()
        
#         # Start monitoring thread
#         self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
#         self._monitor_thread.start()

#     def _update_interfaces(self):
#         try:
#             interfaces = {}
#             for iface in psutil.net_if_stats().keys():
#                 if iface.startswith('uesimtun') or iface == 'ogstun':
#                     addr = self._get_interface_address(iface)
#                     if addr:
#                         interfaces[iface] = {
#                             'address': addr,
#                             'stats': psutil.net_io_counters(pernic=True).get(iface)
#                         }
#             self._interfaces = interfaces
#         except Exception as e:
#             logger.error(f"Error updating interfaces: {e}")

#     def _get_interface_address(self, iface: str) -> Optional[str]:
#         try:
#             addrs = psutil.net_if_addrs().get(iface, [])
#             for addr in addrs:
#                 if addr.family == socket.AF_INET:
#                     return addr.address
#         except Exception as e:
#             logger.error(f"Error getting interface address: {e}")
#         return None

#     def _calculate_jitter(self, timestamps: deque) -> float:
#         if len(timestamps) < 2:
#             return 0.0
#         jitter = 0.0
#         prev_timestamp = timestamps[0]
#         for timestamp in list(timestamps)[1:]:
#             delay = abs(timestamp - prev_timestamp)
#             jitter = jitter + (delay - jitter) / 16
#             prev_timestamp = timestamp
#         return jitter * 1000

#     def record_data_sent(self, data: Any, timestamp: float) -> None:
#         with self.metrics_lock:
#             size = len(str(data)) if isinstance(data, (dict, list)) else len(data)
#             self.total_bytes += size
#             self.total_packets += 1
#             self.packet_sizes.append(size)
#             self.packet_timestamps.append(timestamp)
            
#             if isinstance(data, dict) and "sensor_id" in data:
#                 self.total_readings += 1
#                 sensor_id = data["sensor_id"]
                
#                 if sensor_id not in self.readings_by_sensor:
#                     self.readings_by_sensor[sensor_id] = {
#                         "total_readings": 0,
#                         "last_sequence": -1,
#                         "readings_lost": 0,
#                         "values": deque(maxlen=30)
#                     }
                
#                 self.readings_by_sensor[sensor_id]["total_readings"] += 1
#                 self.readings_by_sensor[sensor_id]["values"].append({
#                     "timestamp": timestamp,
#                     "value": data
#                 })
                
#                 if self.last_reading_time is not None:
#                     interval = timestamp - self.last_reading_time
#                     if interval > 0:
#                         self.sensor_intervals.append(interval)
                
#                 self.last_reading_time = timestamp
#                 self.sensor_timestamps.append(timestamp)

#     def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
#         with self.metrics_lock:
#             size = len(str(data)) if isinstance(data, (dict, list)) else len(data)
#             self.total_bytes += size
#             self.total_packets += 1
#             self.packet_sizes.append(size)
#             self.packet_timestamps.append(timestamp)
            
#             if isinstance(data, dict) and "sensor_id" in data and "sequence" in data:
#                 try:
#                     sensor_id = data["sensor_id"]
#                     current_sequence = data["sequence"]
                    
#                     if sensor_id not in self.readings_by_sensor:
#                         self.readings_by_sensor[sensor_id] = {
#                             "total_readings": 0,
#                             "last_sequence": -1,
#                             "readings_lost": 0,
#                             "values": deque(maxlen=30)
#                         }
                    
#                     sensor_info = self.readings_by_sensor[sensor_id]
#                     if sensor_info["last_sequence"] >= 0:
#                         expected_sequence = sensor_info["last_sequence"] + 1
#                         if current_sequence > expected_sequence:
#                             readings_lost = current_sequence - expected_sequence
#                             sensor_info["readings_lost"] += readings_lost
#                             self.readings_lost += readings_lost
                    
#                     sensor_info["last_sequence"] = current_sequence
#                     sensor_info["total_readings"] += 1
#                     sensor_info["values"].append({
#                         "timestamp": timestamp,
#                         "value": data
#                     })
                    
#                     self.total_readings += 1
#                     self.sensor_readings.append(data)
#                     self.sensor_timestamps.append(timestamp)
                    
#                     if self.last_reading_time is not None:
#                         interval = timestamp - self.last_reading_time
#                         if interval > 0:
#                             self.sensor_intervals.append(interval)
                    
#                     self.last_reading_time = timestamp
                    
#                 except Exception as e:
#                     logger.error(f"Error processing sensor reading: {e}")

#     def calculate_metrics(self) -> Dict[str, Any]:
#         with self.metrics_lock:
#             current_time = monotonic()
#             elapsed = current_time - self.start_time
            
#             metrics = {
#                 "throughput": {
#                     "total_mbps": (self.total_bytes * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
#                 },
#                 "latency": {
#                     "min_ms": 0,
#                     "max_ms": 0,
#                     "avg_ms": 0,
#                     "jitter_ms": self._calculate_jitter(self.packet_timestamps)
#                 }
#             }
            
#             # Interface latency measurement
#             self._update_interfaces()
#             for iface, data in self._interfaces.items():
#                 if iface.startswith('uesimtun'):
#                     latency = self._measure_interface_latency(iface)
#                     if latency > 0:
#                         metrics['latency'].update({
#                             "min_ms": min(metrics['latency']['min_ms'], latency) if metrics['latency']['min_ms'] > 0 else latency,
#                             "max_ms": max(metrics['latency']['max_ms'], latency),
#                             "avg_ms": latency if metrics['latency']['avg_ms'] == 0 else (metrics['latency']['avg_ms'] + latency) / 2
#                         })
            
#             # Calculate readings per second
#             readings_per_second = 0
#             if self.sensor_intervals:
#                 avg_interval = statistics.mean(self.sensor_intervals)
#                 if avg_interval > 0:
#                     readings_per_second = 1 / avg_interval
            
#             # Sensor metrics
#             metrics["sensor_metrics"] = {
#                 "reading_rate": {
#                     "current_rps": readings_per_second,
#                     "reading_interval_ms": statistics.mean(self.sensor_intervals) * 1000 if self.sensor_intervals else 0,
#                     "total_readings": self.total_readings,
#                     "readings_lost": self.readings_lost
#                 },
#                 "by_sensor": {}
#             }
            
#             # Per-sensor metrics
#             for sensor_id, sensor_data in self.readings_by_sensor.items():
#                 latest_readings = list(sensor_data["values"])
#                 if latest_readings:
#                     latest_values = [r["value"] for r in latest_readings]
#                     metrics["sensor_metrics"]["by_sensor"][sensor_id] = {
#                         "total_readings": sensor_data["total_readings"],
#                         "readings_lost": sensor_data["readings_lost"],
#                         "latest_value": latest_values[-1],
#                         "min_value": min(latest_values, key=lambda x: x.get("value", 0)),
#                         "max_value": max(latest_values, key=lambda x: x.get("value", 0)),
#                         "avg_value": statistics.mean([x.get("value", 0) for x in latest_values])
#                     }
            
#             return metrics

#     def _measure_interface_latency(self, interface: str) -> float:
#         try:
#             result = subprocess.run(
#                 ['ping', '-I', interface, '-c', '1', '-W', '1', '10.45.0.1'],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )
#             if result.returncode == 0:
#                 match = re.search(r'time=([\d.]+)', result.stdout)
#                 if match:
#                     return float(match.group(1))
#             return 0
#         except Exception as e:
#             logger.error(f"Error measuring latency for interface {interface}: {e}")
#             return 0

#     def _monitor_network(self):
#         while True:
#             try:
#                 self._update_interfaces()
#                 sleep(1)
#             except Exception as e:
#                 logger.error(f"Error in network monitor: {e}")
#                 sleep(5)

#     def reset(self):
#         with self.metrics_lock:
#             self.start_time = monotonic()
#             self.packet_timestamps.clear()
#             self.packet_sizes.clear()
#             self.total_packets = 0
#             self.total_bytes = 0
#             self.sensor_readings.clear()
#             self.sensor_intervals.clear()
#             self.sensor_timestamps.clear()
#             self.total_readings = 0
#             self.readings_lost = 0
#             self.last_reading_time = None
#             self.last_sequence_number = -1
#             self.readings_by_sensor.clear()
#             self._prev_stats = {}

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Packet timings
        self.send_times = {}  # {sensor_id_sequence: timestamp}
        self.latencies = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        
        # Reading tracking
        self.total_readings = 0
        self.readings_lost = 0
        self.readings_by_sensor = {}
        self.reading_intervals = deque(maxlen=window_size)
        self.last_reading_time = None
        
        logging.getLogger('SensorMetricsCalculator').setLevel(logging.DEBUG)
        self.logger = logging.getLogger('SensorMetricsCalculator')

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and "sensor_id" in data:
                    sensor_id = data["sensor_id"]
                    sequence = data.get("sequence", 0)
                    packet_key = f"{sensor_id}_{sequence}"
                    
                    # Store send time
                    self.send_times[packet_key] = timestamp
                    
                    # Calculate packet size
                    packet_size = len(json.dumps(data).encode())
                    self.packet_sizes.append(packet_size)
                    
                    # Update reading count
                    self.total_readings += 1
                    
                    # Initialize sensor if needed
                    if sensor_id not in self.readings_by_sensor:
                        self.readings_by_sensor[sensor_id] = {
                            "total_readings": 0,
                            "readings_lost": 0,
                            "values": deque(maxlen=30)
                        }
                    self.readings_by_sensor[sensor_id]["total_readings"] += 1
                    
                    # Update intervals
                    if self.last_reading_time is not None:
                        interval = timestamp - self.last_reading_time
                        self.reading_intervals.append(interval)
                    self.last_reading_time = timestamp
                    
                    self.logger.debug(f"Recorded sent data - Sensor: {sensor_id}, Sequence: {sequence}, "
                                    f"Size: {packet_size}, Timestamp: {timestamp}")
            except Exception as e:
                self.logger.error(f"Error in record_data_sent: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            try:
                if isinstance(data, dict) and "sensor_id" in data:
                    sensor_id = data["sensor_id"]
                    sequence = data.get("sequence", 0)
                    packet_key = f"{sensor_id}_{sequence}"
                    
                    # Calculate latency if we have the send time
                    send_time = self.send_times.pop(packet_key, None)
                    if send_time is not None:
                        latency = (timestamp - send_time) * 1000  # Convert to ms
                        self.latencies.append(latency)
                        self.logger.debug(f"Calculated latency for {packet_key}: {latency}ms")
                    
                    # Store received value
                    if sensor_id in self.readings_by_sensor:
                        self.readings_by_sensor[sensor_id]["values"].append({
                            "timestamp": timestamp,
                            "value": data
                        })
                        self.logger.debug(f"Stored received value for sensor {sensor_id}")
            except Exception as e:
                self.logger.error(f"Error in record_data_received: {e}")

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            try:
                # Calculate basic rates
                elapsed = monotonic() - self.start_time
                
                # Calculate throughput
                total_bytes = sum(self.packet_sizes) if self.packet_sizes else 0
                total_mbps = (total_bytes * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
                
                # Calculate reading rate
                current_rps = 0
                if self.reading_intervals:
                    avg_interval = statistics.mean(self.reading_intervals)
                    if avg_interval > 0:
                        current_rps = 1 / avg_interval
                
                # Calculate latency stats
                latency_stats = {
                    "min_ms": min(self.latencies) if self.latencies else 0,
                    "max_ms": max(self.latencies) if self.latencies else 0,
                    "avg_ms": statistics.mean(self.latencies) if self.latencies else 0,
                    "jitter_ms": self._calculate_jitter(self.latencies)
                }
                
                metrics = {
                    "throughput": {
                        "total_mbps": total_mbps
                    },
                    "latency": latency_stats,
                    "sensor_metrics": {
                        "reading_rate": {
                            "current_rps": current_rps,
                            "reading_interval_ms": statistics.mean(self.reading_intervals) * 1000 if self.reading_intervals else 0,
                            "total_readings": self.total_readings,
                            "readings_lost": self.readings_lost
                        },
                        "by_sensor": {}
                    }
                }
                
                # Add per-sensor metrics
                for sensor_id, sensor_data in self.readings_by_sensor.items():
                    if sensor_data["values"]:
                        values = list(sensor_data["values"])
                        metrics["sensor_metrics"]["by_sensor"][sensor_id] = {
                            "total_readings": sensor_data["total_readings"],
                            "readings_lost": sensor_data["readings_lost"],
                            "latest_value": values[-1]["value"],
                            "min_value": min(values, key=lambda x: sum(v for v in x["value"].values() 
                                          if isinstance(v, (int, float))))["value"],
                            "max_value": max(values, key=lambda x: sum(v for v in x["value"].values() 
                                          if isinstance(v, (int, float))))["value"]
                        }
                
                self.logger.debug(f"Calculated metrics: {json.dumps(metrics, indent=2)}")
                return metrics
                
            except Exception as e:
                self.logger.error(f"Error calculating metrics: {e}")
                return {
                    "throughput": {"total_mbps": 0},
                    "latency": {"min_ms": 0, "max_ms": 0, "avg_ms": 0, "jitter_ms": 0},
                    "sensor_metrics": {
                        "reading_rate": {"current_rps": 0, "reading_interval_ms": 0, 
                                       "total_readings": 0, "readings_lost": 0},
                        "by_sensor": {}
                    }
                }

    def _calculate_jitter(self, values: deque) -> float:
        if len(values) < 2:
            return 0.0
        differences = [abs(values[i] - values[i-1]) for i in range(1, len(values))]
        return statistics.mean(differences) if differences else 0.0

    def reset(self):
        with self.metrics_lock:
            self.start_time = monotonic()
            self.send_times.clear()
            self.latencies.clear()
            self.packet_sizes.clear()
            self.total_readings = 0
            self.readings_lost = 0
            self.readings_by_sensor.clear()
            self.reading_intervals.clear()
            self.last_reading_time = None