from articlecrawler import crawler
from articlecrawler.crawldata import crawldata
from statistics.StatisticList import StatisticList
from utils import numSentencesBetween
import pandas as pd

MIN_SENTENCES = 50
MAX_SENTENCES = 100
FILE_PATH = './collected_stats.csv'

class Collector:
    def __init__(self):
        self.statlist = list(map(lambda s: s(), StatisticList))
        try:
            self.collected_stats = pd.read_csv(FILE_PATH)
            self.collected_urls = set(self.collected_stats['url'])
        except FileNotFoundError:
            self.collected_stats = pd.DataFrame()
            self.collected_urls = set()

    def collectStats(self, url, title, content):
        stat_row = {'url': url, 'title': title}
        for stat in self.statlist:
            stat_arr = stat.collect(title, content)
            stat_dict = self.getStatisticalValuesDict(stat_arr, stat.SHORT_NAME)
            print("=====", stat_dict)
            stat_row = {**stat_row, **stat_dict}
        self.addToCollectedStats(stat_row)
        self.collected_urls.update([url])

    def addToCollectedStats(self, stat_row):
        row_df = pd.DataFrame([stat_row])
        self.collected_stats = pd.concat([self.collected_stats, row_df])


    def getStatisticalValuesDict(self, stat_arr, short_name):
        stat_dict = {}
        for idx, val in enumerate(stat_arr):
            stat_dict[f'{short_name}_{idx}'] = val
        return stat_dict

    def storeCollection(self):
        self.collected_stats.to_csv(FILE_PATH, index=False)

    def collectionRoutine(self):
        for newsname, config in crawldata.items():
            print(f'Processing {newsname}')
            urls = crawler.scrapeArticleLinks(config)
            print(f'= Found {len(urls)} articles')
            for idx, url in enumerate(urls):
                print(f'=== ({idx+1}/{len(urls)}) {url}')
                title = crawler.scrapeHeading(url, config)
                content = crawler.scrapeArticle(url, config)
                if (not title) or (not content):
                    continue
                if (not numSentencesBetween(content, MIN_SENTENCES, MAX_SENTENCES)) or (url in self.collected_urls):
                    continue
                self.collectStats(url, title, content)
            self.storeCollection()
            

