#!/bin/bash

# LOG_FILE_PATH="logs/celery_sync_$(date +\%Y-\%m-\%d).log"
celery -A cron_tasks.celery_app worker --loglevel=INFO
