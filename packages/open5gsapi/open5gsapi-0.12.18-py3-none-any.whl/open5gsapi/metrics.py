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

logger = logging.getLogger(__name__)

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Basic metrics
        self.packet_sizes = deque(maxlen=window_size)
        self.total_packets = 0
        self.total_bytes = 0
        
        # For latency calculation
        self.send_timestamps = {}  # Store send timestamps by packet id
        self.latencies = deque(maxlen=window_size)
        
        # For jitter calculation using RFC 3550
        self.last_transit = None
        self.jitter = 0
        self.jitters = deque(maxlen=window_size)
        
        # Frame specific metrics
        self.frame_intervals = deque(maxlen=30)
        self.frame_sizes = deque(maxlen=30)
        self.total_frames = 0
        self.total_frames_lost = 0
        self.frames_lost = 0
        self.last_frame_time = None
        self.last_frame_number = 0
        self.last_sequence_number = -1
        self.frame_timestamps = deque(maxlen=30)
        
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
            try:
                # Calculate size
                if isinstance(data, bytes):
                    size = len(data)
                    is_frame = True
                else:
                    size = len(json.dumps(data).encode('utf-8'))
                    is_frame = False

                # Update basic metrics
                self.total_bytes += size
                self.total_packets += 1
                self.packet_sizes.append(size)
                
                # Add timestamp to data for latency calculation
                if isinstance(data, dict):
                    data['_send_timestamp'] = timestamp

                # Handle frame metrics
                if is_frame:
                    self.total_frames += 1
                    self.frame_sizes.append(size)
                    self.frame_timestamps.append(timestamp)
                    
                    if self.last_frame_time is not None:
                        interval = timestamp - self.last_frame_time
                        if interval > 0:
                            self.frame_intervals.append(interval)
                            
                            # Calculate frame loss based on expected rate
                            expected_interval = 1/30.0
                            if interval > expected_interval * 2:
                                estimated_lost_frames = int(interval/expected_interval) - 1
                                self.total_frames_lost += estimated_lost_frames
                    
                    self.last_frame_time = timestamp
                    self.last_frame_number += 1
                
                logger.debug(f"Recorded sent data size: {size} bytes at {timestamp}")
                
            except Exception as e:
                logger.error(f"Error in record_data_sent: {e}")

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            try:
                # Handle frame data
                if isinstance(data, bytes) and data.startswith(b'FRAME:'):
                    try:
                        header_end = data.index(b':', 6)
                        sequence_str = data[6:header_end].decode('utf-8')
                        current_sequence = int(sequence_str)
                        
                        # Sequence-based frame loss detection
                        if self.last_sequence_number >= 0:
                            expected_sequence = self.last_sequence_number + 1
                            if current_sequence > expected_sequence:
                                frames_lost = current_sequence - expected_sequence
                                self.frames_lost += frames_lost
                                self.total_frames_lost += frames_lost
                        
                        self.last_sequence_number = current_sequence
                        size = len(data)
                        
                    except Exception as e:
                        logger.error(f"Error parsing frame sequence: {e}")
                        size = len(data)
                    
                    self.total_frames += 1
                    self.frame_sizes.append(size)
                    self.frame_timestamps.append(timestamp)
                    
                else:
                    # Handle regular data
                    size = len(json.dumps(data).encode('utf-8')) if isinstance(data, dict) else len(data)

                # Update basic metrics
                self.total_bytes += size
                self.total_packets += 1
                self.packet_sizes.append(size)

                # Calculate latency if send timestamp exists
                if isinstance(data, dict) and '_send_timestamp' in data:
                    send_time = float(data['_send_timestamp'])
                    latency = (timestamp - send_time) * 1000  # Convert to ms
                    
                    if 0 < latency < 1000:  # Sanity check
                        self.latencies.append(latency)
                        
                        # Calculate RFC 3550 jitter
                        if self.last_transit is not None:
                            d = abs(latency - self.last_transit)
                            self.jitter += (d - self.jitter) / 16.0
                            self.jitters.append(self.jitter)
                        
                        self.last_transit = latency

                # Update frame intervals
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    if interval > 0:
                        self.frame_intervals.append(interval)
                
                self.last_frame_time = timestamp
                
            except Exception as e:
                logger.error(f"Error in record_data_received: {e}")

    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            try:
                current_time = monotonic()
                elapsed = max(current_time - self.start_time, 0.001)
                
                # Calculate basic metrics
                metrics = {
                    "throughput": {
                        "total_mbps": (self.total_bytes * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
                    },
                    "latency": {
                        "min_ms": min(self.latencies) if self.latencies else 0,
                        "max_ms": max(self.latencies) if self.latencies else 0,
                        "avg_ms": statistics.mean(self.latencies) if self.latencies else 0,
                        "jitter_ms": statistics.mean(self.jitters) if self.jitters else 0
                    }
                }
                
                # Calculate frame-specific metrics
                current_fps = 0
                if self.frame_intervals:
                    current_fps = 1 / statistics.mean(self.frame_intervals)
                
                metrics["frame_metrics"] = {
                    "frame_rate": {
                        "current_fps": current_fps,
                        "frame_time_ms": statistics.mean(self.frame_intervals) * 1000 if self.frame_intervals else 0,
                        "total_frames": self.total_frames,
                        "frames_received": self.total_frames
                    },
                    "frame_size": {
                        "avg_bytes": statistics.mean(self.frame_sizes) if self.frame_sizes else 0,
                        "max_bytes": max(self.frame_sizes) if self.frame_sizes else 0,
                        "min_bytes": min(self.frame_sizes) if self.frame_sizes else 0
                    },
                    "total_frames": self.total_frames,
                    "frames_lost": self.total_frames_lost
                }
                
                metrics["frames"] = {
                    "total": self.total_frames,
                    "received": self.total_frames,
                    "lost": self.total_frames_lost
                }
                
                return metrics
                
            except Exception as e:
                logger.error(f"Error calculating metrics: {e}")
                return self._get_empty_metrics()

    def _get_empty_metrics(self) -> Dict[str, Any]:
        return {
            "throughput": {"total_mbps": 0},
            "latency": {
                "min_ms": 0,
                "max_ms": 0,
                "avg_ms": 0,
                "jitter_ms": 0
            },
            "frame_metrics": {
                "frame_rate": {
                    "current_fps": 0,
                    "frame_time_ms": 0,
                    "total_frames": 0,
                    "frames_received": 0
                },
                "frame_size": {
                    "avg_bytes": 0,
                    "max_bytes": 0,
                    "min_bytes": 0
                },
                "total_frames": 0,
                "frames_lost": 0
            },
            "frames": {
                "total": 0,
                "received": 0,
                "lost": 0
            }
        }

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
            self.packet_sizes.clear()
            self.total_packets = 0
            self.total_bytes = 0
            self.send_timestamps.clear()
            self.latencies.clear()
            self.last_transit = None
            self.jitter = 0
            self.jitters.clear()
            self.frame_intervals.clear()
            self.frame_sizes.clear()
            self.frame_timestamps.clear()
            self.total_frames = 0
            self.total_frames_lost = 0
            self.frames_lost = 0
            self.last_frame_time = None
            self.last_frame_number = 0
            self.last_sequence_number = -1
            self._prev_stats = {}