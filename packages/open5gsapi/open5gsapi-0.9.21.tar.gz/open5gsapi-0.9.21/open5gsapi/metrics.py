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
        self.total_frames = 0
        self.total_frames_lost = 0
        self.last_frame_time = None
        self.last_frame_number = 0
        self.frame_timestamps = deque(maxlen=30)

        # Enhanced frame tracking
        self.expected_frame_count = 0
        self.received_frame_count = 0
        self.frame_sequence_numbers = set()
        self.last_sequence_number = -1
        self.frame_gaps = deque(maxlen=30)  # Track gaps in frame sequences
        
        # Network packet tracking
        self.packets_sent = 0
        self.packets_received = 0
        self.packet_sequence_numbers = set()
        
        # Interface monitoring
        self._interfaces = {}
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
        if len(timestamps) < 2:
            return 0.0
            
        jitter = 0.0
        prev_timestamp = timestamps[0]
        
        for timestamp in list(timestamps)[1:]:
            delay = abs(timestamp - prev_timestamp)
            jitter = jitter + (delay - jitter) / 16
            prev_timestamp = timestamp
            
        return jitter * 1000

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record metrics for sent data with sequence tracking"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            self.total_bytes += size
            self.total_packets += 1
            self.packets_sent += 1
            
            if isinstance(data, bytes):  # Frame data
                self.expected_frame_count += 1
                current_seq = self.expected_frame_count
                
                self.frame_sequence_numbers.add(current_seq)
                self.last_sequence_number = current_seq
                
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    if interval > 0:
                        self.frame_intervals.append(interval)
                
                self.frame_sizes.append(size)
                self.frame_timestamps.append(timestamp)
                self.last_frame_time = timestamp

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record metrics for received data with sequence tracking"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            self.total_bytes += size
            self.total_packets += 1
            self.packets_received += 1
            
            if 'image' in content_type:  # Frame data
                self.received_frame_count += 1
                
                # Calculate gaps in sequence
                if self.last_sequence_number >= 0:
                    expected_seq = self.last_sequence_number + 1
                    actual_seq = self.received_frame_count
                    if actual_seq > expected_seq:
                        gap = actual_seq - expected_seq
                        self.frame_gaps.append(gap)
                
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    if interval > 0:
                        self.frame_intervals.append(interval)
                
                self.frame_sizes.append(size)
                self.frame_timestamps.append(timestamp)
                self.last_frame_time = timestamp

    def calculate_frame_loss_metrics(self) -> Dict[str, Any]:
        """Calculate detailed frame loss metrics"""
        total_expected = self.expected_frame_count
        total_received = self.received_frame_count
        
        frame_loss = total_expected - total_received if total_expected > total_received else 0
        frame_loss_percent = (frame_loss / total_expected * 100) if total_expected > 0 else 0
        
        # Calculate average gap between frames
        avg_gap = statistics.mean(self.frame_gaps) if self.frame_gaps else 0
        
        # Calculate instantaneous frame rate
        current_fps = 0
        if self.frame_intervals:
            avg_interval = statistics.mean(self.frame_intervals)
            if avg_interval > 0:
                current_fps = 1 / avg_interval
        
        return {
            "total_frames_expected": total_expected,
            "total_frames_received": total_received,
            "frames_lost": frame_loss,
            "frame_loss_percent": frame_loss_percent,
            "average_frame_gap": avg_gap,
            "current_fps": current_fps,
            "sequence_discontinuities": len(self.frame_gaps)
        }

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all network metrics"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = current_time - self.start_time
            
            # Get frame loss metrics
            frame_metrics = self.calculate_frame_loss_metrics()
            
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
                },
                "frame_metrics": {
                    "frame_rate": {
                        "current_fps": frame_metrics["current_fps"],
                        "frame_time_ms": statistics.mean(self.frame_intervals) * 1000 if self.frame_intervals else 0
                    },
                    "frame_size": {
                        "avg_bytes": statistics.mean(self.frame_sizes) if self.frame_sizes else 0,
                        "max_bytes": max(self.frame_sizes) if self.frame_sizes else 0,
                        "min_bytes": min(self.frame_sizes) if self.frame_sizes else 0
                    },
                    "frames": {
                        "expected": frame_metrics["total_frames_expected"],
                        "received": frame_metrics["total_frames_received"],
                        "lost": frame_metrics["frames_lost"],
                        "loss_percent": frame_metrics["frame_loss_percent"]
                    },
                    "quality": {
                        "frame_gaps": frame_metrics["average_frame_gap"],
                        "sequence_breaks": frame_metrics["sequence_discontinuities"]
                    }
                }
            }
            
            # Add interface-specific metrics
            self._update_interfaces()
            for iface, data in self._interfaces.items():
                if iface.startswith('uesimtun'):
                    latency = self._measure_interface_latency(iface)
                    if latency > 0:
                        metrics['latency'].update({
                            "min_ms": min(metrics['latency']['min_ms'], latency) if metrics['latency']['min_ms'] > 0 else latency,
                            "max_ms": max(metrics['latency']['max_ms'], latency),
                            "avg_ms": latency if metrics['latency']['avg_ms'] == 0 else (metrics['latency']['avg_ms'] + latency) / 2
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
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.packet_timestamps.clear()
            self.packet_sizes.clear()
            self.total_packets = 0
            self.total_bytes = 0
            self.frame_intervals.clear()
            self.frame_sizes.clear()
            self.frame_timestamps.clear()
            self.total_frames = 0
            self.total_frames_lost = 0
            self.last_frame_time = None
            self.last_frame_number = 0

            self.expected_frame_count = 0
            self.received_frame_count = 0
            self.frame_sequence_numbers.clear()
            self.last_sequence_number = -1
            self.frame_gaps.clear()
            self.packets_sent = 0
            self.packets_received = 0
            self.packet_sequence_numbers.clear()

            self._prev_stats = {}