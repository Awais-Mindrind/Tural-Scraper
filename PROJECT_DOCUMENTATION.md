# TikTok Scraper - Complete Project Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [API Reference](#api-reference)
6. [Core Components](#core-components)
7. [Task Management System](#task-management-system)
8. [LLM Integration](#llm-integration)
9. [Airtable Integration](#airtable-integration)
10. [Scraping Engine](#scraping-engine)
11. [Cron Jobs & Scheduling](#cron-jobs--scheduling)
12. [Monitoring & Logging](#monitoring--logging)
13. [Error Handling](#error-handling)
14. [Testing](#testing)
15. [Deployment](#deployment)
16. [Troubleshooting](#troubleshooting)
17. [API Examples](#api-examples)
18. [Development Guide](#development-guide)

---

## 🚀 Project Overview

The TikTok Scraper is a comprehensive, production-ready system designed to automatically collect TikTok profile data at scale. It features a modular architecture with multithreaded execution, intelligent task management, and LLM-powered natural language query processing.

**Total API Endpoints: 16** - Providing complete coverage of scraping, profile management, and system operations.

### **Key Features**
- **Multithreaded Scraping**: Concurrent execution of multiple scraping tasks
- **LLM Integration**: Natural language query processing using Google Gemini
- **Airtable Integration**: Dynamic hashtag management and data storage
- **Task Management**: Priority-based queuing and status tracking
- **Automated Scheduling**: Cron-based execution and monitoring
- **Comprehensive Logging**: Detailed tracking and debugging capabilities
- **RESTful API**: Full HTTP interface for all operations
- **Health Monitoring**: Real-time system status and performance metrics
- **Profile Management**: Advanced filtering, search, and analytics
- **AI-Powered Search**: Natural language profile queries and intelligent filtering

### **Use Cases**
- **Influencer Research**: Find and analyze TikTok profiles by category
- **Market Analysis**: Collect demographic and engagement data
- **Content Strategy**: Identify trending hashtags and content types
- **Competitive Intelligence**: Monitor competitor profiles and strategies
- **Data Collection**: Bulk profile data extraction for analysis
- **Profile Analytics**: Comprehensive statistics and insights from collected data
- **Intelligent Search**: Natural language queries for finding specific profile types
- **Data Mining**: Advanced filtering and search across large profile datasets

---

## 🏗️ System Architecture

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TikTok Scraper System                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────────────┐ │
│  │   Client    │    │   Cron      │    │        External Systems         │ │
│  │   Apps      │    │  Scheduler  │    │                                 │ │
│  └─────┬───────┘    └─────┬───────┘    │  ┌─────────────┐ ┌─────────────┐ │
│        │                  │            │  │  Airtable   │ │   Google    │ │
│        │                  │            │  │  Database   │ │   Gemini    │ │
│        │                  │            │  └─────────────┘ └─────────────┘ │
│        │                  │            └─────────────────────────────────┘ │
│        │                  │                              │                 │
│        ▼                  ▼                              ▼                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        FastAPI Application                             │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────────────┐  │ │
│  │  │    API      │ │   Task      │ │         Queue Processor         │  │ │
│  │  │ Endpoints   │ │  Manager    │ │                                 │  │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    Multithreaded Scraping Engine                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────────────┐  │ │
│  │  │  Thread 1   │ │  Thread 2   │ │            Thread N             │  │ │
│  │  │ (Hashtag A) │ │ (Hashtag B) │ │         (Hashtag N)             │  │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           Data Storage                                 │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────────────┐  │ │
│  │  │  Airtable   │ │   Logs      │ │         Local Cache             │  │ │
│  │  │  Profiles   │ │  Files      │ │         & Temp Data             │  │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────────────────┘  │ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **Component Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              File Structure                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📁 schemas.py              # Data models and validation                  │
│  📁 task_manager.py         # Task management and threading               │
│  📁 api.py                  # FastAPI endpoints and LLM integration       │
│  📁 triggers.py             # Cron jobs and system orchestration         │
│  📁 airtable.py            # Airtable integration                        │
│  📁 tikTok_Scraper.py      # Core scraping functionality                 │
│  📁 llm_query.py           # LLM query processing                        │
│  📁 utils.py               # Utility functions                           │
│  📁 test_triggers.py       # Comprehensive test suite                    │
│  📁 requirements.txt       # Python dependencies                          │
│  📁 .env                   # Environment configuration                    │
│  📁 scraper_logs.log       # Application logs                            │
│  📁 MULTITHREADED_README.md # User documentation                         │
│  📁 PROJECT_DOCUMENTATION.md # This comprehensive documentation          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation & Setup

### **Prerequisites**

- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- Airtable account with Personal Access Token
- Google Gemini API key (for LLM features)

### **1. Clone Repository**

```bash
git clone <repository-url>
cd TikTok-Scraper
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Environment Configuration**

Create a `.env` file in the project root:

```env
# Airtable Configuration
AIRTABLE_PAT=your_airtable_personal_access_token
AIRTABLE_BASE_ID=your_base_id

# Google Gemini API (for LLM features)
GOOGLE_API_KEY=your_google_gemini_api_key

# Proxy Configuration (optional)
PROXY=http://username:password@proxyserver:port

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=scraper_logs.log

# System Configuration
MAX_CONCURRENT_THREADS=3
DEFAULT_PROFILES_PER_HASHTAG=500
```

### **4. Airtable Setup**

1. Create a new base in Airtable
2. Create a table named `hashtags` with columns:
   - **Hashtag** (Single line text): The hashtag or category
   - **Active** (Checkbox): Whether this hashtag should be scraped
3. Create a table named `tiktok` for storing scraped profiles
4. Note your Base ID from the URL

### **5. Verify Installation**

```bash
python test_triggers.py
```

---

## ⚙️ Configuration

### **System Configuration**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_CONCURRENT_THREADS` | 3 | Maximum concurrent scraping threads |
| `DEFAULT_PROFILES_PER_HASHTAG` | 500 | Default profiles to scrape per hashtag |
| `LOG_LEVEL` | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | scraper_logs.log | Log file path |

### **Scraping Configuration**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SCROLL_PAUSE` | (2, 4) | Random pause between scrolls (seconds) |
| `DRIVER_TIMEOUT` | 10 | Selenium driver timeout (seconds) |
| `HEADLESS_MODE` | False | Run browser in headless mode |

### **Cron Job Configuration**

| Job | Frequency | Description |
|-----|-----------|-------------|
| Daily Scraping | Every 24 hours | Scrape all active hashtags |
| Task Cleanup | Every 6 hours | Remove old completed tasks |
| Health Monitoring | Every 30 minutes | System health checks |

---

## 📡 API Reference

### **Base URL**
```
http://localhost:5000
```

### **Authentication**
Currently, the API doesn't require authentication. For production use, consider implementing API keys or OAuth.

### **Response Format**
All API responses follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### **Error Responses**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": { ... }
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## 📋 Complete API Endpoints Summary

| Category | Endpoint | Method | Description |
|----------|----------|---------|-------------|
| **Scraping** | `/start-scraper` | POST | Start scraping for specific hashtag |
| **Scraping** | `/start-scraper-with-llm` | POST | Start scraping using LLM query |
| **LLM** | `/llm-query` | POST | Process natural language queries |
| **Profiles** | `/profiles` | GET | Retrieve profiles with filters |
| **Profiles** | `/profiles/ai` | POST | AI-powered profile search |
| **Profiles** | `/profiles/stats` | GET | Profile statistics and analytics |
| **Profiles** | `/profiles/search` | GET | Advanced text-based search |
| **Tasks** | `/task-status/{task_id}` | GET | Get task status |
| **Tasks** | `/active-tasks` | GET | List active tasks |
| **Tasks** | `/task/{task_id}` | DELETE | Cancel task |
| **System** | `/health` | GET | System health check |
| **System** | `/active-hashtags` | GET | Get active hashtags |
| **System** | `/task-statistics` | GET | Task performance metrics |
| **System** | `/cleanup-tasks` | POST | Clean up old tasks |
| **System** | `/` | GET | API information and endpoints |

---

## 🔌 Core Components

### **1. Data Models (`schemas.py`)**

#### **Profile Models**
```python
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

class ProfileFilters(BaseModel):
    hashtag: Optional[str] = None
    country: Optional[str] = None
    min_followers: Optional[int] = None
    min_likes: Optional[int] = None
    limit: Optional[int] = 100
```

#### **API Models**
```python
class ScraperRequest(BaseModel):
    hashtag: Optional[str] = None
    num_profiles: int = 500
    priority: int = 1

class ScraperResponse(BaseModel):
    task_id: str
    message: str
    status: str
    hashtags: List[str] = []

class TaskStatus(BaseModel):
    hashtag: str
    num_profiles: int
    source: str
    status: str
    request_time: float
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[str] = None
```

#### **LLM Models**
```python
class AIQueryRequest(BaseModel):
    query: str

class LLMQueryResponse(BaseModel):
    filters: ProfileFilters
    query: str
    confidence: float = 1.0
```

### **2. Task Management (`task_manager.py`)**

#### **TaskManager Class**
```python
class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, TaskInfo] = {}
        self.lock = threading.Lock()
        self.task_queue = queue.PriorityQueue()
        self.active_threads: Dict[str, ThreadInfo] = {}
        self.thread_lock = threading.Lock()
    
    def add_task(self, task_id: str, task_info: Dict[str, Any]) -> None
    def update_task_status(self, task_id: str, status: str, error: Optional[str] = None) -> None
    def get_task_status(self, task_id: str) -> Optional[TaskInfo]
    def add_to_queue(self, task_id: str, hashtag: str, num_profiles: int, priority: int = 1) -> None
    def get_from_queue(self) -> Optional[TaskQueueItem]
    def add_active_thread(self, task_id: str, thread_name: str) -> None
    def remove_active_thread(self, task_id: str) -> None
    def cleanup_old_tasks(self, max_age_hours: int = 24) -> int
    def get_task_statistics(self) -> Dict[str, Any]
```

#### **Utility Functions**
```python
def generate_task_id() -> str
def create_task_info(hashtag: str, num_profiles: int, source: str, priority: int = 1) -> Dict[str, Any]
```

### **3. API Endpoints (`api.py`)**

#### **Scraper Endpoints**
```python
@app.post("/start-scraper")
@app.post("/start-scraper-with-llm")
@app.get("/task-status/{task_id}")
@app.get("/active-tasks")
@app.delete("/task/{task_id}")
```

#### **LLM Endpoints**
```python
@app.post("/llm-query")
```

#### **Profile Management Endpoints**
```python
@app.get("/profiles")
@app.post("/profiles/ai")
@app.get("/profiles/stats")
@app.get("/profiles/search")
```

#### **System Endpoints**
```python
@app.get("/health")
@app.get("/active-hashtags")
@app.get("/task-statistics")
@app.post("/cleanup-tasks")
@app.get("/")
```

### **4. Scraping Engine (`tikTok_Scraper.py`)**

#### **Core Functions**
```python
def get_driver() -> Driver
def human_sleep(min_s: float, max_s: float) -> None
def extract_username_from_url(url: str) -> Optional[str]
def generate_country_hashtags(base_hashtag: str) -> List[Tuple[str, str]]
def get_unique_profiles_via_videos(driver: Driver, hashtag: str, num_profiles: int, profile_urls: List[Dict], country: str) -> None
def scrape_tiktok_profiles(base_hashtag: str = BASE_HASHTAG, num_profiles: int = NUM_PROFILES) -> None
```

#### **Scraping Process**
1. **Profile Collection**: Browse hashtag pages to collect profile URLs
2. **Data Extraction**: Visit individual profiles to extract data
3. **Data Storage**: Save profiles to Airtable
4. **Progress Tracking**: Log progress and handle errors

### **5. LLM Integration (`llm_query.py`)**

#### **Core Functionality**
```python
def parse_query_to_filters(query: str) -> ProfileFilters
```

#### **LLM Configuration**
- **Model**: Google Gemini 2.5 Flash
- **Temperature**: 0 (deterministic output)
- **Output Format**: Structured JSON matching ProfileFilters schema

#### **Query Examples**
```
Input: "Find travel influencers with more than 50k followers from USA"
Output: {
  "hashtag": "travel",
  "country": "USA",
  "min_followers": 50000,
  "min_likes": null,
  "limit": 100
}
```

### **6. Airtable Integration (`airtable.py`)**

#### **Core Functions**
```python
def get_active_hashtags() -> List[str]
def save_profile_to_airtable(profile_data: dict) -> Optional[Any]
def get_existing_usernames() -> List[str]
```

#### **Table Structure**
- **hashtags**: Manages active hashtags for scraping
- **tiktok**: Stores scraped profile data

---

## 🔄 Task Management System

### **Task Lifecycle**

```
1. Task Creation → 2. Queue Addition → 3. Thread Assignment → 4. Execution → 5. Completion
     ↓                    ↓                ↓              ↓           ↓
  API/Cron           Priority Queue    Worker Thread   Scraping    Status Update
```

### **Task States**

| State | Description | Actions Available |
|-------|-------------|-------------------|
| `queued` | Task is waiting in queue | Cancel, Monitor |
| `running` | Task is currently executing | Monitor, Cancel |
| `completed` | Task finished successfully | View Results, Cleanup |
| `failed` | Task encountered an error | View Error, Retry |
| `cancelled` | Task was cancelled | None |

### **Priority System**

- **Priority 1**: High priority (processed first)
- **Priority 2**: Normal priority
- **Priority 3**: Low priority (processed last)

### **Thread Management**

- **Maximum Concurrent Threads**: Configurable (default: 3)
- **Thread Naming**: `Scraper-{task_id}`
- **Thread Cleanup**: Automatic cleanup on completion
- **Resource Management**: Proper driver cleanup

---

## 🤖 LLM Integration

### **Natural Language Processing**

The system can understand and process queries like:

```
"Find travel influencers with more than 50k followers from USA"
"Show me food bloggers with high engagement"
"Get fitness profiles from Europe with at least 1000 likes"
"Find gaming content creators in Japan"
```

### **Filter Extraction**

The LLM automatically extracts:

- **Hashtags**: Primary content category
- **Geographic Location**: Country/region preferences
- **Engagement Metrics**: Follower/like requirements
- **Content Type**: Specific content categories
- **Limits**: Number of profiles to return

### **Fallback Handling**

If LLM processing fails:
1. Use default hashtag "general"
2. Log error for debugging
3. Continue with basic scraping
4. Return error response to client

---

## 📊 Airtable Integration

### **Table Schemas**

#### **hashtags Table**
| Field | Type | Description |
|-------|------|-------------|
| Hashtag | Single line text | The hashtag or category |
| Active | Checkbox | Whether to scrape this hashtag |

#### **tiktok Table**
| Field | Type | Description |
|-------|------|-------------|
| Username | Single line text | TikTok username |
| Bio | Long text | Profile bio |
| Followers | Number | Follower count |
| Likes | Number | Total likes |
| Profile URL | URL | Profile URL |
| Image URL | URL | Profile image |
| Hashtag | Single line text | Source hashtag |
| Blacklist | Checkbox | Whether to exclude |
| Source | Single line text | Data source |
| Country | Single line text | Geographic location |

### **Data Operations**

- **Read**: Fetch active hashtags for scraping
- **Write**: Save scraped profile data
- **Update**: Modify existing profiles
- **Delete**: Remove outdated data

---

## 🕷️ Scraping Engine

### **Scraping Strategy**

#### **Phase 1: Profile Collection**
1. Navigate to hashtag page
2. Scroll through videos to find profile links
3. Extract unique profile URLs
4. Continue until target count reached

#### **Phase 2: Data Extraction**
1. Visit each profile URL
2. Extract profile information:
   - Username
   - Bio
   - Follower count
   - Like count
   - Profile image
3. Handle missing data gracefully
4. Skip already processed profiles

### **Anti-Detection Measures**

- **Random Delays**: Human-like timing between actions
- **User-Agent Rotation**: Different browser configurations
- **Proxy Support**: Optional proxy rotation
- **Incognito Mode**: Clean browser sessions
- **Scroll Simulation**: Natural scrolling behavior

### **Error Handling**

- **Network Errors**: Retry with exponential backoff
- **Element Not Found**: Skip and continue
- **Rate Limiting**: Pause and resume
- **Browser Crashes**: Restart driver and continue

---

## ⏰ Cron Jobs & Scheduling

### **Scheduled Jobs**

#### **Daily Scraping (Every 24 hours)**
```python
def run_cron_job():
    # Fetch active hashtags from Airtable
    # Queue scraping tasks for each hashtag
    # Log completion status
```

#### **Task Cleanup (Every 6 hours)**
```python
def cleanup_old_tasks():
    # Remove completed/failed tasks older than 24 hours
    # Log cleanup statistics
```

#### **Health Monitoring (Every 30 minutes)**
```python
def health_monitor():
    # Check system health
    # Log performance metrics
    # Alert on long-running tasks
```

### **Scheduler Configuration**

```python
scheduler = BackgroundScheduler()
scheduler.add_job(run_cron_job, IntervalTrigger(hours=24), id="daily_scraping")
scheduler.add_job(cleanup_old_tasks, IntervalTrigger(hours=6), id="cleanup_tasks")
scheduler.add_job(health_monitor, IntervalTrigger(minutes=30), id="health_monitor")
```

---

## 📊 Monitoring & Logging

### **Logging Configuration**

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_logs.log"),
        logging.StreamHandler()
    ]
)
```

### **Log Levels**

| Level | Description | Use Case |
|-------|-------------|----------|
| `DEBUG` | Detailed debugging information | Development and troubleshooting |
| `INFO` | General information messages | Normal operation tracking |
| `WARNING` | Warning messages | Potential issues |
| `ERROR` | Error messages | Operation failures |
| `CRITICAL` | Critical errors | System failures |

### **Log Categories**

- **System**: Startup, shutdown, configuration
- **API**: Request/response logging
- **Tasks**: Task creation, execution, completion
- **Scraping**: Profile collection and data extraction
- **LLM**: Query processing and responses
- **Airtable**: Database operations
- **Threading**: Thread management and status

### **Performance Metrics**

The system tracks:
- Task execution time
- Success/failure rates
- Thread utilization
- Queue performance
- Memory usage
- API response times

---

## 🚨 Error Handling

### **Error Categories**

#### **System Errors**
- **Configuration Errors**: Missing environment variables
- **Initialization Errors**: Failed component startup
- **Resource Errors**: Memory, disk space issues

#### **API Errors**
- **Validation Errors**: Invalid request data
- **Processing Errors**: Internal processing failures
- **External Errors**: Airtable, LLM API failures

#### **Scraping Errors**
- **Network Errors**: Connection timeouts, failures
- **Browser Errors**: Driver crashes, element not found
- **Data Errors**: Invalid data format, parsing failures

### **Error Recovery**

#### **Automatic Recovery**
- **Retry Logic**: Exponential backoff for transient errors
- **Fallback Mechanisms**: Alternative processing paths
- **Resource Cleanup**: Automatic cleanup on failures

#### **Manual Recovery**
- **Task Cancellation**: Cancel problematic tasks
- **System Restart**: Restart failed components
- **Data Recovery**: Restore from backups

### **Error Reporting**

- **Detailed Logging**: Full error context and stack traces
- **Status Updates**: Real-time error status
- **Alerting**: Notifications for critical errors
- **Metrics**: Error rate tracking and analysis

---

## 🧪 Testing

### **Test Suite Structure**

```python
def test_schemas()           # Data model validation
def test_task_manager()      # Task management functionality
def test_llm_integration()   # LLM query processing
def test_airtable_integration() # Airtable operations
def test_api_endpoints()     # API functionality
```

### **Running Tests**

```bash
# Run all tests
python test_triggers.py

# Run specific test (modify test file)
python -c "from test_triggers import test_schemas; test_schemas()"
```

### **Test Coverage**

- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **API Tests**: Endpoint functionality testing (16 endpoints covered)
- **End-to-End Tests**: Complete workflow testing
- **Profile Management Tests**: Profile filtering, search, and analytics
- **LLM Integration Tests**: Natural language query processing

### **Mocking & Stubbing**

- **External APIs**: Mock Airtable and LLM responses
- **Browser**: Mock Selenium driver
- **Time**: Mock time-based operations
- **Network**: Mock network requests

---

## 🚀 Deployment

### **Development Deployment**

```bash
# Start development server
python triggers.py

# Server runs on http://localhost:5000
# Logs written to scraper_logs.log
# Cron jobs start automatically
```

### **Production Deployment**

#### **Option 1: Direct Python**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AIRTABLE_PAT="your_token"
export GOOGLE_API_KEY="your_key"

# Start server
python triggers.py
```

#### **Option 2: Gunicorn (Recommended)**
```bash
# Install gunicorn
pip install gunicorn

# Start with gunicorn
gunicorn -w 1 -k uvicorn.workers.UvicornWorker triggers:app --bind 0.0.0.0:5000
```

#### **Option 3: Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "triggers.py"]
```

### **Environment Configuration**

#### **Development**
```env
LOG_LEVEL=DEBUG
MAX_CONCURRENT_THREADS=2
```

#### **Production**
```env
LOG_LEVEL=INFO
MAX_CONCURRENT_THREADS=5
HEADLESS_MODE=true
```

### **Process Management**

#### **Systemd Service**
```ini
[Unit]
Description=TikTok Scraper Service
After=network.target

[Service]
Type=simple
User=scraper
WorkingDirectory=/opt/tiktok-scraper
Environment=PATH=/opt/tiktok-scraper/venv/bin
ExecStart=/opt/tiktok-scraper/venv/bin/python triggers.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **Supervisor**
```ini
[program:tiktok-scraper]
command=/opt/tiktok-scraper/venv/bin/python triggers.py
directory=/opt/tiktok-scraper
user=scraper
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/tiktok-scraper.log
```

---

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Airtable Connection Issues**
```bash
# Check environment variable
echo $AIRTABLE_PAT

# Verify table structure
# Check base ID in airtable.py
```

#### **2. LLM API Issues**
```bash
# Check Google API key
echo $GOOGLE_API_KEY

# Verify API quota
# Check internet connectivity
```

#### **3. Scraping Failures**
```bash
# Check logs
tail -f scraper_logs.log

# Verify Chrome installation
# Check proxy settings
```

#### **4. Thread Management Issues**
```bash
# Check thread count
curl http://localhost:5000/health

# Monitor active tasks
curl http://localhost:5000/active-tasks
```

### **Debug Mode**

Enable debug logging in any component:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Performance Tuning**

#### **Thread Optimization**
```python
# Adjust based on system resources
MAX_CONCURRENT_THREADS = 3  # Increase for more powerful systems
```

#### **Memory Management**
```python
# Regular cleanup of old tasks
CLEANUP_INTERVAL_HOURS = 6
MAX_TASK_AGE_HOURS = 24
```

#### **Network Optimization**
```python
# Adjust timeouts
DRIVER_TIMEOUT = 10
SCROLL_PAUSE = (2, 4)
```

---

## 📚 API Examples

### **Basic Scraping**

#### **Start Scraper for Specific Hashtag**
```bash
curl -X POST http://localhost:5000/start-scraper \
  -H "Content-Type: application/json" \
  -d '{
    "hashtag": "travel",
    "num_profiles": 100,
    "priority": 1
  }'
```

**Response:**
```json
{
  "task_id": "task_1704067200000_12345",
  "message": "Scraper task queued for hashtag: travel",
  "status": "queued",
  "hashtags": ["travel"]
}
```

#### **Start Scraper with Active Hashtags**
```bash
curl -X POST http://localhost:5000/start-scraper \
  -H "Content-Type: application/json" \
  -d '{
    "num_profiles": 500
  }'
```

### **LLM Integration**

#### **Process Natural Language Query**
```bash
curl -X POST http://localhost:5000/llm-query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find food bloggers from USA with more than 10k followers"
  }'
```

**Response:**
```json
{
  "filters": {
    "hashtag": "food",
    "country": "USA",
    "min_followers": 10000,
    "min_likes": null,
    "limit": 100
  },
  "query": "Find food bloggers from USA with more than 10k followers",
  "confidence": 1.0
}
```

#### **Start Scraper with LLM Query**
```bash
curl -X POST http://localhost:5000/start-scraper-with-llm \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find gaming content creators in Japan"
  }' \
  -G -d "num_profiles=200"
```

### **Profile Management**

#### **Get Profiles with Filters**
```bash
curl "http://localhost:5000/profiles?hashtag=travel&country=USA&min_followers=10000&limit=100"
```

**Response:**
```json
{
  "success": true,
  "count": 45,
  "data": [
    {
      "Username": "traveler123",
      "Bio": "Adventure seeker",
      "Followers": 15000,
      "Likes": 2500,
      "Hashtag": "travel",
      "Country": "USA"
    }
  ],
  "filters": {
    "hashtag": "travel",
    "country": "USA",
    "min_followers": 10000,
    "min_likes": null,
    "limit": 100
  }
}
```

#### **AI-Powered Profile Search**
```bash
curl -X POST "http://localhost:5000/profiles/ai" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find food bloggers from USA with more than 10k followers"
  }'
```

**Response:**
```json
{
  "success": true,
  "query": "Find food bloggers from USA with more than 10k followers",
  "filters": {
    "hashtag": "food",
    "country": "USA",
    "min_followers": 10000,
    "min_likes": null,
    "limit": 100
  },
  "count": 23,
  "data": [...],
  "formula": "AND(SEARCH('food', LOWER({Hashtag})), {Country} = 'USA', {Followers} >= 10000)"
}
```

#### **Get Profile Statistics**
```bash
curl "http://localhost:5000/profiles/stats"
```

**Response:**
```json
{
  "success": true,
  "total_profiles": 1250,
  "statistics": {
    "hashtag_distribution": {
      "travel": 450,
      "food": 320,
      "fitness": 280,
      "gaming": 200
    },
    "country_distribution": {
      "USA": 600,
      "UK": 200,
      "Canada": 150,
      "Australia": 100
    },
    "follower_ranges": {
      "0-1K": 100,
      "1K-10K": 300,
      "10K-100K": 500,
      "100K-1M": 300,
      "1M+": 50
    },
    "top_hashtags": [
      ["travel", 450],
      ["food", 320],
      ["fitness", 280]
    ],
    "top_countries": [
      ["USA", 600],
      ["UK", 200],
      ["Canada", 150]
    ]
  }
}
```

#### **Advanced Profile Search**
```bash
curl "http://localhost:5000/profiles/search?q=travel&limit=20"
```

**Response:**
```json
{
  "success": true,
  "query": "travel",
  "count": 15,
  "data": [...],
  "search_formula": "OR(SEARCH('travel', LOWER({Username})), SEARCH('travel', LOWER({Bio})), SEARCH('travel', LOWER({Hashtag})))"
}
```

### **System Information**

#### **Get API Information**
```bash
curl "http://localhost:5000/"
```

**Response:**
```json
{
  "message": "TikTok Scraper API",
  "version": "2.0.0",
  "features": [
    "Multithreaded scraping",
    "LLM query processing",
    "Task management",
    "Airtable integration",
    "Health monitoring"
  ],
  "endpoints": [
    "POST /start-scraper",
    "POST /llm-query",
    "POST /start-scraper-with-llm",
    "GET /task-status/{task_id}",
    "GET /active-tasks",
    "GET /active-hashtags",
    "GET /health",
    "GET /task-statistics",
    "GET /profiles",
    "POST /profiles/ai",
    "GET /profiles/stats",
    "GET /profiles/search"
  ]
}
```

### **Task Management**

#### **Get Task Status**
```bash
curl http://localhost:5000/task-status/task_1704067200000_12345
```

**Response:**
```json
{
  "hashtag": "travel",
  "num_profiles": 100,
  "source": "api",
  "status": "running",
  "request_time": 1704067200.0,
  "start_time": 1704067205.0,
  "end_time": null,
  "error": null
}
```

#### **Get Active Tasks**
```bash
curl http://localhost:5000/active-tasks
```

**Response:**
```json
{
  "active_tasks": 2,
  "tasks": {
    "task_1704067200000_12345": {
      "hashtag": "travel",
      "num_profiles": 100,
      "source": "api",
      "status": "running",
      "request_time": 1704067200.0,
      "start_time": 1704067205.0,
      "end_time": null,
      "error": null
    }
  }
}
```

#### **Cancel Task**
```bash
curl -X DELETE http://localhost:5000/task/task_1704067200000_12345
```

**Response:**
```json
{
  "success": true,
  "message": "Task task_1704067200000_12345 marked as cancelled",
  "task_id": "task_1704067200000_12345"
}
```

### **System Monitoring**

#### **Health Check**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "active_threads": 2,
  "queue_size": 1,
  "scheduler_running": true
}
```

#### **Task Statistics**
```bash
curl http://localhost:5000/task-statistics
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_tasks": 15,
    "status_counts": {
      "completed": 10,
      "running": 2,
      "queued": 1,
      "failed": 2
    },
    "queue_size": 1,
    "active_threads": 2
  },
  "timestamp": 1704067200.0
}
```

#### **Active Hashtags**
```bash
curl http://localhost:5000/active-hashtags
```

**Response:**
```json
{
  "hashtags": ["travel", "food", "fitness", "gaming"],
  "count": 4
}
```

### **Maintenance Operations**

#### **Cleanup Old Tasks**
```bash
curl -X POST http://localhost:5000/cleanup-tasks?max_age_hours=24
```

**Response:**
```json
{
  "success": true,
  "message": "Cleaned up 5 old tasks",
  "cleaned_count": 5,
  "max_age_hours": 24
}
```

---

## 👨‍💻 Development Guide

### **Adding New Endpoints**

1. **Define Schema** in `schemas.py`:
```python
class NewRequest(BaseModel):
    field1: str
    field2: Optional[int] = None

class NewResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
```

2. **Add Endpoint** in `api.py`:
```python
@app.post("/new-endpoint", response_model=NewResponse)
async def new_endpoint(request: NewRequest):
    try:
        # Implementation logic
        return NewResponse(success=True, data={...})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

3. **Add Test** in `test_triggers.py`:
```python
def test_new_endpoint():
    # Test implementation
    pass
```

### **Adding New Task Types**

1. **Extend TaskInfo** in `schemas.py`:
```python
class TaskInfo(BaseModel):
    # ... existing fields ...
    task_type: str = "scraping"  # New field
```

2. **Update TaskManager** in `task_manager.py`:
```python
def process_task_type(self, task_type: str, task_data: Dict):
    if task_type == "new_type":
        return self.process_new_type(task_data)
    # ... existing logic ...
```

3. **Add Worker Function** in `api.py`:
```python
def new_type_worker(task_id: str, data: Dict):
    # Implementation
    pass
```

### **Adding New Data Sources**

1. **Create Integration Module**:
```python
# new_source.py
def fetch_data_from_source(config: Dict) -> List[Dict]:
    # Implementation
    pass
```

2. **Add to API**:
```python
@app.post("/fetch-from-new-source")
async def fetch_from_new_source(config: Dict):
    data = fetch_data_from_source(config)
    return {"data": data}
```

### **Performance Optimization**

#### **Threading Optimization**
```python
# Adjust based on system capabilities
MAX_CONCURRENT_THREADS = min(os.cpu_count(), 8)
```

#### **Memory Management**
```python
# Regular cleanup
import gc
gc.collect()
```

#### **Caching**
```python
# Add caching for frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_data(key: str):
    return expensive_operation(key)
```

---

## 📈 Performance Metrics

### **Key Performance Indicators (KPIs)**

| Metric | Description | Target | Monitoring |
|--------|-------------|--------|------------|
| **Task Throughput** | Tasks completed per hour | >100 | Real-time dashboard |
| **Success Rate** | Percentage of successful tasks | >95% | Daily reports |
| **Response Time** | API response time | <500ms | Performance monitoring |
| **Thread Utilization** | Active thread percentage | 70-90% | System monitoring |
| **Memory Usage** | Memory consumption | <2GB | Resource monitoring |

### **Monitoring Dashboard**

#### **Real-Time Metrics**
- Active task count
- Queue size
- Thread utilization
- System health status

#### **Historical Data**
- Task completion rates
- Performance trends
- Error patterns
- Resource usage

### **Alerting**

#### **Critical Alerts**
- System down
- High error rate
- Resource exhaustion
- Task queue overflow

#### **Warning Alerts**
- Performance degradation
- High memory usage
- Long-running tasks
- Low success rate

---

## 🔒 Security Considerations

### **API Security**

#### **Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/start-scraper")
@limiter.limit("10/minute")
async def start_scraper(request: ScraperRequest):
    # Implementation
    pass
```

#### **Input Validation**
```python
from pydantic import validator

class ScraperRequest(BaseModel):
    hashtag: str
    num_profiles: int
    
    @validator('hashtag')
    def validate_hashtag(cls, v):
        if not v.isalnum() and not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Invalid hashtag format')
        return v.lower()
    
    @validator('num_profiles')
    def validate_num_profiles(cls, v):
        if v < 1 or v > 10000:
            raise ValueError('Number of profiles must be between 1 and 10000')
        return v
```

### **Data Security**

#### **Environment Variables**
```bash
# Use secure environment variable management
export AIRTABLE_PAT="$(gpg --decrypt token.gpg)"
```

#### **Data Encryption**
```python
import cryptography.fernet

def encrypt_sensitive_data(data: str) -> bytes:
    key = cryptography.fernet.Fernet.generate_key()
    f = cryptography.fernet.Fernet(key)
    return f.encrypt(data.encode())
```

---

## 🔮 Future Enhancements

### **Short Term (1-3 months)**

- **Advanced LLM Models**: Support for multiple LLM providers
- **Enhanced Filtering**: More sophisticated profile filtering
- **Batch Processing**: Group similar tasks for efficiency
- **Real-time Notifications**: Webhook support for task updates

### **Medium Term (3-6 months)**

- **Web Dashboard**: Visual interface for monitoring and control
- **Advanced Analytics**: Data visualization and insights
- **Multi-platform Support**: Instagram, YouTube, Twitter scraping
- **Machine Learning**: Predictive analytics for trending content

### **Long Term (6+ months)**

- **Distributed Architecture**: Multi-server deployment
- **Cloud Integration**: AWS, GCP, Azure support
- **Mobile App**: iOS/Android applications
- **Enterprise Features**: Multi-tenant support, advanced security

---

## 📞 Support & Community

### **Getting Help**

- **Documentation**: This comprehensive guide
- **Code Comments**: Inline documentation in source code
- **Logs**: Detailed logging for debugging
- **Tests**: Comprehensive test suite for validation

### **Contributing**

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests and documentation**
5. **Submit a pull request**

### **Reporting Issues**

When reporting issues, include:
- **Environment details**: OS, Python version, dependencies
- **Error logs**: Full error messages and stack traces
- **Steps to reproduce**: Detailed reproduction steps
- **Expected vs actual behavior**: Clear description of the issue

---

## 📝 License & Legal

### **Project License**

This project is licensed under the MIT License. See LICENSE file for details.

### **Legal Considerations**

- **Terms of Service**: Ensure compliance with TikTok's ToS
- **Data Privacy**: Follow applicable data protection laws
- **Rate Limiting**: Respect platform rate limits
- **Ethical Use**: Use responsibly and ethically

### **Compliance**

- **GDPR**: European data protection compliance
- **CCPA**: California privacy compliance
- **COPPA**: Children's privacy protection
- **Platform Policies**: TikTok and other platform policies

---

## 🎯 Conclusion

The TikTok Scraper is a powerful, production-ready system that combines modern software engineering practices with intelligent automation. Its modular architecture, comprehensive error handling, and extensive monitoring capabilities make it suitable for both development and production environments.

### **Key Strengths**

- **Scalability**: Handles multiple concurrent scraping tasks
- **Reliability**: Robust error handling and recovery mechanisms
- **Intelligence**: LLM-powered natural language processing
- **Monitoring**: Comprehensive logging and health monitoring
- **Maintainability**: Clean, modular code structure

### **Best Practices**

- **Test thoroughly** before deploying to production
- **Monitor performance** and adjust configuration as needed
- **Keep dependencies updated** for security and performance
- **Document changes** to maintain system knowledge
- **Backup data** regularly to prevent data loss

### **Next Steps**

1. **Deploy the system** in your environment
2. **Configure monitoring** and alerting
3. **Test with small datasets** before scaling up
4. **Monitor performance** and optimize as needed
5. **Contribute improvements** to the community

---

*This documentation is a living document. Please update it as the system evolves and new features are added.*
