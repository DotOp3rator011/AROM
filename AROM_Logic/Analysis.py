import logging
import time

from .Scraper import Scraper
from .SentimentClassifier import Classifier

logging.basicConfig(level=logging.INFO)


def analyze(asin):
    # asin = "B073QVY9PQ"
    startTime = time.time()
    logging.info("ASIN: " + asin)
    url = "https://www.amazon.in/dp/" + asin
    logging.info("Extracting from URL: " + url)
    scraper = Scraper()
    scrapeTime = time.time()
    reviews = scraper.get_reviews(url)
    logging.info(time.time() - scrapeTime)
    logging.info("Extraction complete")
    total_reviews_count = len(reviews)
    logging.info("Number of reviews extracted: " + str(total_reviews_count))
    classifier = Classifier()
    logging.info("classifying reviews")
    analysisTime = time.time()
    opinions = classifier.classify(reviews)
    logging.info(time.time() - analysisTime)
    logging.info("classification complete")
    analysis = {
        "ASIN": asin,
        "total_reviews_count": total_reviews_count,
        "negative_reviews_count": opinions[0],
        "positive_reviews_count": opinions[1],
    }
    logging.info(time.time() - startTime)
    return analysis
