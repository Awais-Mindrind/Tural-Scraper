from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# PROFILE MODELS
# ------------------------------
class ProfileFilters(BaseModel):
    hashtag: Optional[str] = None
    country: Optional[str] = None
    min_followers: Optional[int] = None
    min_likes: Optional[int] = None
    limit: Optional[int] = 100

class Profile(BaseModel):
    Username: str
    Bio: Optional[str] = None
    Followers: Optional[int] = 0
    Likes: Optional[int] = 0
    Profile_URL: Optional[str] = None
    Image_URL: Optional[str] = None
    Hashtag: str 
    Blacklist: bool = False
    Source: str = "Tiktok"
    Country: Optional[str] = None

class AIQueryRequest(BaseModel):
    query: str

class ScrapeRequest(BaseModel):
    hashtag: str
    num_profiles: Optional[int] = 1000


# API REQUEST/RESPONSE MODELS
# ------------------------------
class ScraperRequest(BaseModel):
    hashtag: Optional[str] = None  # If not provided, will use active hashtags from Airtable
    num_profiles: int = 500
    priority: int = 1  # Higher number = higher priority

class ScraperResponse(BaseModel):
    task_id: str
    message: str
    status: str
    hashtags: List[str] = []

class TaskStatus(BaseModel):
    hashtag: str
    num_profiles: int
    source: str  # 'api' or 'cron'
    status: str  # 'queued', 'running', 'completed', 'failed'
    request_time: float
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[str] = None

class ActiveTasksResponse(BaseModel):
    active_tasks: int
    tasks: Dict[str, TaskStatus]

class ActiveHashtagsResponse(BaseModel):
    hashtags: List[str]
    count: int

class HealthResponse(BaseModel):
    status: str
    active_threads: int
    queue_size: int
    scheduler_running: bool

class LLMQueryResponse(BaseModel):
    filters: ProfileFilters
    query: str
    confidence: float = 1.0


# TASK MANAGEMENT MODELS
# ------------------------------
class TaskInfo(BaseModel):
    hashtag: str
    num_profiles: int
    source: str
    request_time: float
    status: str = "queued"
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[str] = None
    priority: int = 1
    retry_count: int = 0
    max_retries: int = 3

class TaskQueueItem(BaseModel):
    task_id: str
    hashtag: str
    num_profiles: int
    priority: int = 1
    created_at: float = Field(default_factory=lambda: datetime.now().timestamp())

class ThreadInfo(BaseModel):
    task_id: str
    thread_name: str
    start_time: float
    status: str = "running"
