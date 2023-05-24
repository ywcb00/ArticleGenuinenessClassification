from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getSentences

# Obtain the quartiles, mean and difference between mean and
#   median of the word counts over all sentences
class SentenceWordCount(IStatistic):
    SHORT_NAME = "SentWC"

    def collect(self, title, content):
        sentences = getSentences(content)
        sentlen = np.array(list(map(getNumWords, sentences)))
        sentlen_stats = np.quantile(sentlen, [0.25, 0.5, 0.75])
        sentlen_stats = np.append(sentlen_stats, np.mean(sentlen))
        sentlen_stats = np.append(sentlen_stats, np.mean(sentlen) - np.quantile(sentlen, 0.5))
        return sentlen_stats
