from articlecrawler import crawler
from articlecrawler.crawldata import crawldata
from statistics.StatisticList import StatisticList
from utils import numSentencesBetween

MIN_SENTENCES = 50
MAX_SENTENCES = 100

class Collector:
    def __init__(self):
        self.statlist = list(map(lambda s: s(), StatisticList))

    def collectStats(self, title, content):
        for stat in self.statlist:
            print("=====", stat.SHORT_NAME, stat.collect(title, content))

    def collectionRoutine(self):
        for newsname, config in crawldata.items():
            print(f'Processing {newsname}')
            urls = crawler.scrapeArticleLinks(config)
            print(f'= Found {len(urls)} articles')
            for idx, url in enumerate(urls):
                print(f'=== ({idx}/{len(urls)}) {url}')
                title = crawler.scrapeHeading(url, config)
                content = crawler.scrapeArticle(url, config)
                if not numSentencesBetween(content, MIN_SENTENCES, MAX_SENTENCES):
                    continue
                self.collectStats(title, content)
            

