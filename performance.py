"""
Performance Monitoring Module
Tracks system performance metrics and response times
"""

import time
from typing import Dict, Any
from collections import deque
from datetime import datetime

class PerformanceMonitor:
    """Monitor and track system performance"""
    
    def __init__(self, max_samples: int = 100):
        self.max_samples = max_samples
        self.response_times = deque(maxlen=max_samples)
        self.detection_times = deque(maxlen=max_samples)
        self.agent_times = deque(maxlen=max_samples)
        self.extraction_times = deque(maxlen=max_samples)
        self.total_requests = 0
        self.error_count = 0
        self.start_time = datetime.utcnow()
    
    def record_response_time(self, duration: float):
        """Record API response time"""
        self.response_times.append(duration)
        self.total_requests += 1
    
    def record_detection_time(self, duration: float):
        """Record scam detection time"""
        self.detection_times.append(duration)
    
    def record_agent_time(self, duration: float):
        """Record agent response generation time"""
        self.agent_times.append(duration)
    
    def record_extraction_time(self, duration: float):
        """Record intelligence extraction time"""
        self.extraction_times.append(duration)
    
    def record_error(self):
        """Record an error"""
        self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        stats = {
            "uptime_seconds": uptime,
            "total_requests": self.total_requests,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.total_requests, 1),
            "avg_response_time": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            "avg_detection_time": sum(self.detection_times) / len(self.detection_times) if self.detection_times else 0,
            "avg_agent_time": sum(self.agent_times) / len(self.agent_times) if self.agent_times else 0,
            "avg_extraction_time": sum(self.extraction_times) / len(self.extraction_times) if self.extraction_times else 0,
            "requests_per_second": self.total_requests / max(uptime, 1),
        }
        
        return stats

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

