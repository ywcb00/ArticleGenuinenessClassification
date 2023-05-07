from abc import ABC, abstractmethod

class IStatistic(ABC):
    @property
    @abstractmethod
    def SHORT_NAME(self):
        # define a member variable for the short name (max. 10 characters) as
        #   it will appear in the resulting overall dataframe of statistics
        pass

    @abstractmethod
    def collect(self, title, content):
        # @param title article title as text string
        # @param content article content as text string
        # extract features from the documents and compute/obtain statistical
        #   values (numbers) from these features
        # the resulting values should be expected to have one mean throughout
        #   the population of real news articles
        # @return the array with one/multiple number values
        pass
