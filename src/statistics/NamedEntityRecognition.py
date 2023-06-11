from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getParagraphs, getWords
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# perform a named entity recognition on the content and on its individual
#   paragraphs and collect statistics like the proportion of nameable entities
#   w.r.t. the total word count as well as the proportions of individual
#   entity types
class NamedEntityRecognition(IStatistic):
    SHORT_NAME = "NER"

    NER_TAGS = ['ORGANIZATION', 'PERSON', 'LOCATION', 'DATE', 'TIME', 'MONEY', 'PERCENT', 'FACILITY', 'GPE']

    def getNERTagList(self, text):
        words = getWords(text)

        pos = nltk.pos_tag(words)

        ner = nltk.ne_chunk(pos)
        ner = nltk.tree2conlltags(ner)
        ner = map(lambda elem: elem[2], ner)
        ner = filter(lambda elem: len(elem) > 2, ner)
        ner = map(lambda elem: elem[2:], ner)

        return list(ner)

    def collect(self, title, content):
        ner_stats = np.array([])

        paragraphs = getParagraphs(content)

        ner_paragraphs = map(self.getNERTagList, paragraphs)

        ner_counts_paragraphs = [map(ner_p.count, self.NER_TAGS) for ner_p in ner_paragraphs]
        ner_counts_paragraphs = np.array([list(ner_c) for ner_c in ner_counts_paragraphs])

        num_words = getNumWords(content)
        ner_counts_content = np.sum(ner_counts_paragraphs, axis=0)

        # total number of nameable entities scaled by the number of words
        ner_stats = np.append(ner_stats, np.sum(ner_counts_content) / num_words)

        # counts of the ner tags scaled by the total number of words
        ner_freq_content = ner_counts_content / num_words
        ner_stats = np.append(ner_stats, ner_freq_content)

        paragraph_lengths = np.array([getNumWords(p) for p in paragraphs])

        ner_freq_paragraphs = ner_counts_paragraphs / paragraph_lengths.reshape(-1,1)

        # difference between the ner tag frequencies of the overall content and the mean of the paragraph frequencies
        ner_freq_contparadiff = ner_freq_content - np.mean(ner_freq_paragraphs, axis=0)
        ner_stats = np.append(ner_stats, ner_freq_contparadiff)

        # diff in mean and median frequencies between the first and the second half paragraphs
        ner_stats = np.append(ner_stats, np.mean(ner_freq_paragraphs[:len(paragraphs)//2], axis=0) - np.mean(ner_freq_paragraphs[len(paragraphs)//2:], axis=0))
        ner_stats = np.append(ner_stats, np.median(ner_freq_paragraphs[:len(paragraphs)//2], axis=0) - np.median(ner_freq_paragraphs[len(paragraphs)//2:], axis=0))

        return ner_stats
