import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

def getWords(text):
    paragraphs = getParagraphs(text)
    words = []
    for p in paragraphs:
        words.extend(word_tokenize(p))
    return words

def getNumWords(text):
    return len(getWords(text))

def getSentences(text):
    paragraphs = getParagraphs(text)
    sentences = []
    for p in paragraphs:
        sentences.extend(sent_tokenize(p))
    return sentences

def getNumSentences(text):
    return len(getSentences(text))

def numSentencesBetween(text, min, max):
    num_sentences = getNumSentences(text)
    if(num_sentences >= min and num_sentences <= max):
        return True
    return False

def getParagraphs(text):
    return text.split('\n')
