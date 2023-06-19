from .NamedEntityRecognition import NamedEntityRecognition
from .NoParNamedEntityRecognition import NoParNamedEntityRecognition
from .NoParPartOfSpeechTags import NoParPartOfSpeechTags
from .NoParSentimentAnalysisScore import NoParSentimentAnalysisScore
from .NoParTitleContentCommonality import NoParTitleContentCommonality
from .ParagraphLengthWordCount import ParagraphLengthWordCount
from .PartOfSpeechTags import PartOfSpeechTags
from .SentenceWordCount import SentenceWordCount
from .SentimentAnalysisScore import SentimentAnalysisScore
from .StopWordsCountProportion import StopWordsCountProportion
from .TitleContentCommonality import TitleContentCommonality
from .WordFreqProportion import WordFreqProportion
from .ZipfsLawDeviation import ZipfsLawDeviation

StatisticList = [
    NamedEntityRecognition,
    NoParNamedEntityRecognition,
    NoParPartOfSpeechTags,
    NoParSentimentAnalysisScore,
    NoParTitleContentCommonality,
    ParagraphLengthWordCount,
    PartOfSpeechTags,
    SentenceWordCount,
    SentimentAnalysisScore,
    StopWordsCountProportion,
    TitleContentCommonality,
    WordFreqProportion,
    ZipfsLawDeviation
]
