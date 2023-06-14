from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getParagraphs, getSentences, getWords
import nltk
nltk.download('universal_tagset')

# Count the occurences of the 12 individual PoS tags in the total content and
#   compare the difference in PoS tag counts between the first and the second
#   half of paragraphs
class PartOfSpeechTags(IStatistic):
    SHORT_NAME = "PoSTag"

    POS_TAGS = ['ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRT', 'PRON', 'VERB', '.', 'X']

    def getPosTagList(self, text):
        words_sentences = getSentences(text)
        words_sentences = list(map(getWords, words_sentences))

        pos = nltk.pos_tag_sents(words_sentences, tagset='universal')
        pos = sum(pos, []) # flatten the list

        return pos

    def getPosTagCounts(self, text):
        pos = self.getPosTagList(text)
        pos = list(map(lambda elem: elem[1], pos))
        postag_counts = [pos.count(pt) for pt in self.POS_TAGS]
        return np.array(postag_counts)

    def collect(self, title, content):
        pos_stats = np.array([])

        num_words = getNumWords(content)

        content_pos_counts = self.getPosTagCounts(content)
        # append the pos tag counts from the content scaled by the total number of words
        pos_stats = np.append(pos_stats, content_pos_counts / num_words)

        paragraphs = getParagraphs(content)
        first_half_pos_counts = self.getPosTagCounts('\n'.join(paragraphs[:len(paragraphs)//2]))
        second_half_pos_counts = self.getPosTagCounts('\n'.join(paragraphs[len(paragraphs)//2:]))
        # append the difference of pos tag frequencies between the first half of paragraphs and the second half
        pos_stats = np.append(pos_stats, (first_half_pos_counts - second_half_pos_counts) / num_words)

        return pos_stats
