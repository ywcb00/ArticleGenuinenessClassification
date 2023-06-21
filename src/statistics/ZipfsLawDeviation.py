from .Statistic import IStatistic
import numpy as np
from utils import getWords
from nltk import FreqDist

# The Zipf's Law describes the distribution of words in a general text corpus.
#   In theory, the occurence count of the i-th most common word should be
#   ((i+1)/i) as large as the occurence count of the (i+1)-th most common word.
#   Here, we take the difference of these theoretical word occurences from
#   the <N_CONSIDER> most occurent word pairs and scale them by the occurence
#   count of the more common word.
class ZipfsLawDeviation(IStatistic):
    SHORT_NAME = "ZLDev"
    N_CONSIDER = 7

    def collect(self, title, content):
        words = getWords(content)
        fd = FreqDist(words)

        freq = fd.values()
        freq = np.sort(np.array(list(freq)))
        freq = freq[::-1]

        deviations = []
        for counter in range(min(self.N_CONSIDER, (len(freq)-1))):
            zipf_diff = freq[counter] - (((counter+2)/(counter+1)) * freq[counter + 1])
            deviations.append(zipf_diff / freq[counter])

        return np.array(deviations)
