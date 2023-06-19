from .Statistic import IStatistic
import numpy as np
from utils import getNumWords, getSentences, getWords
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Replace the paragraphs of NamedEntityRecognition by sentences
class NoParNamedEntityRecognition(IStatistic):
    SHORT_NAME = "NPNER"

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

        sentences = getSentences(content)

        ner_sentences = map(self.getNERTagList, sentences)

        ner_counts_sentences = [map(ner_p.count, self.NER_TAGS) for ner_p in ner_sentences]
        ner_counts_sentences = np.array([list(ner_c) for ner_c in ner_counts_sentences])

        num_words = getNumWords(content)
        ner_counts_content = np.sum(ner_counts_sentences, axis=0)

        # counts of the ner tags scaled by the total number of words
        ner_freq_content = ner_counts_content / num_words

        sentence_lengths = np.array([getNumWords(s) for s in sentences])

        ner_freq_sentences = ner_counts_sentences / sentence_lengths.reshape(-1,1)

        # difference between the ner tag frequencies of the overall content and the mean of the sentence frequencies
        ner_freq_contparadiff = ner_freq_content - np.mean(ner_freq_sentences, axis=0)
        ner_stats = np.append(ner_stats, ner_freq_contparadiff)

        # diff in mean and median frequencies between the first and the second half sentences
        ner_stats = np.append(ner_stats, np.mean(ner_freq_sentences[:len(sentences)//2], axis=0) - np.mean(ner_freq_sentences[len(sentences)//2:], axis=0))
        ner_stats = np.append(ner_stats, np.median(ner_freq_sentences[:len(sentences)//2], axis=0) - np.median(ner_freq_sentences[len(sentences)//2:], axis=0))

        return ner_stats
