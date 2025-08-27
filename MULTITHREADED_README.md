# TikTok Scraper - Modular Multithreaded System

## 🚀 Overview

This system provides a robust, modular, and multithreaded approach to managing TikTok profile scraping tasks through both API triggers and automated cron jobs. It's designed with clean separation of concerns, making it maintainable, testable, and scalable.

## ✨ Key Features

- **Modular Architecture**: Clean separation of concerns across multiple files
- **Multithreaded Execution**: Run multiple scrapers simultaneously without conflicts
- **Thread-Safe Task Management**: Queue-based system with proper locking mechanisms
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **API & Cron Integration**: Both manual API calls and automated scheduling
- **LLM Integration**: Natural language query processing for intelligent scraping
- **Airtable Integration**: Fetch active hashtags dynamically from Airtable
- **Health Monitoring**: Real-time status tracking and health checks
- **Error Isolation**: Thread failures don't affect other running tasks

## 🏗️ Architecture

### **Modular File Structure**

```
├── schemas.py              # All Pydantic BaseModel classes
├── task_manager.py         # Task management and threading logic
├── api.py                  # FastAPI endpoints and LLM integration
├── triggers.py             # Cron jobs and scheduling
├── airtable.py            # Airtable integration
├── tikTok_Scraper.py      # Enhanced scraper with comprehensive logging
├── llm_query.py           # LLM query processing
├── test_triggers.py       # Comprehensive test suite
├── MULTITHREADED_README.md # This documentation
└── scraper_logs.log       # Comprehensive logging output
```

### **Core Components**

1. **`schemas.py`**: Centralized data models and validation
2. **`task_manager.py`**: Thread-safe task management system
3. **`api.py`**: RESTful API endpoints and LLM integration
4. **`triggers.py`**: Cron scheduling and system orchestration
5. **`airtable.py`**: External data source integration
6. **`tikTok_Scraper.py`**: Core scraping functionality

### **Thread Safety Features**

- **Locked Resources**: Thread-safe access to shared data structures
- **Queue Management**: Atomic operations for task queuing/dequeuing
- **Status Tracking**: Thread-safe task status updates
- **Resource Cleanup**: Automatic cleanup of completed threads

## 📁 File Descriptions

### **`schemas.py`** - Data Models
Contains all Pydantic BaseModel classes:
- **Profile Models**: `Profile`, `ProfileFilters`
- **API Models**: `ScraperRequest`, `ScraperResponse`, `TaskStatus`
- **LLM Models**: `AIQueryRequest`, `LLMQueryResponse`
- **Task Models**: `TaskInfo`, `TaskQueueItem`, `ThreadInfo`

### **`task_manager.py`** - Task Management
Handles all task-related operations:
- **TaskManager Class**: Thread-safe task tracking
- **Queue Management**: Priority-based task queuing
- **Thread Tracking**: Active thread monitoring
- **Statistics**: Performance metrics and reporting

### **`api.py`** - API Endpoints
FastAPI application with all endpoints:
- **Scraper Endpoints**: Start, monitor, and manage scraping tasks
- **LLM Endpoints**: Natural language query processing
- **Task Endpoints**: Task status and management
- **Health Endpoints**: System monitoring and statistics

### **`triggers.py`** - System Orchestration
Manages cron jobs and system lifecycle:
- **Cron Scheduling**: Automated scraping every 24 hours
- **Health Monitoring**: Periodic system health checks
- **Task Cleanup**: Automatic cleanup of old tasks
- **Graceful Shutdown**: Proper resource cleanup

## 🚀 Getting Started

### 1. Prerequisites

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file with:

```env
AIRTABLE_PAT=your_airtable_personal_access_token
GOOGLE_API_KEY=your_google_gemini_api_key
PROXY=your_proxy_settings_if_needed
```

### 3. Airtable Setup

Create a table named `hashtags` with columns:
- **Hashtag**: Text field for hashtag/category
- **Active**: Checkbox field (default: checked)

### 4. Start the System

```bash
python triggers.py
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### **Core Scraper Endpoints**

#### Start Scraper
```http
POST /start-scraper
Content-Type: application/json

{
  "hashtag": "travel",        # Optional: specific hashtag
  "num_profiles": 500,        # Number of profiles to scrape
  "priority": 1               # Task priority (higher = more important)
}
```

#### Start Scraper with LLM
```http
POST /start-scraper-with-llm
Content-Type: application/json

{
  "query": "Find TikTok profiles about travel with more than 10k followers"
}
```

### **LLM Integration Endpoints**

#### Process LLM Query
```http
POST /llm-query
Content-Type: application/json

{
  "query": "Find food bloggers from USA with high engagement"
}
```

**Response:**
```json
{
  "filters": {
    "hashtag": "food",
    "country": "USA",
    "min_followers": null,
    "min_likes": null,
    "limit": 100
  },
  "query": "Find food bloggers from USA with high engagement",
  "confidence": 1.0
}
```

### **Task Management Endpoints**

#### Get Task Status
```http
GET /task-status/{task_id}
```

#### Get Active Tasks
```http
GET /active-tasks
```

#### Get Task Statistics
```http
GET /task-statistics
```

#### Cancel Task
```http
DELETE /task/{task_id}
```

#### Cleanup Old Tasks
```http
POST /cleanup-tasks?max_age_hours=24
```

### **System Endpoints**

#### Health Check
```http
GET /health
```

#### Active Hashtags
```http
GET /active-hashtags
```

#### Root Information
```http
GET /
```

## ⚙️ Configuration

### **Thread Limits**

In `api.py`, adjust the maximum concurrent threads:

```python
max_concurrent_threads = 3  # Adjust based on your system capabilities
```

### **Cron Schedule**

Modify the cron job frequency in `triggers.py`:

```python
scheduler.add_job(run_cron_job, IntervalTrigger(hours=24), id="daily_scraping")
```

### **Task Cleanup**

Configure automatic cleanup in `triggers.py`:

```python
# Cleanup every 6 hours
scheduler.add_job(cleanup_old_tasks, IntervalTrigger(hours=6))

# Health monitoring every 30 minutes
scheduler.add_job(health_monitor, IntervalTrigger(minutes=30))
```

## 🔄 How It Works

### **1. Task Creation**
- API request or cron job creates a task
- Task is added to the priority queue in `task_manager.py`
- Task is registered with the TaskManager

### **2. Task Processing**
- Queue processor in `api.py` monitors the queue
- When a thread slot is available, task is dequeued
- New thread is started for the task
- Thread executes the scraper function

### **3. Task Execution**
- Each thread runs independently
- Status updates are logged and tracked
- Errors are isolated to individual threads
- Resources are cleaned up automatically

### **4. Task Completion**
- Thread updates final status
- Thread is removed from active tracking
- Results are logged and stored
- Queue processor continues with next task

## 🤖 LLM Integration

### **Natural Language Queries**

The system can process natural language requests:

```
"Find travel influencers with more than 50k followers from USA"
"Show me food bloggers with high engagement"
"Get fitness profiles from Europe"
```

### **Automatic Filter Generation**

The LLM automatically converts queries to structured filters:
- **Hashtag extraction**: Identifies relevant hashtags
- **Geographic filtering**: Detects country/region preferences
- **Engagement metrics**: Understands follower/like requirements
- **Content categorization**: Classifies profile types

## 📊 Monitoring & Logging

### **Log Files**

- **scraper_logs.log**: Comprehensive logging output
- **Console Output**: Real-time status updates

### **Log Format**

```
2024-01-01 12:00:00 - Scraper-task_123 - INFO - Starting scraper task task_123 for hashtag: travel
2024-01-01 12:00:01 - Scraper-task_123 - INFO - Web driver initialized successfully
2024-01-01 12:00:02 - Scraper-task_123 - INFO - Phase 1: Collecting profile URLs...
```

### **Performance Metrics**

The system tracks:
- Task execution time
- Success/failure rates
- Thread utilization
- Queue performance
- Error patterns
- LLM query processing time

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_triggers.py
```

This will test:
- Schema validation
- Task manager functionality
- LLM integration
- Airtable integration
- API endpoints
- Task management
- Error handling

## 🚨 Error Handling

### **Thread Isolation**
- Individual thread failures don't affect others
- Failed tasks are logged with full tracebacks
- System continues processing other tasks

### **Graceful Degradation**
- Queue overflow protection
- Resource cleanup on failures
- Automatic retry mechanisms (configurable)

### **LLM Error Handling**
- Fallback to default filters on LLM failures
- Query validation and sanitization
- Error logging for debugging

## 🔧 Troubleshooting

### **Common Issues**

1. **Thread Limit Reached**
   - Check `max_concurrent_threads` setting in `api.py`
   - Monitor queue size via `/health` endpoint

2. **Airtable Connection Issues**
   - Verify `AIRTABLE_PAT` environment variable
   - Check table name and column structure

3. **LLM Integration Issues**
   - Verify `GOOGLE_API_KEY` environment variable
   - Check internet connectivity for API calls

4. **Scraper Failures**
   - Check `scraper_logs.log` for detailed errors
   - Verify proxy settings if using one
   - Check TikTok's anti-bot measures

### **Debug Mode**

Enable debug logging in any file:

```python
logging.basicConfig(level=logging.DEBUG)
```

### **Performance Tuning**

- Adjust `max_concurrent_threads` based on system resources
- Monitor memory usage during heavy scraping
- Consider proxy rotation for large-scale operations
- Optimize LLM query processing for high-volume requests

## 🔮 Future Enhancements

- **Priority Queuing**: Implement task priority management
- **Retry Mechanisms**: Automatic retry for failed tasks
- **Load Balancing**: Distribute tasks across multiple servers
- **Metrics Dashboard**: Web-based monitoring interface
- **Task Scheduling**: More flexible cron patterns
- **Resource Monitoring**: CPU/memory usage tracking
- **Advanced LLM**: Multi-modal queries and better context understanding
- **Batch Processing**: Group similar tasks for efficiency

## 📝 License

This project is part of the TikTok Scraper system. Please ensure compliance with TikTok's terms of service and applicable laws when using this tool.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add comprehensive logging
5. Test thoroughly
6. Submit a pull request

---

**Note**: This system is designed for production use with proper error handling, logging, and thread safety. The modular architecture makes it easy to maintain, test, and extend. Always test in a development environment before deploying to production.
