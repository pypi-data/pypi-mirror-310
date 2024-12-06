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
import json
from collections import deque
from time import monotonic, sleep
from typing import Dict, Any, Optional, Deque, Union, Tuple

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Interface mapping
        self.ue_interfaces = self._get_ue_interfaces()  # Get uesimtun interfaces from UE container
        self.upf_interface = self._get_upf_interface()  # Get ogstun interface from UPF container
        logger.info(f"Detected UE interfaces: {self.ue_interfaces}")
        logger.info(f"Detected UPF interface: {self.upf_interface}")
        
        # Packet tracking per interface
        self.interface_packets = {
            'ue': {},  # {interface: {packet_id: (timestamp, size)}}
            'upf': {}  # {packet_id: (timestamp, size)}
        }
        
        # Metrics storage
        self.latencies = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        self.total_bytes = 0
        self.total_packets = 0
        
        # Sensor specific metrics
        self.sensor_readings = deque(maxlen=window_size)
        self.sensor_intervals = deque(maxlen=30)
        self.total_readings = 0
        self.readings_lost = 0
        self.readings_by_sensor = {}
        
        # Start interface monitoring
        self._monitor_thread = threading.Thread(target=self._monitor_interfaces, daemon=True)
        self._monitor_thread.start()

    def _run_docker_command(self, container: str, command: str) -> str:
        """Execute command inside docker container"""
        try:
            cmd = f"docker exec {container} {command}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"Docker command failed: {result.stderr}")
                return ""
        except Exception as e:
            logger.error(f"Error executing docker command: {e}")
            return ""

    def _get_ue_interfaces(self) -> Dict[str, str]:
        """Get all uesimtun interfaces and their IPs from UE container"""
        interfaces = {}
        ifconfig_output = self._run_docker_command('ue', 'ifconfig')
        
        # Parse ifconfig output for uesimtun interfaces
        current_interface = None
        for line in ifconfig_output.split('\n'):
            if 'uesimtun' in line:
                current_interface = line.split()[0]
            elif current_interface and 'inet ' in line:
                ip = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', line)
                if ip:
                    interfaces[current_interface] = ip.group(1)
                current_interface = None
                
        return interfaces

    def _get_upf_interface(self) -> Optional[str]:
        """Get ogstun interface IP from UPF container"""
        ifconfig_output = self._run_docker_command('upf', 'ifconfig ogstun')
        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ifconfig_output)
        return ip_match.group(1) if ip_match else None

    def _monitor_interfaces(self):
        """Monitor network interfaces in containers"""
        while True:
            try:
                # Update interface lists periodically
                self.ue_interfaces = self._get_ue_interfaces()
                self.upf_interface = self._get_upf_interface()
                sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Error monitoring interfaces: {e}")
                sleep(5)

    def _get_interface_for_ip(self, ip: str) -> Optional[str]:
        """Get the interface name for a given IP"""
        for interface, interface_ip in self.ue_interfaces.items():
            if interface_ip == ip:
                return interface
        return None

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record data being sent from UE"""
        with self.metrics_lock:
            try:
                size = len(json.dumps(data)) if isinstance(data, dict) else len(data)
                
                if isinstance(data, dict) and 'ue_ip' in data:
                    source_ip = data['ue_ip']
                    interface = self._get_interface_for_ip(source_ip)
                    
                    if interface and source_ip.startswith('10.45.0.'):
                        # Generate unique packet identifier
                        packet_id = f"{data.get('sensor_id', '')}_{data.get('sequence', self.total_packets)}"
                        
                        # Record packet timing for the specific interface
                        if interface not in self.interface_packets['ue']:
                            self.interface_packets['ue'][interface] = {}
                        self.interface_packets['ue'][interface][packet_id] = (timestamp, size)
                        
                        logger.debug(f"UE {interface} ({source_ip}) sent packet {packet_id} at {timestamp}")
                        
                        # Update metrics
                        self.total_bytes += size
                        self.total_packets += 1
                        self.packet_sizes.append(size)
                        
                        # Handle sensor data
                        if 'sensor_id' in data:
                            self._update_sensor_metrics(data, timestamp)
                            
            except Exception as e:
                logger.error(f"Error recording sent data: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record data being received at UPF"""
        with self.metrics_lock:
            try:
                size = len(json.dumps(data)) if isinstance(data, dict) else len(data)
                
                if isinstance(data, dict) and 'source_ip' in data:
                    source_ip = data['source_ip']
                    
                    if source_ip.startswith('10.45.0.'):
                        # Generate packet identifier
                        packet_id = f"{data.get('sensor_id', '')}_{data.get('sequence', self.total_packets)}"
                        
                        # Find corresponding UE send time
                        ue_data = None
                        for interface, packets in self.interface_packets['ue'].items():
                            if packet_id in packets:
                                ue_data = packets[packet_id]
                                break
                        
                        if ue_data:
                            ue_timestamp, _ = ue_data
                            # Calculate latency
                            latency = timestamp - ue_timestamp
                            if latency > 0:
                                self.latencies.append(latency)
                                logger.debug(f"Packet {packet_id} latency: {latency*1000:.2f}ms")
                        
                        # Record UPF receive time
                        self.interface_packets['upf'][packet_id] = (timestamp, size)
                        
                        logger.debug(f"UPF received packet {packet_id} at {timestamp}")
                        
                        # Update metrics
                        if 'sensor_id' in data:
                            self._update_sensor_metrics(data, timestamp)
                            
            except Exception as e:
                logger.error(f"Error recording received data: {e}")

    def _update_sensor_metrics(self, data: Dict, timestamp: float):
        """Update sensor-specific metrics"""
        sensor_id = data.get('sensor_id')
        if not sensor_id:
            return
            
        if sensor_id not in self.readings_by_sensor:
            self.readings_by_sensor[sensor_id] = {
                "total_readings": 0,
                "last_sequence": -1,
                "readings_lost": 0,
                "values": deque(maxlen=30)
            }
        
        sensor_data = self.readings_by_sensor[sensor_id]
        current_sequence = data.get('sequence', -1)
        
        if sensor_data["last_sequence"] >= 0 and current_sequence > sensor_data["last_sequence"] + 1:
            lost = current_sequence - (sensor_data["last_sequence"] + 1)
            sensor_data["readings_lost"] += lost
            self.readings_lost += lost
        
        sensor_data["last_sequence"] = current_sequence
        sensor_data["total_readings"] += 1
        sensor_data["values"].append({"timestamp": timestamp, "value": data.copy()})
        
        self.total_readings += 1
        self.sensor_readings.append(data)
        
        # Calculate intervals
        if len(sensor_data["values"]) >= 2:
            interval = timestamp - list(sensor_data["values"])[-2]["timestamp"]
            if interval > 0:
                self.sensor_intervals.append(interval)

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = max(current_time - self.start_time, 0.001)
            
            # Calculate metrics
            metrics = {
                "throughput": {
                    "total_mbps": (self.total_bytes * 8) / (elapsed * 1_000_000)
                },
                "latency": {
                    "min_ms": min(l * 1000 for l in self.latencies) if self.latencies else 0,
                    "max_ms": max(l * 1000 for l in self.latencies) if self.latencies else 0,
                    "avg_ms": (sum(l * 1000 for l in self.latencies) / len(self.latencies)) if self.latencies else 0,
                    "jitter_ms": self._calculate_jitter(self.latencies)
                },
                "sensor_metrics": {
                    "reading_rate": {
                        "current_rps": 1 / statistics.mean(self.sensor_intervals) if self.sensor_intervals else 0,
                        "reading_interval_ms": statistics.mean(self.sensor_intervals) * 1000 if self.sensor_intervals else 0,
                        "total_readings": self.total_readings,
                        "readings_lost": self.readings_lost
                    },
                    "by_sensor": {}
                }
            }
            
            # Add per-sensor metrics
            for sensor_id, sensor_data in self.readings_by_sensor.items():
                readings = list(sensor_data["values"])
                if readings:
                    metrics["sensor_metrics"]["by_sensor"][sensor_id] = {
                        "total_readings": sensor_data["total_readings"],
                        "readings_lost": sensor_data["readings_lost"],
                        "latest_value": readings[-1]["value"],
                        "min_value": min(readings, key=lambda x: x["value"].get("sequence", 0))["value"],
                        "max_value": max(readings, key=lambda x: x["value"].get("sequence", 0))["value"]
                    }
            
            return metrics

    def _calculate_jitter(self, latencies: deque) -> float:
        """Calculate jitter using RFC 3550 algorithm"""
        if len(latencies) < 2:
            return 0.0
        
        jitter = 0.0
        prev_latency = None
        for latency in latencies:
            if prev_latency is not None:
                variation = abs(latency - prev_latency)
                jitter = jitter + (variation - jitter) / 16
            prev_latency = latency
        
        return jitter * 1000  # Convert to milliseconds

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.interface_packets = {'ue': {}, 'upf': {}}
            self.latencies.clear()
            self.packet_sizes.clear()
            self.total_bytes = 0
            self.total_packets = 0
            self.sensor_readings.clear()
            self.sensor_intervals.clear()
            self.total_readings = 0
            self.readings_lost = 0
            self.readings_by_sensor.clear()