import json
import logging
import pickle
import random
from os.path import isfile

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO)


class Classifier:

    def __init__(self):
        """
            Default constructor
        """
        pass

    @staticmethod
    def get_corpus():
        """ get the corpus from Corpus.json and make a list
        Args:
            None
        Returns:
            corpus (list): list of corpus data
        """

        with open("C:/Users/rahul/PycharmProjects/AmazonReviewsClassifier/AROM_Logic/Corpus.json", "r") as jf:
            corpus = json.load(jf)
            random.shuffle(corpus)
        return corpus

    @staticmethod
    def word_features(words):
        """ Create a dictionary of features
        Args:
            words (string): sentence to be converted as features
        Returns:
            features (dict): dictionary of feature words
        """

        stopWords = set(stopwords.words("english"))
        features = dict([(word, True) for word in word_tokenize(words) if word not in stopWords])
        return features

    def get_trainingSet(self):
        """ Convert the corpus data into training data 
        Args:
            None
        Returns:
            trainingSet (list): list of training data
        """

        corpus = self.get_corpus()
        trainingSet = list()
        for item in corpus:
            trainingSet.append((self.word_features(item["text"]), item["label"]))
        return trainingSet

    def get_classifier(self):
        """ Trains and returns the classifier or a pickle
        Args:
            None
        Returns:
            classifier (object): negative and positive opinion count
        """

        if isfile('AROM_Logic/classifier.pickle'):
            with open("AROM_Logic/classifier.pickle", "rb") as pickleFile:
                classifier = pickle.load(pickleFile)
            return classifier
        trainingSet = self.get_trainingSet()
        classifier = NaiveBayesClassifier.train(trainingSet)
        with open("AROM_Logic/classifier.pickle", "wb") as pickleFile:
            pickle.dump(classifier, pickleFile)
        return classifier

    def classify(self, reviews):
        """ Classify the text as postive or negative and sum the count of each
        Args:
            reviews (list): list of reviews to be classified
        Returns:
            opinions (list): negative and positive opinion count
        """

        classifier = self.get_classifier()
        negative_reviews_count = 0
        positive_reviews_count = 0
        for review in reviews:
            try:
                opinion = classifier.classify(self.word_features(review))
                if opinion == "negative":
                    negative_reviews_count += 1
                elif opinion == "positive":
                    positive_reviews_count += 1
            except Exception as e:
                logging.info(e)
        return [negative_reviews_count, positive_reviews_count]
