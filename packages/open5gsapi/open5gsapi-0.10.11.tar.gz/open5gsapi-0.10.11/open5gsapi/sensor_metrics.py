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
        self.readings_by_sensor = {}  # Will be initialized when first sensor data arrives
        self.sensor_intervals = deque(maxlen=30)
        self.last_reading_time = None
        self.readings_timestamps = deque(maxlen=30)

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

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        with self.metrics_lock:
            size = len(str(data)) if isinstance(data, (dict, list)) else len(data)
            self.total_bytes += size
            self.total_packets += 1
            self.packet_sizes.append(size)
            self.packet_timestamps.append(timestamp)
            
            if isinstance(data, dict) and "sensor_id" in data:
                sensor_id = data["sensor_id"]
                if sensor_id not in self.readings_by_sensor:
                    self.readings_by_sensor[sensor_id] = {
                        "total_readings": 0,
                        "last_sequence": -1,
                        "readings_lost": 0,
                        "values": deque(maxlen=30),
                        "latencies": deque(maxlen=30)
                    }
                
                # Include source_ip (UE TUN IP) and size in the reading data
                reading_data = {
                    'timestamp': timestamp,
                    'value': data,
                    'size': size,
                    'source_ip': data.get('ue_ip'),  # This should be the 10.45.0.x address
                    'dest_ip': '10.45.0.1'  # UPF TUN interface
                }
                
                self.readings_by_sensor[sensor_id]["values"].append(reading_data)
                self.readings_by_sensor[sensor_id]["total_readings"] += 1
                
                if self.last_reading_time is not None:
                    interval = timestamp - self.last_reading_time
                    if interval > 0:
                        self.sensor_intervals.append(interval)
                
                self.last_reading_time = timestamp
                self.readings_timestamps.append(timestamp)

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            size = len(str(data)) if isinstance(data, (dict, list)) else len(data)
            self.total_bytes += size
            self.total_packets += 1
            self.packet_sizes.append(size)
            self.packet_timestamps.append(timestamp)
            
            if isinstance(data, dict) and "sensor_id" in data:
                sensor_id = data["sensor_id"]
                source_ip = data.get('ue_ip')  # The UE TUN IP (10.45.0.x)
                
                if sensor_id not in self.readings_by_sensor:
                    self.readings_by_sensor[sensor_id] = {
                        "total_readings": 0,
                        "last_sequence": -1,
                        "readings_lost": 0,
                        "values": deque(maxlen=30),
                        "latencies": deque(maxlen=30)
                    }
                
                sensor_info = self.readings_by_sensor[sensor_id]
                
                # Find matching sent packet for accurate latency calculation
                for sent_reading in reversed(list(sensor_info["values"])):
                    if (sent_reading['value'].get('sequence') == data.get('sequence') and 
                        sent_reading['source_ip'] == source_ip):
                        # Calculate network latency
                        latency = (timestamp - sent_reading['timestamp']) * 1000  # ms
                        throughput = (sent_reading['size'] * 8) / (latency / 1000) / 1_000_000  # Mbps
                        
                        # Store latency for jitter calculations
                        sensor_info["latencies"].append(latency)
                        
                        # Store received data with network metrics
                        reading_data = {
                            'timestamp': timestamp,
                            'value': data,
                            'latency': latency,
                            'throughput': throughput,
                            'size': size
                        }
                        break
                else:
                    # If no matching sent packet found
                    reading_data = {
                        'timestamp': timestamp,
                        'value': data,
                        'size': size
                    }
                
                sensor_info["values"].append(reading_data)
                sensor_info["total_readings"] += 1
                
                # Handle sequence tracking
                if 'sequence' in data:
                    current_sequence = data['sequence']
                    if sensor_info["last_sequence"] >= 0:
                        expected_sequence = sensor_info["last_sequence"] + 1
                        if current_sequence > expected_sequence:
                            sensor_info["readings_lost"] += current_sequence - expected_sequence
                    sensor_info["last_sequence"] = current_sequence
                
                if self.last_reading_time is not None:
                    interval = timestamp - self.last_reading_time
                    if interval > 0:
                        self.sensor_intervals.append(interval)
                
                self.last_reading_time = timestamp
                self.readings_timestamps.append(timestamp)

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = max(current_time - self.start_time, 0.001)  # Avoid division by zero
            
            metrics = {
                "throughput": {"total_mbps": 0.0},
                "latency": {
                    "min_ms": 0,
                    "max_ms": 0,
                    "avg_ms": 0,
                    "jitter_ms": 0
                },
                "sensor_metrics": {
                    "reading_rate": {
                        "current_rps": 0,
                        "reading_interval_ms": 0,
                        "total_readings": 0,
                        "readings_lost": 0
                    },
                    "by_sensor": {}
                }
            }
            
            total_latencies = []
            total_throughput = 0
            total_packets = 0
            
            # Calculate per-sensor metrics and aggregate
            for sensor_id, sensor_data in self.readings_by_sensor.items():
                readings = list(sensor_data["values"])
                latencies = list(sensor_data.get("latencies", []))
                
                if readings:
                    recent_readings = readings[-10:]  # Last 10 readings for rate calculation
                    if len(recent_readings) >= 2:
                        time_diff = recent_readings[-1]['timestamp'] - recent_readings[0]['timestamp']
                        if time_diff > 0:
                            current_rps = len(recent_readings) / time_diff
                        else:
                            current_rps = 0
                    else:
                        current_rps = 0
                    
                    # Calculate sensor-specific metrics
                    sensor_metrics = {
                        "total_readings": sensor_data["total_readings"],
                        "readings_lost": sensor_data["readings_lost"],
                        "latest_value": readings[-1]['value'],
                        "min_value": min(readings, key=lambda x: x['timestamp'])['value'],
                        "max_value": max(readings, key=lambda x: x['timestamp'])['value']
                    }
                    
                    # Add network metrics if available
                    if latencies:
                        sensor_metrics.update({
                            "latency_ms": {
                                "min": min(latencies),
                                "max": max(latencies),
                                "avg": sum(latencies) / len(latencies)
                            }
                        })
                        total_latencies.extend(latencies)
                    
                    metrics["sensor_metrics"]["by_sensor"][sensor_id] = sensor_metrics
                    total_packets += sensor_data["total_readings"]
            
            # Calculate overall metrics
            if total_latencies:
                metrics["latency"].update({
                    "min_ms": min(total_latencies),
                    "max_ms": max(total_latencies),
                    "avg_ms": sum(total_latencies) / len(total_latencies)
                })
                
                # Calculate jitter using consecutive latency differences
                if len(total_latencies) >= 2:
                    jitter = sum(abs(total_latencies[i] - total_latencies[i-1]) 
                               for i in range(1, len(total_latencies))) / (len(total_latencies) - 1)
                    metrics["latency"]["jitter_ms"] = jitter
            
            # Calculate overall throughput
            metrics["throughput"]["total_mbps"] = (self.total_bytes * 8) / (elapsed * 1_000_000)
            
            # Calculate overall reading rate
            if self.sensor_intervals:
                avg_interval = statistics.mean(self.sensor_intervals)
                current_rps = 1 / avg_interval if avg_interval > 0 else 0
                metrics["sensor_metrics"]["reading_rate"].update({
                    "current_rps": current_rps,
                    "reading_interval_ms": avg_interval * 1000,
                    "total_readings": total_packets,
                    "readings_lost": sum(data["readings_lost"] for data in self.readings_by_sensor.values())
                })
            
            return metrics

    def _measure_interface_latency(self, interface: str) -> float:
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
            self.sensor_intervals.clear()
            self.readings_timestamps.clear()
            self.last_reading_time = None
            self.readings_by_sensor.clear()
            self._prev_stats = {}
