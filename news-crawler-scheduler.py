import subprocess
import schedule
import time
from concurrent.futures import ThreadPoolExecutor

CRAWLERS = [
    "guardian",
    "cnn"
]

def run_crawler(crawler: str):
    print(f"Starting crawler {crawler}...")
    subprocess.run(["scrapy", "crawl", crawler], check=True)

def run_crawlers():
    with ThreadPoolExecutor(max_workers=len(CRAWLERS)) as executor:
        executor.map(run_crawler, CRAWLERS)

schedule.every().day.at("06:00").do(run_crawlers)

if __name__ == "__main__":
    run_crawlers()
    while True:
        schedule.run_pending()
        time.sleep(60)