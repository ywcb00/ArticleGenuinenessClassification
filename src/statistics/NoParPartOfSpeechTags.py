from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getSentences, getWords
import nltk
nltk.download('universal_tagset')

# Replace the paragraphs of PartOfSpeechTags by sentences
class NoParPartOfSpeechTags(IStatistic):
    SHORT_NAME = "NPPoSTag"

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

        sentences = getSentences(content)
        first_half_pos_counts = self.getPosTagCounts('\n'.join(sentences[:len(sentences)//2]))
        second_half_pos_counts = self.getPosTagCounts('\n'.join(sentences[len(sentences)//2:]))
        # append the difference of pos tag frequencies between the first half of sentences and the second half
        pos_stats = np.append(pos_stats, (first_half_pos_counts - second_half_pos_counts) / num_words)

        return pos_stats
