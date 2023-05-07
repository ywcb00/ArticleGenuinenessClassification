#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from .crawldata import crawldata
from functools import partial
import re

# Instructed by https://towardsdatascience.com/scraping-1000s-of-news-articles-using-10-simple-steps-d57636a49755

# https://www.foxnews.com/politics <header class="info-header>"
#   --> <a href="/politics/newslink...></a>"
#       foxnews article: <p></p> or <p class="speakable"></p>

def scrapeArticleLinks(config):
    al_conf = config['article-links']
    links = set()
    for o_url in al_conf['overview-urls']:
        url = f'{config["url-prefix"]}{o_url}'
        try:
            page = requests.get(url)
        except Exception as e:
            print(e)
        soup = BeautifulSoup(page.text, 'html.parser')
        linkcontainer = filterTags(al_conf['find-tags'], soup.find())
        tmp_links = set()
        for lc in linkcontainer:
            if 'href' in lc.attrs:
                tmp_links.add(lc['href'].strip())
        links.update(filter(lambda l: l.startswith(al_conf['link-prefix']), tmp_links))
    links = set(map(lambda l: f'{config["url-prefix"]}{l}', links))
    return links

def filterTags(ft_conf, tag):
    tags = [tag]
    for ft in ft_conf:
        if(ft['type'] == 'include'):
            tags = [t.find_all(ft['name'], attrs=ft['attrs']) for t in tags]
            tags = [t for tl in tags for t in tl]
        elif(ft['type'] == 'exclude'):
            tags = filter(partial(excludeTagFilter, ft), tags)
        elif(ft['type'] == 'excludeParent'):
            tags = filter(partial(excludeParentTagFilter, ft), tags)
        else:
            print(f'Type {ft["type"]} not known')
    return tags

def excludeTagFilter(excludeDict, tag):
    if(tag.name != excludeDict['name']):
        return True
    if(excludeDict['attrs'] == {}):
        return True
    for akey, aval in excludeDict['attrs'].items():
        if(not (akey in tag.attrs and tag.attrs[akey] == aval)):
            return True
    return False

def excludeParentTagFilter(excludeDict, tag):
    matching_tags = tag.find_parent(excludeDict['name'], attrs=excludeDict['attrs'])
    if(matching_tags):
        return False
    else:
        return True

def scrapeHeading(url, config):
    h_conf = config['heading']
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    soup = BeautifulSoup(page.text, 'html.parser')

    paragraphs = filterTags(h_conf['find-tags'], soup.find())
    # print('\n\n'.join(list(map(lambda p: p.prettify(), paragraphs))))
    paragraphs = map(lambda p: p.get_text(), paragraphs)
    paragraphs = filter(lambda p: p != None, paragraphs)
    return list(paragraphs)[0]

def scrapeArticle(url, config):
    a_conf = config['article']
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    soup = BeautifulSoup(page.text, 'html.parser')

    paragraphs = filterTags(a_conf['find-tags'], soup.find())
    # print('\n\n'.join(list(map(lambda p: p.prettify(), paragraphs))))
    paragraphs = map(lambda p: p.get_text(), paragraphs)
    paragraphs = filter(lambda p: p != None, paragraphs)
    for rf in a_conf['regex-filter']:
        pattern = re.compile(rf)
        paragraphs = filter(lambda p: bool(pattern.match(p)), paragraphs)
    return '\n'.join(paragraphs)



def main():
    # Example for scraping the links to the articles from one source
    config = crawldata['foxnews']
    urls = scrapeArticleLinks(config)

    # Example for scraping one article
    u = urls.pop()
    heading = scrapeHeading(u, config)
    article = scrapeArticle(u, config)
    print('\n\n'.join([u, heading, article]))


if __name__ == '__main__':
    main()
