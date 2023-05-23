from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getWords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import FreqDist

# Collect the stopwords of the whole article content and consider
#   the proportion of all stopwords w.r.t. the total word count
#   as well as the proportions of the <N_CONSIDER> most common
#   stopwords w.r.t. the total word count.
class StopWordsCountProportion(IStatistic):
    SHORT_NAME = "StopWC"
    N_CONSIDER = 8

    def collect(self, title, content):
        words = getWords(content)
        num_words = getNumWords(content)

        stopword_set = set(stopwords.words('english'))
        filtered_stopwords = filter(lambda w: w in stopword_set, words)
        filtered_stopwords = list(filtered_stopwords)

        totalswcount = len(filtered_stopwords)

        fd = FreqDist(filtered_stopwords)
        freq = fd.values()
        freq = np.sort(np.array(list(freq)))
        freq = freq[::-1]

        if(self.N_CONSIDER <= len(freq)):
            high_freq = freq[ :self.N_CONSIDER]
        else:
            high_freq = np.concatenate((freq, np.zeros(self.N_CONSIDER - len(freq))))

        sw_freq = np.concatenate((np.array([totalswcount]), high_freq))

        freq_prop = sw_freq / num_words

        return np.array(freq_prop)
