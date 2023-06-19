from .Statistic import IStatistic
import numpy as np
from utils import getNumSentences, getSentences, getSentences, getWords
import nltk
nltk.download('universal_tagset')

# Replace the paragraphs of TitleContentCommonality by sentences
class NoParTitleContentCommonality(IStatistic):
    SHORT_NAME = "NPTCCom"

    RELEVANT_POS_TAGS = ['NOUN', 'NUM', 'X']

    def getPosTagList(self, text):
        words_sentences = getSentences(text)
        words_sentences = list(map(getWords, words_sentences))

        pos = nltk.pos_tag_sents(words_sentences, tagset='universal')
        pos = sum(pos, []) # flatten the list

        return pos

    def filterRelevantPosTags(self, text):
        pos = self.getPosTagList(text)
        # filter relevant pos tags
        pos = filter(lambda elem: elem[1] in self.RELEVANT_POS_TAGS, pos)
        words = list(map(lambda elem: elem[0].lower(), pos))
        return words

    def collect(self, title, content):
        tccom_stats = np.array([])

        num_sentences = getNumSentences(content)

        title_words = getWords(title)
        title_words = list(map(lambda w: w.lower(), title_words))


        content_words = self.filterRelevantPosTags(content)

        sentences = getSentences(content)
        first_half_sentences_words = self.filterRelevantPosTags('\n'.join(sentences[:len(sentences)//2]))
        second_half_sentences_words = self.filterRelevantPosTags('\n'.join(sentences[len(sentences)//2:]))

        fhp_common_occurence_count = map(first_half_sentences_words.count, title_words)
        fhp_common_occurence_count = np.array(list(fhp_common_occurence_count))

        shp_common_occurence_count = map(second_half_sentences_words.count, title_words)
        shp_common_occurence_count = np.array(list(shp_common_occurence_count))
        # append the difference in common occurence count of title and content between the first half of sentences
        #   and the second half of sentences scaled by the total number of sentences
        tccom_stats = np.append(tccom_stats, (np.sum(fhp_common_occurence_count) - np.sum(shp_common_occurence_count)) / num_sentences)

        return tccom_stats
