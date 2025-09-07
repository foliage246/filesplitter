import os
import shutil
from datetime import datetime, timedelta
from flask import current_app

def cleanup_old_files():
    """Clean up files older than 24 hours from uploads and downloads directories"""
    cutoff_time = datetime.now() - timedelta(hours=24)

    # Clean uploads directory
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            filepath = os.path.join(uploads_dir, filename)
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_modified < cutoff_time:
                    try:
                        os.remove(filepath)
                        current_app.logger.info(f"Cleaned up old upload file: {filename}")
                    except Exception as e:
                        current_app.logger.error(f"Error cleaning up {filename}: {str(e)}")

    # Clean downloads directory
    downloads_dir = current_app.config['DOWNLOAD_FOLDER']
    if os.path.exists(downloads_dir):
        for filename in os.listdir(downloads_dir):
            filepath = os.path.join(downloads_dir, filename)
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_modified < cutoff_time:
                    try:
                        os.remove(filepath)
                        current_app.logger.info(f"Cleaned up old download file: {filename}")
                    except Exception as e:
                        current_app.logger.error(f"Error cleaning up {filename}: {str(e)}")

def init_scheduler(app):
    """Initialize background scheduler for cleanup tasks"""
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: app.app_context()(cleanup_old_files)(),
        trigger=IntervalTrigger(hours=1),  # Run every hour
        id='cleanup_job',
        name='Clean up old files',
        replace_existing=True
    )
    scheduler.start()
    app.logger.info("File cleanup scheduler started")
    return scheduler