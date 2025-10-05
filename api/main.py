from fastapi import FastAPI, Query
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime
from db.mongo import articles_collection
from .news_dto import NewsDTO, NewsResponse

app = FastAPI()

@app.get("/api/news", summary="Get News", tags=["News"])
def get_news(
    source: Optional[str] = Query(None, description="Source of information (f.e. Guardian)"),
    tags: Optional[List[str]] = Query(None, description="List of tags for filtration"),
    start_date: Optional[str] = Query(None, description="Publish date from (f.e. 2025-10-01)"),
    end_date: Optional[str] = Query(None, description="Publish date to (f.e. 2025-10-01)"),
    limit: int = Query(10, description="Max count")
):
    query = {}

    if source:
        query["source"] = source
    
    if tags:
        query["tags"] = {"$in": tags}

    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = datetime.fromisoformat(start_date)
        if end_date:
            date_filter["$lte"] = datetime.fromisoformat(end_date)
        query["date"] = date_filter

    cursor = articles_collection.find(query).limit(limit)
    results: List[NewsDTO] = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(NewsDTO(**doc))

    return NewsResponse(count=len(results), items=results)

    

