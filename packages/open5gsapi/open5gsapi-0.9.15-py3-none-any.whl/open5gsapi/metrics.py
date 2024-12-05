import socket
import subprocess
from dataclasses import dataclass
from typing import Dict, Any, Optional, Deque, Union, Tuple
from time import time, monotonic
import threading
from collections import deque
import statistics
import logging
import re
import psutil

logger = logging.getLogger(__name__)

@dataclass
class PacketMetrics:
    """Base metrics for any packet"""
    id: int
    size_bytes: int
    timestamp: float
    source_ip: str
    destination_ip: str
    frame_type: Optional[str] = None
    is_frame: bool = False

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Packet metrics with timestamps
        self.packet_timestamps = deque(maxlen=window_size)
        self.packet_sizes = deque(maxlen=window_size)
        self.total_packets = 0
        self.total_bytes = 0
        
        # Frame metrics
        self.frame_intervals = deque(maxlen=30)
        self.frame_sizes = deque(maxlen=30)
        self.last_frame_time = None
        
        # Interface monitoring
        self._interfaces = {}  # Map of interface names to their stats
        self._prev_stats = {}
        self._last_update = monotonic()
        self._update_interfaces()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self._monitor_thread.start()

    def _update_interfaces(self):
        """Update list of monitored interfaces"""
        try:
            interfaces = {}
            # Get all uesimtun interfaces and ogstun
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

    def _get_interface_address(self, iface: str) -> str:
        """Get IP address for interface"""
        try:
            addrs = psutil.net_if_addrs().get(iface, [])
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
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
            # Calculate delay variation
            delay = abs(timestamp - prev_timestamp)
            # Update running jitter calculation
            jitter = jitter + (delay - jitter) / 16
            prev_timestamp = timestamp
            
        return jitter * 1000  # Convert to milliseconds

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record metrics for sent data"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            self.total_bytes += size
            self.total_packets += 1
            self.packet_sizes.append(size)
            self.packet_timestamps.append(timestamp)
            
            if isinstance(data, bytes):  # Frame data
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    self.frame_intervals.append(interval)
                self.last_frame_time = timestamp
                self.frame_sizes.append(size)

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record metrics for received data"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            self.total_bytes += size
            self.total_packets += 1
            self.packet_sizes.append(size)
            self.packet_timestamps.append(timestamp)
            
            if 'image' in content_type:  # Frame data
                self.frame_sizes.append(size)

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all network metrics"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = current_time - self.start_time
            
            # Calculate base metrics
            metrics = {
                "throughput": {
                    "total_mbps": (self.total_bytes * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
                },
                "latency": {
                    "min_ms": 0,
                    "max_ms": 0,
                    "avg_ms": 0,
                    "jitter_ms": self._calculate_jitter(self.packet_timestamps)
                }
            }
            
            # Get interface-specific metrics
            self._update_interfaces()
            for iface, data in self._interfaces.items():
                if iface.startswith('uesimtun'):
                    # Measure latency from UE to UPF
                    latency = self._measure_interface_latency(iface)
                    if latency > 0:
                        metrics['latency'].update({
                            "min_ms": min(metrics['latency']['min_ms'], latency) if metrics['latency']['min_ms'] > 0 else latency,
                            "max_ms": max(metrics['latency']['max_ms'], latency),
                            "avg_ms": latency if metrics['latency']['avg_ms'] == 0 else (metrics['latency']['avg_ms'] + latency) / 2
                        })
            
            # Add frame metrics if available
            if self.frame_intervals:
                metrics["frame_metrics"] = {
                    "frame_rate": {
                        "current_fps": 1 / statistics.mean(self.frame_intervals) if self.frame_intervals else 0,
                        "frame_time_ms": statistics.mean(self.frame_intervals) * 1000 if self.frame_intervals else 0
                    },
                    "frame_size": {
                        "avg_bytes": statistics.mean(self.frame_sizes) if self.frame_sizes else 0,
                        "max_bytes": max(self.frame_sizes) if self.frame_sizes else 0,
                        "min_bytes": min(self.frame_sizes) if self.frame_sizes else 0
                    }
                }
            
            return metrics

    def _measure_interface_latency(self, interface: str) -> float:
        """Measure latency from specific interface to UPF"""
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
        """Monitor network interfaces in background"""
        while True:
            try:
                self._update_interfaces()
                time.sleep(1)  # Update every second
            except Exception as e:
                logger.error(f"Error in network monitor: {e}")
                time.sleep(5)  # Wait longer on error

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.packet_timestamps.clear()
            self.packet_sizes.clear()
            self.total_packets = 0
            self.total_bytes = 0
            self.frame_intervals.clear()
            self.frame_sizes.clear()
            self.last_frame_time = None
            self._prev_stats = {}