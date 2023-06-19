from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getSentences
from transformers import pipeline

# Based on https://huggingface.co/blog/sentiment-analysis-python

# Replace the paragraphs of SentimentAnalysisScore by sentences
class NoParSentimentAnalysisScore(IStatistic):
    SHORT_NAME = "NPSAS"

    sentiment_pipeline = pipeline("sentiment-analysis")

    def getPositiveSentimentScore(self, text_arr):
        scores = self.sentiment_pipeline(text_arr)
        scores = map(lambda elem: (1-elem['score']) if elem['label'] == 'NEGATIVE'
            else elem['score'], scores)
        return np.array(list(scores))

    def collect(self, title, content):
        sentiment_stats = np.array([])

        # append the min, mean, median, and max sentiment score of the sentences
        sentences = getSentences(content)
        # NOTE: we cannot process text with more than 512 tokens with the sentiment pipeline
        #   Hence, we simply set the paragraph to nan
        sentences = list(map(lambda s: np.nan if getNumWords(s) > 500 else s ,sentences))
        sentiment_sents = self.getPositiveSentimentScore(sentences)
        sentiment_stats = np.append(sentiment_stats, np.min(sentiment_sents))
        sentiment_stats = np.append(sentiment_stats, np.mean(sentiment_sents))
        sentiment_stats = np.append(sentiment_stats, np.median(sentiment_sents))
        sentiment_stats = np.append(sentiment_stats, np.max(sentiment_sents))

        # append the variance between the sentiment score of the sentences
        sentiment_stats = np.append(sentiment_stats, np.var(sentiment_sents))

        # append the sentiment score of the first half and the second half individually and
        #   the difference of both
        sentiment_firsthalf = np.mean(self.getPositiveSentimentScore(sentences[:(len(sentences)//2)]))
        sentiment_secondhalf = np.mean(self.getPositiveSentimentScore(sentences[(len(sentences)//2):]))
        sentiment_stats = np.append(sentiment_stats, sentiment_firsthalf)
        sentiment_stats = np.append(sentiment_stats, sentiment_secondhalf)
        sentiment_stats = np.append(sentiment_stats, sentiment_firsthalf - sentiment_secondhalf)

        return sentiment_stats
