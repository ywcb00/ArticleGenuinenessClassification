from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getWords
from nltk import FreqDist

# Take the <N_CONSIDER> highest word occurences and scale them
#   by the total word count
class WordFreqProportion(IStatistic):
    SHORT_NAME = "WFProp"
    N_CONSIDER = 7

    def collect(self, title, content):
        words = getWords(content)
        fd = FreqDist(words)

        num_words = getNumWords(content)
        freq = fd.values()
        freq = np.sort(np.array(list(freq)))

        high_freq = freq[-self.N_CONSIDER: ][::-1]

        freq_prop = high_freq / num_words

        return freq_prop
