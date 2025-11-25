from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from repositories.article_ml_repository import ArticleMLRepository
from typing import Optional
import joblib
from logging import Logger

class ArticleModelTrainer:
    def __init__(self, logger: Logger, repo: ArticleMLRepository, model_path: str = "model.pkl"):
        self._logger = logger
        self._repo: ArticleMLRepository = repo
        self._model_path = model_path
        self._mlb = MultiLabelBinarizer()
        self._model = Optional[Pipeline] = None

    def _load_model(self):
        self._model, self._mlb = joblib.load(self._model_path)

    def _create_model(self):
        self._model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=30_000, ngram_range=(1,2))),
            ('clf', OneVsRestClassifier(SGDClassifier(loss='log_loss', max_iter=5)))
        ])

    def train_batches(
        self,
        batch_size: int = 500,
        initial: bool = False,
        **query_filters
    ) -> None:
        
        if initial:
            self._logger.info("== Fitting Model from scratch... ==")
            self._create_model()
        else:
            self._logger.info("== Loading an existing Model... ==")
            self._load_model()

        batches = self._repo.get_batches(batch_size=batch_size, **query_filters)

        for i, batch in enumerate(batches, start=1):
            X_batch = [b.content for b in batch]
            y_batch = [b.tags for b in batch]

            if initial and i == 1:
                Y = self._mlb.fit_transform(y_batch)
                self._model.fit(X_batch, )