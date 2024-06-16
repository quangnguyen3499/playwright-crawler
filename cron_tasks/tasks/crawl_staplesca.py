# from cron_tasks.celery_logging import logger
import logging
from datetime import datetime

from celery import shared_task


@shared_task
def crawl_staplesca_task():
    try:
        logging.info("----- Start crawling https://www.staples.ca -----")
        from websites.non_proxy import collect_data

        collect_data()
    except Exception as e:
        error_msg = f"""
            --- *{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}* ---
            Error crawling https://www.staples.ca:
            {repr(e)}
        """
        logging.error(error_msg)

    logging.info("End crawling staplesca")
    logging.info("----------------------------------------")
