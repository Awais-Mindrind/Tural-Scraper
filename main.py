import logging
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.api import app
from src.task_manager import task_manager, generate_task_id, create_task_info
from src.airtable import get_active_hashtags

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_logs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Cron Job Trigger
def run_cron_job():
    """
    Cron job that runs every 24 hours to scrape active hashtags
    """
    logger.info("🕐 Cron job triggered - starting scheduled scraping")
    
    try:
        # Get active hashtags from Airtable
        active_hashtags = get_active_hashtags()
        
        if not active_hashtags:
            logger.warning("No active hashtags found in Airtable for cron job")
            return
        
        logger.info(f"Found {len(active_hashtags)} active hashtags for cron job")
        
        # Process each hashtag in parallel (but limited by queue processor)
        for hashtag in active_hashtags:
            task_id = generate_task_id()
            
            # Add to queue
            task_manager.add_to_queue(task_id, hashtag, 500)  # Default 500 profiles
            
            # Register task
            task_info = create_task_info(hashtag, 500, 'cron')
            task_manager.add_task(task_id, task_info)
            
            logger.info(f"Cron job: Queued task {task_id} for hashtag: {hashtag}")
        
        logger.info(f"✅ Cron job completed: {len(active_hashtags)} tasks queued")
        
    except Exception as e:
        logger.error(f"❌ Error in cron job: {e}")
        logger.error(f"Cron job traceback: {traceback.format_exc()}")

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(
    run_cron_job, 
    IntervalTrigger(hours=24), 
    id="daily_scraping",
    name="Daily TikTok Scraping"
)
scheduler.start()
logger.info("📅 Scheduler started - cron job will run every 24 hours")

# Periodic cleanup job
def cleanup_old_tasks():
    """Clean up old completed/failed tasks every 6 hours"""
    try:
        cleaned_count = task_manager.cleanup_old_tasks(max_age_hours=24)
        if cleaned_count > 0:
            logger.info(f"🧹 Cleanup job: Removed {cleaned_count} old tasks")
    except Exception as e:
        logger.error(f"Error in cleanup job: {e}")

scheduler.add_job(
    cleanup_old_tasks,
    IntervalTrigger(hours=6),
    id="cleanup_tasks",
    name="Task Cleanup"
)
logger.info("🧹 Cleanup job scheduled - runs every 6 hours")

# Health monitoring
def health_monitor():
    """Monitor system health and log statistics"""
    try:
        stats = task_manager.get_task_statistics()
        logger.info(f"📊 Health Monitor - Active: {stats['active_threads']}, "
                   f"Queue: {stats['queue_size']}, Total: {stats['total_tasks']}")
        
        # Log any long-running tasks
        active_threads = task_manager.get_active_threads()
        current_time = time.time()
        for task_id, thread_info in active_threads.items():
            runtime = current_time - thread_info.start_time
            if runtime > 3600:  # More than 1 hour
                logger.warning(f"⚠️ Long-running task: {task_id} running for {runtime/3600:.1f} hours")
                
    except Exception as e:
        logger.error(f"Error in health monitor: {e}")

scheduler.add_job(
    health_monitor,
    IntervalTrigger(minutes=30),
    id="health_monitor",
    name="Health Monitoring"
)
logger.info("💓 Health monitor scheduled - runs every 30 minutes")

# Graceful shutdown handler
def shutdown_handler():
    """Handle graceful shutdown"""
    logger.info("🛑 Shutdown signal received, cleaning up...")
    
    # Stop scheduler
    scheduler.shutdown()
    logger.info("📅 Scheduler stopped")
    
    # Wait for active tasks to complete (with timeout)
    active_count = task_manager.active_thread_count()
    if active_count > 0:
        logger.info(f"⏳ Waiting for {active_count} active tasks to complete...")
        timeout = 60  # 60 seconds timeout
        start_time = time.time()
        
        while task_manager.active_thread_count() > 0 and (time.time() - start_time) < timeout:
            time.sleep(1)
        
        remaining = task_manager.active_thread_count()
        if remaining > 0:
            logger.warning(f"⚠️ {remaining} tasks still running after timeout")
        else:
            logger.info("✅ All tasks completed")
    
    logger.info("👋 Shutdown complete")

# Register shutdown handler
import atexit
atexit.register(shutdown_handler)

# Run FastAPI app
if __name__ == "__main__":
    import uvicorn
    import traceback
    
    logger.info("🚀 Starting TikTok Scraper Triggers System...")
    logger.info("📁 Using modular architecture:")
    logger.info("   - api.py: FastAPI endpoints and LLM integration")
    logger.info("   - task_manager.py: Task management and threading")
    logger.info("   - triggers.py: Cron jobs and scheduling")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=5000,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("⚠️ Keyboard interrupt received")
        shutdown_handler()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        shutdown_handler()
        raise