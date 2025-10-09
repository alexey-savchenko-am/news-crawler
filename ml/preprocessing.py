import re
from typing import List
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag

class TextPreprocessor:
    """
    Class for cleaning and tokenizing text before training a model.
    """
    _stop_words = set(stopwords.words("english")) | {
        # common
        "lets", "us", "via", "say", "says", "said", "make", "makes", "made",
        "get", "gets", "got", "getting", "see", "seen", "look", "looks", "looking",
        "take", "takes", "taken", "give", "given", "giving",
        # auxiliary verbs
        "will", "would", "can", "could", "should", "may", "might", "must",
        "isn", "aren", "wasn", "weren", "hasn", "haven", "hadn",
        # particles and introductory words
        "also", "just", "still", "even", "really", "already", "yet",
        "one", "two", "three", "many", "much", "every", "some", "any",
        "new", "first", "second", "next", "last",
        # content-agnostic words from media headlines
        "update", "report", "analysis", "video", "photo", "watch",
        "breaking", "live", "exclusive",
    }

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Remove extra charachters and punctuation, and converts text to lowercase
        """

        # Transform text to lowercase
        text = text.lower()

        # Remove special symbols and quotes 
        text = re.sub(r"[‘’“”]", "'", text)

        # Remove everything except letters, numbers and spaces
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text
    
    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)

        result = [
            word for word, tag in tagged
            if word not in cls._stop_words and (tag.startswith("NN") or tag.startswith("JJ"))
        ]

        return result
    
    @classmethod
    def preprocess(cls, text: str) -> str:
        cleaned = cls.clean_text(text)
        tokens = cls.tokenize(cleaned)
        return " ".join(tokens)