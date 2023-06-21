from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getParagraphs, getSentences
from transformers import pipeline

# Based on https://huggingface.co/blog/sentiment-analysis-python

# Perform a sentiment analysis on the article content
class SentimentAnalysisScore(IStatistic):
    SHORT_NAME = "SAS"

    sentiment_pipeline = pipeline("sentiment-analysis")

    def getPositiveSentimentScore(self, text_arr):
        try:
            scores = self.sentiment_pipeline(text_arr)
            scores = map(lambda elem: (1-elem['score']) if elem['label'] == 'NEGATIVE'
                else elem['score'], scores)
        except:
            if(type(text_arr) is list):
                scores = [np.nan for ix in text_arr]
            else:
                scores = [np.nan]

        return np.array(list(scores))

    def collect(self, title, content):
        sentiment_stats = np.array([])

        # append the min, mean, median, and max sentiment score of the paragraphs
        paragraphs = getParagraphs(content)
        # NOTE: we cannot process text with more than 512 tokens with the sentiment pipeline
        #   Hence, we simply set the paragraph to nan
        paragraphs = list(map(lambda p: "" if getNumWords(p) > 500 else p ,paragraphs))
        sentiment_par = self.getPositiveSentimentScore(paragraphs)
        sentiment_stats = np.append(sentiment_stats, np.min(sentiment_par))
        sentiment_stats = np.append(sentiment_stats, np.mean(sentiment_par))
        sentiment_stats = np.append(sentiment_stats, np.median(sentiment_par))
        sentiment_stats = np.append(sentiment_stats, np.max(sentiment_par))

        # append the variance between the sentiment score of the paragraphs
        sentiment_stats = np.append(sentiment_stats, np.var(sentiment_par))

        # append the sentiment score of the first half and the second half individually and
        #   the difference of both
        sentiment_firsthalf = np.mean(self.getPositiveSentimentScore(paragraphs[:(len(paragraphs)//2)]))
        sentiment_secondhalf = np.mean(self.getPositiveSentimentScore(paragraphs[(len(paragraphs)//2):]))
        sentiment_stats = np.append(sentiment_stats, sentiment_firsthalf)
        sentiment_stats = np.append(sentiment_stats, sentiment_secondhalf)
        sentiment_stats = np.append(sentiment_stats, sentiment_firsthalf - sentiment_secondhalf)

        # append the min, mean, and max of the mean squared difference between the
        #   sentiment scores of the paragraphs and the sentiment scores of their sentences
        sentiment_pardiffsentence = [(self.getPositiveSentimentScore(par) - np.mean(self.getPositiveSentimentScore(getSentences(par))))**2 for par in paragraphs]
        sentiment_pardiffsentence = np.array(sentiment_pardiffsentence)
        if(sentiment_pardiffsentence is not None):
            sentiment_stats = np.append(sentiment_stats, np.min(sentiment_pardiffsentence))
            sentiment_stats = np.append(sentiment_stats, np.mean(sentiment_pardiffsentence))
            sentiment_stats = np.append(sentiment_stats, np.max(sentiment_pardiffsentence))
        else:
            sentiment_stats = np.append(sentiment_stats, [np.nan, np.nan, np.nan])

        return sentiment_stats
