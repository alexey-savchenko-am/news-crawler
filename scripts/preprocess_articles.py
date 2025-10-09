from repositories.article_repository import ArticleRepository
from repositories.article_ml_repository import ArticleMLRepository
from models.article_ml import ArticleML
from ml.preprocessing import TextPreprocessor
from datetime import datetime, timezone
from logging import Logger

def preprocess_articles(
        logger: Logger,
        article_repo: ArticleRepository,
        article_ml_repo: ArticleMLRepository,
        preprocessor: TextPreprocessor
):
    logger.info("Start articles preprocessing...")

    for batch in article_repo.get_batches(batch_size=100, is_processed=False):
        try:
            articles_ml = []
            processed_ids = []

            for article in batch:
                preprocessed_content = preprocessor.preprocess(article.content)
                article_ml = ArticleML(
                    article_id=article.id,
                    content=preprocessed_content,
                    tags=article.tags
                )
                articles_ml.append(article_ml)
                processed_ids.append(article.id)

            article_ml_repo.create_many(articles_ml)
            article_repo.update_many(processed_ids, {"processed_at": datetime.now(timezone.utc)})

            logger.info(f"Processed batch of {len(batch)} articles.")
        except Exception as e:
            logger.exception(f"Error while processing batch: {e}")

    logger.info("Preprocessing completed.")