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
import pyshark # type: ignore
from collections import deque
from time import monotonic, sleep
from typing import Dict, Any, Optional, Deque, Union, Tuple

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Packet capture configuration
        self.ue_capture = None
        self.upf_capture = None
        self.packet_pairs = {}  # {packet_id: {'ue_time': timestamp, 'upf_time': timestamp}}
        
        # Metrics storage
        self.latencies = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        self.total_bytes = 0
        self.total_packets = 0
        
        # Start packet capture
        self._start_packet_capture()
        
        # Other metrics remain the same
        self.sensor_readings = deque(maxlen=window_size)
        self.sensor_intervals = deque(maxlen=30)
        self.total_readings = 0
        self.readings_lost = 0
        self.readings_by_sensor = {}

    def _start_packet_capture(self):
        """Start capturing packets on both UE and UPF interfaces"""
        try:
            # Start UE capture (inside UE container)
            ue_cmd = "docker exec ue tshark -i uesimtun0 -f 'ip src 10.45.0.2 or ip dst 10.45.0.2' -T fields -e frame.time_epoch -e ip.src -e ip.dst -e frame.len"
            self.ue_capture = subprocess.Popen(
                ue_cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Start UPF capture (inside UPF container)
            upf_cmd = "docker exec upf tshark -i ogstun -f 'ip src 10.45.0.1 or ip dst 10.45.0.1' -T fields -e frame.time_epoch -e ip.src -e ip.dst -e frame.len"
            self.upf_capture = subprocess.Popen(
                upf_cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Start packet processing threads
            threading.Thread(target=self._process_ue_packets, daemon=True).start()
            threading.Thread(target=self._process_upf_packets, daemon=True).start()

            logger.info("Packet capture started successfully")
        except Exception as e:
            logger.error(f"Failed to start packet capture: {e}")
            raise

    def _process_ue_packets(self):
        """Process packets captured on UE interface"""
        while True:
            try:
                line = self.ue_capture.stdout.readline()
                if line:
                    timestamp, src_ip, dst_ip, length = line.strip().split()
                    timestamp = float(timestamp)
                    length = int(length)
                    
                    if src_ip.startswith('10.45.0.'):
                        packet_id = f"{src_ip}_{dst_ip}_{timestamp}"
                        with self.metrics_lock:
                            self.packet_pairs[packet_id] = {'ue_time': timestamp, 'size': length}
                            self.total_bytes += length
                            self.total_packets += 1
                            self.packet_sizes.append(length)
            except Exception as e:
                logger.error(f"Error processing UE packet: {e}")
                sleep(0.1)

    def _process_upf_packets(self):
        """Process packets captured on UPF interface"""
        while True:
            try:
                line = self.upf_capture.stdout.readline()
                if line:
                    timestamp, src_ip, dst_ip, length = line.strip().split()
                    timestamp = float(timestamp)
                    
                    # Look for matching packet from UE
                    for packet_id, data in list(self.packet_pairs.items()):
                        if 'ue_time' in data and 'upf_time' not in data:
                            # Calculate latency
                            latency = timestamp - data['ue_time']
                            if latency > 0:
                                with self.metrics_lock:
                                    self.latencies.append(latency)
                                    data['upf_time'] = timestamp
                            logger.debug(f"Latency recorded: {latency*1000:.2f}ms")
            except Exception as e:
                logger.error(f"Error processing UPF packet: {e}")
                sleep(0.1)

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record application-level metrics"""
        with self.metrics_lock:
            if isinstance(data, dict) and 'sensor_id' in data:
                sensor_id = data['sensor_id']
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
                    "value": data.copy()
                })
                self.total_readings += 1

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record application-level metrics"""
        with self.metrics_lock:
            if isinstance(data, dict) and 'sensor_id' in data:
                sensor_id = data['sensor_id']
                if sensor_id in self.readings_by_sensor:
                    current_sequence = data.get('sequence', 0)
                    last_sequence = self.readings_by_sensor[sensor_id]["last_sequence"]
                    
                    if last_sequence >= 0 and current_sequence > last_sequence + 1:
                        readings_lost = current_sequence - (last_sequence + 1)
                        self.readings_by_sensor[sensor_id]["readings_lost"] += readings_lost
                        self.readings_lost += readings_lost
                    
                    self.readings_by_sensor[sensor_id]["last_sequence"] = current_sequence

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = max(current_time - self.start_time, 0.001)
            
            # Calculate latency statistics
            latency_stats = {
                "min_ms": min(l * 1000 for l in self.latencies) if self.latencies else 0,
                "max_ms": max(l * 1000 for l in self.latencies) if self.latencies else 0,
                "avg_ms": (sum(l * 1000 for l in self.latencies) / len(self.latencies)) if self.latencies else 0,
                "jitter_ms": self._calculate_jitter(self.latencies)
            }
            
            # Calculate throughput
            throughput = (self.total_bytes * 8) / (elapsed * 1_000_000) if self.total_bytes > 0 else 0

            metrics = {
                "throughput": {
                    "total_mbps": throughput
                },
                "latency": latency_stats,
                "sensor_metrics": {
                    "reading_rate": {
                        "current_rps": len(self.latencies) / elapsed if elapsed > 0 else 0,
                        "reading_interval_ms": (elapsed * 1000) / len(self.latencies) if self.latencies else 0,
                        "total_readings": self.total_readings,
                        "readings_lost": self.readings_lost
                    },
                    "by_sensor": self._get_sensor_metrics()
                }
            }
            
            return metrics

    def _get_sensor_metrics(self) -> Dict[str, Any]:
        """Get per-sensor metrics"""
        sensor_metrics = {}
        for sensor_id, sensor_data in self.readings_by_sensor.items():
            readings = list(sensor_data["values"])
            if readings:
                sensor_metrics[sensor_id] = {
                    "total_readings": sensor_data["total_readings"],
                    "readings_lost": sensor_data["readings_lost"],
                    "latest_value": readings[-1]["value"],
                    "min_value": min(readings, key=lambda x: x["value"].get("sequence", 0))["value"],
                    "max_value": max(readings, key=lambda x: x["value"].get("sequence", 0))["value"]
                }
        return sensor_metrics

    def _calculate_jitter(self, latencies: deque) -> float:
        if len(latencies) < 2:
            return 0.0
        
        jitter = 0.0
        prev_latency = None
        for latency in latencies:
            if prev_latency is not None:
                variation = abs(latency - prev_latency)
                jitter = jitter + (variation - jitter) / 16
            prev_latency = latency
        
        return jitter * 1000

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            # Restart packet capture
            if self.ue_capture:
                self.ue_capture.terminate()
            if self.upf_capture:
                self.upf_capture.terminate()
            self._start_packet_capture()
            
            # Reset metrics
            self.start_time = monotonic()
            self.packet_pairs.clear()
            self.latencies.clear()
            self.packet_sizes.clear()
            self.total_bytes = 0
            self.total_packets = 0
            self.sensor_readings.clear()
            self.sensor_intervals.clear()
            self.total_readings = 0
            self.readings_lost = 0
            self.readings_by_sensor.clear()

    def __del__(self):
        """Cleanup packet capture processes"""
        if self.ue_capture:
            self.ue_capture.terminate()
        if self.upf_capture:
            self.upf_capture.terminate()