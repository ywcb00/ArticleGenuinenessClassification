from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getParagraphs

# Obtain the min, average, and max word count per paragraph
class ParagraphLengthWordCount(IStatistic):
    SHORT_NAME = "ParWC"

    def collect(self, title, content):
        paragraphs = getParagraphs(content)
        parlen = np.array(list(map(getNumWords, paragraphs)))
        return np.array([np.min(parlen), np.mean(parlen), np.max(parlen)])
