from fastapi import FastAPI, Query
from typing import List, Optional
from datetime import datetime
from .news_response import NewsResponse
from repositories.article_repository import ArticleRepository

app = FastAPI()
repo = ArticleRepository()

@app.get("/api/news", summary="Get News", tags=["News"])
def get_news(
    source: Optional[str] = Query(None, description="Source of information (f.e. Guardian)"),
    tags: Optional[List[str]] = Query(None, description="List of tags for filtration"),
    start_date: Optional[str] = Query(None, description="Publish date from (f.e. 2025-10-01)"),
    end_date: Optional[str] = Query(None, description="Publish date to (f.e. 2025-10-01)"),
    limit: int = Query(10, description="Max count")
):
    
    start_date_iso = datetime.fromisoformat(start_date) if start_date else None
    end_date_iso = datetime.fromisoformat(end_date) if end_date else None

    articles = repo.get_list(source, tags, start_date_iso, end_date_iso, limit)

    return NewsResponse(
        count=len(articles), 
        items = articles
    )