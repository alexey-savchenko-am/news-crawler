from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk import pos_tag
import re
from datetime import datetime
from scrapy.http import HtmlResponse
from typing import Optional

class TagExtractor:
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
    _rake = Rake(stopwords=_stop_words)

    @staticmethod
    def extract_tags(title: str):
        clean_title = re.sub(r"[‘’“”]", "'", title)

        TagExtractor._rake.extract_keywords_from_text(clean_title)
        phrases = TagExtractor._rake.get_ranked_phrases()

        words = set()
        for phrase in phrases:
            for word in phrase.split():
                word = word.lower()
                if word not in TagExtractor._stop_words:
                    words.add(word)
        
        tagged_words = pos_tag(list(words))
        tags = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]

        return tags
        

class DateExtractor:
    @staticmethod
    def extract_iso_date(
        response: HtmlResponse,
        xpath: str = '//meta[@property="article:published_time"]/@content'
    ) -> Optional[datetime]:
        date_str = response.xpath(xpath).get()

        if not date_str:
            return None
        
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None