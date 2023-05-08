from .Statistic import IStatistic
import numpy as np

class ParagraphLengthWordCount(IStatistic):
    SHORT_NAME = "ParWC"

    def collect(self, title, content):
        paragraphs = content.split('\n')
        parlen = np.array(list(map(lambda p: len(p.split(' ')), paragraphs)))
        return np.array([np.min(parlen), np.mean(parlen), np.max(parlen)])
