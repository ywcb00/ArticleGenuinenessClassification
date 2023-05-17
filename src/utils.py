import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

def getWords(text):
    return word_tokenize(text)

def getNumWords(text):
    return len(getWords(text))

def getSentences(text):
    return sent_tokenize(text)

def numSentencesBetween(text, min, max):
    num_sentences = len(getSentences(text))
    if(num_sentences >= min and num_sentences <= max):
        return True
    return False

def getParagraphs(text):
    return text.split('\n')
