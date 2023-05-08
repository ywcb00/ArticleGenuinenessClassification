import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def getSentences(text):
    return sent_tokenize(text)

def numSentencesBetween(text, min, max):
    num_sentences = len(getSentences(text))
    if(num_sentences >= min and num_sentences <= max):
        return True
    return False
