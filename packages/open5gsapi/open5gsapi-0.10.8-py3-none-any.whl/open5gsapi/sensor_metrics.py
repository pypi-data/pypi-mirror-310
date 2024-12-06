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
from typing import Dict, Any, Optional, Deque, Union
import time

logger = logging.getLogger(__name__)

class SensorMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        
        # Track packets and their timestamps
        self.packet_pairs = {}  # {unique_id: {'send_time', 'receive_time', 'size'}}
        self.completed_packets = deque(maxlen=window_size)  # Store completed transmissions
        
        # Sensor specific metrics
        self.readings_by_sensor = {}
        self.sensor_intervals = deque(maxlen=30)
        self.last_reading_time = None
        
        # Interface monitoring
        self._interfaces = {}
        self._prev_stats = {}
        self._last_update = monotonic()
        self._update_interfaces()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self._monitor_thread.start()

    def _update_interfaces(self):
        """Update network interface information"""
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
        """Get IP address for a network interface"""
        try:
            addrs = psutil.net_if_addrs().get(iface, [])
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address
        except Exception as e:
            logger.error(f"Error getting interface address: {e}")
        return None

    def _generate_packet_id(self, data: dict) -> str:
        """Generate a unique ID for the packet"""
        return f"{data.get('sensor_id', 'unknown')}_{data.get('sequence', time.time_ns())}"

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record metrics when data is sent from UE"""
        with self.metrics_lock:
            if isinstance(data, dict) and "sensor_id" in data:
                # Generate packet ID
                packet_id = self._generate_packet_id(data)
                
                # Calculate actual packet size
                packet_size = len(json.dumps(data).encode())
                
                # Store send information
                self.packet_pairs[packet_id] = {
                    'send_time': timestamp,
                    'size': packet_size,
                    'receive_time': None
                }
                
                # Update sensor tracking
                sensor_id = data["sensor_id"]
                if sensor_id not in self.readings_by_sensor:
                    self.readings_by_sensor[sensor_id] = {
                        "total_readings": 0,
                        "last_sequence": -1,
                        "readings_lost": 0,
                        "values": deque(maxlen=30)
                    }
                
                # Update reading intervals
                if self.last_reading_time is not None:
                    interval = timestamp - self.last_reading_time
                    if interval > 0:
                        self.sensor_intervals.append(interval)
                self.last_reading_time = timestamp

                # Update reading count
                self.readings_by_sensor[sensor_id]["total_readings"] += 1

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record metrics when data is received at UPF"""
        with self.metrics_lock:
            if isinstance(data, dict) and "sensor_id" in data:
                # Generate packet ID
                packet_id = self._generate_packet_id(data)
                
                # If we have the corresponding send record
                if packet_id in self.packet_pairs:
                    packet_info = self.packet_pairs[packet_id]
                    packet_info['receive_time'] = timestamp
                    
                    # Calculate metrics for this packet
                    send_time = packet_info['send_time']
                    size = packet_info['size']
                    latency = (timestamp - send_time) * 1000  # Convert to ms
                    
                    # Add to completed packets
                    self.completed_packets.append({
                        'latency': latency,
                        'size': size,
                        'timestamp': timestamp,
                        'throughput': (size * 8) / (latency / 1000) / 1_000_000 if latency > 0 else 0  # Mbps
                    })
                    
                    # Clean up
                    del self.packet_pairs[packet_id]
                
                # Update sensor tracking
                sensor_id = data["sensor_id"]
                if sensor_id in self.readings_by_sensor:
                    current_sequence = data.get('sequence', -1)
                    last_sequence = self.readings_by_sensor[sensor_id]["last_sequence"]
                    
                    if last_sequence >= 0 and current_sequence > last_sequence + 1:
                        self.readings_by_sensor[sensor_id]["readings_lost"] += (current_sequence - last_sequence - 1)
                    
                    self.readings_by_sensor[sensor_id]["last_sequence"] = current_sequence
                    self.readings_by_sensor[sensor_id]["values"].append({
                        "timestamp": timestamp,
                        "value": data
                    })

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all metrics"""
        with self.metrics_lock:
            # Get completed packet metrics
            completed_packets = list(self.completed_packets)
            
            # Calculate latency statistics
            latencies = [p['latency'] for p in completed_packets if p['latency'] > 0]
            latency_stats = {
                "min_ms": min(latencies) if latencies else 0,
                "max_ms": max(latencies) if latencies else 0,
                "avg_ms": sum(latencies) / len(latencies) if latencies else 0,
                "jitter_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0
            }
            
            # Calculate throughput
            throughputs = [p['throughput'] for p in completed_packets if p['throughput'] > 0]
            avg_throughput = sum(throughputs) / len(throughputs) if throughputs else 0
            
            # Calculate reading rate
            current_rps = 0
            if self.sensor_intervals:
                avg_interval = statistics.mean(self.sensor_intervals)
                if avg_interval > 0:
                    current_rps = 1 / avg_interval
            
            return {
                "throughput": {
                    "total_mbps": avg_throughput
                },
                "latency": latency_stats,
                "sensor_metrics": {
                    "reading_rate": {
                        "current_rps": current_rps,
                        "reading_interval_ms": statistics.mean(self.sensor_intervals) * 1000 if self.sensor_intervals else 0,
                        "total_readings": sum(sensor["total_readings"] for sensor in self.readings_by_sensor.values()),
                        "readings_lost": sum(sensor["readings_lost"] for sensor in self.readings_by_sensor.values())
                    },
                    "by_sensor": {
                        sensor_id: {
                            "total_readings": sensor_data["total_readings"],
                            "readings_lost": sensor_data["readings_lost"],
                            "latest_value": list(sensor_data["values"])[-1]["value"] if sensor_data["values"] else None
                        }
                        for sensor_id, sensor_data in self.readings_by_sensor.items()
                    }
                }
            }

    def _monitor_network(self):
        """Monitor network and clean up old packets"""
        while True:
            try:
                self._update_interfaces()
                
                # Clean up old packet pairs
                current_time = monotonic()
                with self.metrics_lock:
                    self.packet_pairs = {
                        k: v for k, v in self.packet_pairs.items()
                        if current_time - v['send_time'] < 30  # Remove packets older than 30 seconds
                    }
                
                sleep(1)
            except Exception as e:
                logger.error(f"Error in network monitor: {e}")
                sleep(5)

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.packet_pairs.clear()
            self.completed_packets.clear()
            self.readings_by_sensor.clear()
            self.sensor_intervals.clear()
            self.last_reading_time = None
            self._prev_stats.clear()
            self._update_interfaces()
            logger.info("All sensor metrics have been reset")