import os

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://admin:secret@db:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "news")

settings = Settings()