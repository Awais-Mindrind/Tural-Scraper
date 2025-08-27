import threading
import time
import queue
import logging
from typing import Dict, Any, Optional
from src.schemas import TaskInfo, TaskQueueItem, ThreadInfo

logger = logging.getLogger(__name__)


class TaskManager:
    """
    Thread-safe task manager for handling scraper tasks
    """
    
    def __init__(self):
        self.tasks: Dict[str, TaskInfo] = {}
        self.lock = threading.Lock()
        self.task_queue = queue.PriorityQueue()
        self.active_threads: Dict[str, ThreadInfo] = {}
        self.thread_lock = threading.Lock()
    
    def add_task(self, task_id: str, task_info: Dict[str, Any]) -> None:
        """Add a new task to the manager"""
        with self.lock:
            self.tasks[task_id] = TaskInfo(**task_info)
            logger.info(f"Task {task_id} added to manager")
    
    def update_task_status(self, task_id: str, status: str, error: Optional[str] = None) -> None:
        """Update the status of a specific task"""
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = status
                
                if status == "running":
                    task.start_time = time.time()
                elif status in ["completed", "failed"]:
                    task.end_time = time.time()
                
                if error:
                    task.error = error
                
                logger.info(f"Task {task_id} status updated to: {status}")
            else:
                logger.warning(f"Attempted to update non-existent task: {task_id}")
    
    def get_task_status(self, task_id: str) -> Optional[TaskInfo]:
        """Get the status of a specific task"""
        with self.lock:
            return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, TaskInfo]:
        """Get all tasks"""
        with self.lock:
            return self.tasks.copy()
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a completed/failed task"""
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                logger.info(f"Task {task_id} removed from manager")
                return True
            return False
    
    def add_to_queue(self, task_id: str, hashtag: str, num_profiles: int, priority: int = 1) -> None:
        """Add a task to the priority queue"""
        queue_item = TaskQueueItem(
            task_id=task_id,
            hashtag=hashtag,
            num_profiles=num_profiles,
            priority=priority
        )
        # Lower priority number = higher priority (queue.get() returns lowest)
        self.task_queue.put((priority, time.time(), queue_item))
        logger.info(f"Task {task_id} added to queue with priority {priority}")
    
    def get_from_queue(self) -> Optional[TaskQueueItem]:
        """Get the next task from the queue"""
        try:
            priority, timestamp, item = self.task_queue.get_nowait()
            logger.debug(f"Retrieved task {item.task_id} from queue")
            return item
        except queue.Empty:
            return None
    
    def queue_size(self) -> int:
        """Get the current queue size"""
        return self.task_queue.qsize()
    
    def add_active_thread(self, task_id: str, thread_name: str) -> None:
        """Track an active thread"""
        with self.thread_lock:
            self.active_threads[task_id] = ThreadInfo(
                task_id=task_id,
                thread_name=thread_name,
                start_time=time.time()
            )
            logger.info(f"Active thread added: {task_id} ({thread_name})")
    
    def remove_active_thread(self, task_id: str) -> None:
        """Remove a completed thread from tracking"""
        with self.thread_lock:
            if task_id in self.active_threads:
                del self.active_threads[task_id]
                logger.info(f"Active thread removed: {task_id}")
    
    def get_active_threads(self) -> Dict[str, ThreadInfo]:
        """Get all active threads"""
        with self.thread_lock:
            return self.active_threads.copy()
    
    def active_thread_count(self) -> int:
        """Get the count of active threads"""
        with self.thread_lock:
            return len(self.active_threads)
    
    def cleanup_old_tasks(self, max_age_hours: int = 24) -> int:
        """Clean up old completed/failed tasks"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        cleaned_count = 0
        
        with self.lock:
            tasks_to_remove = []
            for task_id, task in self.tasks.items():
                if task.status in ["completed", "failed"] and task.end_time:
                    if current_time - task.end_time > max_age_seconds:
                        tasks_to_remove.append(task_id)
            
            for task_id in tasks_to_remove:
                del self.tasks[task_id]
                cleaned_count += 1
        
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old tasks")
        
        return cleaned_count
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        with self.lock:
            total_tasks = len(self.tasks)
            status_counts = {}
            for task in self.tasks.values():
                status_counts[task.status] = status_counts.get(task.status, 0) + 1
            
            return {
                "total_tasks": total_tasks,
                "status_counts": status_counts,
                "queue_size": self.queue_size(),
                "active_threads": self.active_thread_count()
            }


def generate_task_id() -> str:
    """Generate unique task ID"""
    return f"task_{int(time.time() * 1000)}_{threading.get_ident()}"


def create_task_info(hashtag: str, num_profiles: int, source: str, priority: int = 1) -> Dict[str, Any]:
    """Create a task info dictionary"""
    return {
        "hashtag": hashtag,
        "num_profiles": num_profiles,
        "source": source,
        "request_time": time.time(),
        "priority": priority
    }


# Global task manager instance
task_manager = TaskManager()
