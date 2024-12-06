# import threading
# import statistics
# import logging
# import re
# import psutil
# import socket
# import subprocess
# from collections import deque
# from time import monotonic, sleep
# from typing import Dict, Any, Optional, Deque, Union
# import json

# logger = logging.getLogger(__name__)

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

#     # def _calculate_jitter(self, timestamps: deque) -> float:
#     #     if len(timestamps) < 2:
#     #         return 0.0
#     #     jitter = 0.0
#     #     prev_timestamp = timestamps[0]
#     #     for timestamp in list(timestamps)[1:]:
#     #         delay = abs(timestamp - prev_timestamp)
#     #         jitter = jitter + (delay - jitter) / 16
#     #         prev_timestamp = timestamp
#     #     return jitter * 1000

#     def _calculate_jitter(self, timestamps: deque) -> float:
#         """Calculate jitter using RFC 3550 algorithm"""
#         if len(timestamps) < 2:
#             return 0.0
            
#         delays = []
#         timestamps_list = sorted(list(timestamps))
#         for i in range(1, len(timestamps_list)):
#             delay = timestamps_list[i] - timestamps_list[i-1]
#             delays.append(delay)
        
#         if not delays:
#             return 0.0
            
#         avg_delay = sum(delays) / len(delays)
#         jitter = sum(abs(d - avg_delay) for d in delays) / len(delays)
#         return jitter * 1000  # Convert to ms

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

#     # def calculate_metrics(self) -> Dict[str, Any]:
#     #     with self.metrics_lock:
#     #         current_time = monotonic()
#     #         elapsed = current_time - self.start_time
            
#     #         metrics = {
#     #             "throughput": {
#     #                 "total_mbps": (self.total_bytes * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
#     #             },
#     #             "latency": {
#     #                 "min_ms": 0,
#     #                 "max_ms": 0,
#     #                 "avg_ms": 0,
#     #                 "jitter_ms": self._calculate_jitter(self.packet_timestamps)
#     #             }
#     #         }
            
#     #         # Interface latency measurement
#     #         self._update_interfaces()
#     #         for iface, data in self._interfaces.items():
#     #             if iface.startswith('uesimtun'):
#     #                 latency = self._measure_interface_latency(iface)
#     #                 if latency > 0:
#     #                     metrics['latency'].update({
#     #                         "min_ms": min(metrics['latency']['min_ms'], latency) if metrics['latency']['min_ms'] > 0 else latency,
#     #                         "max_ms": max(metrics['latency']['max_ms'], latency),
#     #                         "avg_ms": latency if metrics['latency']['avg_ms'] == 0 else (metrics['latency']['avg_ms'] + latency) / 2
#     #                     })
            
#     #         # Calculate readings per second
#     #         readings_per_second = 0
#     #         if self.sensor_intervals:
#     #             avg_interval = statistics.mean(self.sensor_intervals)
#     #             if avg_interval > 0:
#     #                 readings_per_second = 1 / avg_interval
            
#     #         # Sensor metrics
#     #         metrics["sensor_metrics"] = {
#     #             "reading_rate": {
#     #                 "current_rps": readings_per_second,
#     #                 "reading_interval_ms": statistics.mean(self.sensor_intervals) * 1000 if self.sensor_intervals else 0,
#     #                 "total_readings": self.total_readings,
#     #                 "readings_lost": self.readings_lost
#     #             },
#     #             "by_sensor": {}
#     #         }
            
#     #         # Per-sensor metrics
#     #         for sensor_id, sensor_data in self.readings_by_sensor.items():
#     #             latest_readings = list(sensor_data["values"])
#     #             if latest_readings:
#     #                 latest_values = [r["value"] for r in latest_readings]
#     #                 metrics["sensor_metrics"]["by_sensor"][sensor_id] = {
#     #                     "total_readings": sensor_data["total_readings"],
#     #                     "readings_lost": sensor_data["readings_lost"],
#     #                     "latest_value": latest_values[-1],
#     #                     "min_value": min(latest_values, key=lambda x: x.get("value", 0)),
#     #                     "max_value": max(latest_values, key=lambda x: x.get("value", 0)),
#     #                     "avg_value": statistics.mean([x.get("value", 0) for x in latest_values])
#     #                 }
            
#     #         return metrics

#     def calculate_metrics(self) -> Dict[str, Any]:
#         with self.metrics_lock:
#             current_time = monotonic()
#             elapsed = current_time - self.start_time
            
#             # Calculate throughput
#             total_bytes = self.total_bytes
#             throughput_mbps = (total_bytes * 8) / (1_000_000 * max(elapsed, 1))
            
#             # Calculate latency statistics
#             latencies = []
#             for sensor_data in self.readings_by_sensor.values():
#                 for reading in sensor_data['values']:
#                     if 'timestamp' in reading and 'value' in reading and 'timestamp' in reading['value']:
#                         receive_time = reading['timestamp']
#                         send_time = reading['value']['timestamp']
#                         latency = receive_time - send_time
#                         if latency >= 0:
#                             latencies.append(latency * 1000)
            
#             # Calculate jitter
#             jitter = 0
#             if len(self.packet_timestamps) >= 2:
#                 delays = []
#                 timestamps = sorted(list(self.packet_timestamps))
#                 for i in range(1, len(timestamps)):
#                     delay = timestamps[i] - timestamps[i-1]
#                     delays.append(delay)
                
#                 if delays:
#                     avg_delay = sum(delays) / len(delays)
#                     jitter = sum(abs(d - avg_delay) for d in delays) / len(delays)
#                     jitter *= 1000  # Convert to ms
            
#             # Calculate readings per second
#             current_rps = 0
#             if self.sensor_intervals:
#                 avg_interval = statistics.mean(self.sensor_intervals)
#                 if avg_interval > 0:
#                     current_rps = 1 / avg_interval
            
#             metrics = {
#                 "throughput": {
#                     "total_mbps": throughput_mbps
#                 },
#                 "latency": {
#                     "min_ms": min(latencies) if latencies else 0,
#                     "max_ms": max(latencies) if latencies else 0,
#                     "avg_ms": sum(latencies) / len(latencies) if latencies else 0,
#                     "jitter_ms": jitter
#                 },
#                 "sensor_metrics": {
#                     "reading_rate": {
#                         "current_rps": current_rps,
#                         "reading_interval_ms": statistics.mean(self.sensor_intervals) * 1000 if self.sensor_intervals else 0,
#                         "total_readings": sum(data['total_readings'] for data in self.readings_by_sensor.values()),
#                         "readings_lost": sum(data['readings_lost'] for data in self.readings_by_sensor.values())
#                     },
#                     "by_sensor": {}
#                 }
#             }
            
#             # Calculate per-sensor metrics
#             for sensor_id, sensor_data in self.readings_by_sensor.items():
#                 readings = list(sensor_data['values'])
#                 if readings:
#                     latest = readings[-1]
#                     metrics["sensor_metrics"]["by_sensor"][sensor_id] = {
#                         "total_readings": sensor_data['total_readings'],
#                         "readings_lost": sensor_data['readings_lost'],
#                         "latest_value": latest['value'],
#                         "min_value": min(readings, key=lambda x: x['timestamp'])['value'],
#                         "max_value": max(readings, key=lambda x: x['timestamp'])['value'],
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

import json
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

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Packet metrics with timestamps
        self.packet_timestamps = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        self.total_packets = 0
        self.total_bytes = 0
        
        # Sensor specific metrics
        self.sensor_readings = deque(maxlen=window_size)
        self.sensor_intervals = deque(maxlen=30)
        self.total_readings = 0
        self.readings_lost = 0
        self.last_reading_time = None
        self.last_sequence_number = -1
        self.readings_by_sensor = {}
        self.sensor_timestamps = deque(maxlen=30)
        
        # Network latency tracking
        self.latencies = deque(maxlen=window_size)
        
        # Interface monitoring
        self._interfaces = {}
        self._prev_stats = {}
        self._last_update = monotonic()
        self._update_interfaces()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self._monitor_thread.start()

    def _update_interfaces(self):
        try:
            interfaces = {}
            for iface in psutil.net_if_stats().keys():
                if iface.startswith('uesimtun') or iface == 'ogstun':
                    addr = self._get_interface_address(iface)
                    if addr:
                        interfaces[iface] = {
                            'address': addr,
                            'stats': psutil.net_io_counters(pernic=True).get(iface)
                        }
            self._interfaces = interfaces
        except Exception as e:
            logger.error(f"Error updating interfaces: {e}")

    def _get_interface_address(self, iface: str) -> Optional[str]:
        try:
            addrs = psutil.net_if_addrs().get(iface, [])
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address
        except Exception as e:
            logger.error(f"Error getting interface address: {e}")
        return None

    def _calculate_jitter(self, timestamps: deque) -> float:
        """Calculate jitter using RFC 3550 algorithm"""
        if len(timestamps) < 2:
            return 0.0
        
        jitter = 0.0
        prev_timestamp = timestamps[0]
        
        for timestamp in list(timestamps)[1:]:
            delay = abs(timestamp - prev_timestamp)
            jitter = jitter + (delay - jitter) / 16
            prev_timestamp = timestamp
            
        return jitter * 1000  # Convert to ms

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        with self.metrics_lock:
            # Calculate packet size consistently
            size = len(json.dumps(data)) if isinstance(data, (dict, list)) else len(data)
            self.total_bytes += size
            self.total_packets += 1
            self.packet_sizes.append(size)
            self.packet_timestamps.append(timestamp)
            
            if isinstance(data, dict) and "sensor_id" in data:
                self.total_readings += 1
                sensor_id = data["sensor_id"]
                
                if sensor_id not in self.readings_by_sensor:
                    self.readings_by_sensor[sensor_id] = {
                        "total_readings": 0,
                        "last_sequence": -1,
                        "readings_lost": 0,
                        "values": deque(maxlen=30)
                    }
                
                self.readings_by_sensor[sensor_id]["total_readings"] += 1
                self.readings_by_sensor[sensor_id]["values"].append({
                    "timestamp": timestamp,
                    "value": data
                })
                
                if self.last_reading_time is not None:
                    interval = timestamp - self.last_reading_time
                    if interval > 0:
                        self.sensor_intervals.append(interval)
                
                self.last_reading_time = timestamp
                self.sensor_timestamps.append(timestamp)

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            # Calculate packet size consistently
            size = len(json.dumps(data)) if isinstance(data, (dict, list)) else len(data)
            self.total_bytes += size
            self.total_packets += 1
            self.packet_sizes.append(size)
            self.packet_timestamps.append(timestamp)
            
            if isinstance(data, dict) and "sensor_id" in data:
                sensor_id = data["sensor_id"]
                current_sequence = data.get("sequence", -1)
                
                # Calculate network latency using timestamps
                if "timestamp" in data:
                    send_time = data["timestamp"]
                    latency = timestamp - send_time
                    if latency >= 0:  # Avoid negative latencies
                        self.latencies.append(latency)
                
                if sensor_id not in self.readings_by_sensor:
                    self.readings_by_sensor[sensor_id] = {
                        "total_readings": 0,
                        "last_sequence": -1,
                        "readings_lost": 0,
                        "values": deque(maxlen=30)
                    }
                
                sensor_info = self.readings_by_sensor[sensor_id]
                
                # Track sequence numbers for lost readings
                if current_sequence >= 0:
                    if sensor_info["last_sequence"] >= 0:
                        expected_sequence = sensor_info["last_sequence"] + 1
                        if current_sequence > expected_sequence:
                            readings_lost = current_sequence - expected_sequence
                            sensor_info["readings_lost"] += readings_lost
                            self.readings_lost += readings_lost
                    
                    sensor_info["last_sequence"] = current_sequence
                
                sensor_info["total_readings"] += 1
                sensor_info["values"].append({
                    "timestamp": timestamp,
                    "value": data
                })
                
                self.total_readings += 1
                self.sensor_readings.append(data)
                self.sensor_timestamps.append(timestamp)
                
                if self.last_reading_time is not None:
                    interval = timestamp - self.last_reading_time
                    if interval > 0:
                        self.sensor_intervals.append(interval)
                
                self.last_reading_time = timestamp

    def _measure_interface_latency(self, interface: str) -> float:
        """Measure network latency using ping"""
        try:
            result = subprocess.run(
                ['ping', '-I', interface, '-c', '1', '-W', '1', '10.45.0.1'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                match = re.search(r'time=([\d.]+)', result.stdout)
                if match:
                    return float(match.group(1))
            return 0
        except Exception as e:
            logger.error(f"Error measuring latency for interface {interface}: {e}")
            return 0

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = max(current_time - self.start_time, 0.001)  # Avoid division by zero
            
            # Calculate throughput based on actual data transferred
            throughput_mbps = (self.total_bytes * 8) / (elapsed * 1_000_000)
            
            # Calculate latency statistics from recorded latencies
            latency_stats = {
                "min_ms": min(self.latencies) * 1000 if self.latencies else 0,
                "max_ms": max(self.latencies) * 1000 if self.latencies else 0,
                "avg_ms": statistics.mean(self.latencies) * 1000 if self.latencies else 0,
                "jitter_ms": self._calculate_jitter(self.packet_timestamps)
            }
            
            # Update latency with ping measurements for verification
            self._update_interfaces()
            for iface, data in self._interfaces.items():
                if iface.startswith('uesimtun'):
                    ping_latency = self._measure_interface_latency(iface)
                    if ping_latency > 0:
                        latency_stats.update({
                            "min_ms": min(latency_stats["min_ms"], ping_latency) if latency_stats["min_ms"] > 0 else ping_latency,
                            "max_ms": max(latency_stats["max_ms"], ping_latency),
                            "avg_ms": ping_latency if latency_stats["avg_ms"] == 0 else (latency_stats["avg_ms"] + ping_latency) / 2
                        })
            
            # Calculate current readings per second
            current_rps = 0
            if self.sensor_intervals:
                avg_interval = statistics.mean(self.sensor_intervals)
                if avg_interval > 0:
                    current_rps = 1 / avg_interval
            
            metrics = {
                "throughput": {
                    "total_mbps": throughput_mbps
                },
                "latency": latency_stats,
                "sensor_metrics": {
                    "reading_rate": {
                        "current_rps": current_rps,
                        "reading_interval_ms": statistics.mean(self.sensor_intervals) * 1000 if self.sensor_intervals else 0,
                        "total_readings": self.total_readings,
                        "readings_lost": self.readings_lost
                    },
                    "by_sensor": {}
                }
            }
            
            # Calculate per-sensor metrics
            for sensor_id, sensor_data in self.readings_by_sensor.items():
                readings = list(sensor_data["values"])
                if readings:
                    latest = readings[-1]["value"]
                    metrics["sensor_metrics"]["by_sensor"][sensor_id] = {
                        "total_readings": sensor_data["total_readings"],
                        "readings_lost": sensor_data["readings_lost"],
                        "latest_value": latest,
                        "min_value": min(readings, key=lambda x: x["value"].get("sequence", 0))["value"],
                        "max_value": max(readings, key=lambda x: x["value"].get("sequence", 0))["value"]
                    }
            
            return metrics

    def _monitor_network(self):
        while True:
            try:
                self._update_interfaces()
                sleep(1)
            except Exception as e:
                logger.error(f"Error in network monitor: {e}")
                sleep(5)

    def reset(self):
        with self.metrics_lock:
            self.start_time = monotonic()
            self.packet_timestamps.clear()
            self.packet_sizes.clear()
            self.total_packets = 0
            self.total_bytes = 0
            self.sensor_readings.clear()
            self.sensor_intervals.clear()
            self.sensor_timestamps.clear()
            self.total_readings = 0
            self.readings_lost = 0
            self.last_reading_time = None
            self.last_sequence_number = -1
            self.readings_by_sensor.clear()
            self.latencies.clear()
            self._prev_stats = {}