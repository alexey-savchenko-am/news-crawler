import subprocess
import schedule
import time
from concurrent.futures import ThreadPoolExecutor
from scripts.preprocess_articles import preprocess_articles
from datetime import datetime, timezone
from repositories.article_repository import ArticleRepository
from repositories.article_ml_repository import ArticleMLRepository
from ml.preprocessing import TextPreprocessor
import logging
import os

CRAWLERS = [
    "guardian",
    "cnn"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)
article_repo = ArticleRepository()
article_ml_repo = ArticleMLRepository()
preprocessor = TextPreprocessor()


def run_crawler(crawler: str):
    try:
        logger.info(f"Starting crawler '{crawler}'...")
        subprocess.run(["scrapy", "crawl", crawler], check=True)
        logger.info(f"Crawler '{crawler}' finished successfully.")
    except subprocess.CalledProcessError as e:
        logger.exception(f"Crawler '{crawler}' failed: {e}")

def run_crawlers():
    logger.info("Start articles crawling...")
    with ThreadPoolExecutor(max_workers=len(CRAWLERS)) as executor:
        executor.map(run_crawler, CRAWLERS)
    logger.info("Articles crawling completed.")

def run_pipeline():
    logger.info(" === PIPELINE STARTED === ")
    run_crawlers()
    preprocess_articles(logger, article_repo, article_ml_repo, preprocessor)
    logger.info(" === PIPELINE FINISHED === ")

schedule.every().day.at("06:00").do(run_pipeline)

if __name__ == "__main__":
    crawling_after_start = os.getenv("CRAWLING_AFTER_START", "false").lower()

    if crawling_after_start == "true":
        run_pipeline()
        
    while True:
        schedule.run_pending()
        time.sleep(60)