
crawldata = {
    'foxnews': {
        'url-prefix': 'https://www.foxnews.com',
        'article-links': {
            'overview-urls': ['/us', '/politics', '/world', '/opinion', '/sports'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'header', 'attrs': {'class': 'info-header'}},
                {'type': 'include', 'name': 'a', 'attrs': {}}
            ],
            'link-prefix': ('/us/', '/politics/', '/world/', '/opinion/', '/sports/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'h1', 'attrs': {'class': 'headline'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'article-content'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
                {'type': 'excludeParent', 'name': 'div', 'attrs': {'class': 'caption'}},
                {'type': 'exclude', 'name': 'p', 'attrs': {'class': 'copyright'}},
                {'type': 'exclude', 'name': 'p', 'attrs': {'data-v-b8a95802': ''}},
                {'type': 'excludeParent', 'name': 'div', 'attrs': {'class': 'article-meta'}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'reuters': {
        'url-prefix': 'https://reuters.com',
        'article-links': {
            'overview-urls': ['/world', '/business', '/markets', '/legal', '/technology', '/sports'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'data-testid': 'MediaStoryCard'}},
                {'type': 'include', 'name': 'a', 'attrs': {'data-testid': 'Heading'}}
            ],
            'link-prefix': ('/world/', '/business/', '/markets/', '/legal/', '/technology/', '/sports/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'h1', 'attrs': {'data-testid': 'Heading'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'article-body__container__3ypuX article-body__over-6-para__1Ov64'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
                {'type': 'exclude', 'name': 'p', 'attrs': {'data-testid': 'Body'}},
                {'type': 'exclude', 'name': 'p', 'attrs': {'data-testid': 'Heading'}},
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'cnn': {
        'url-prefix': 'https://edition.cnn.com',
        'article-links': {
            'overview-urls': ['/us', '/world', '/politics', '/business', '/health', '/entertainment', '/style', '/travel', '/sports'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'a', 'attrs': {'data-link-type': 'article'}}
            ],
            'link-prefix': ('/us/', '/world/', '/politics/', '/business/', '/health/', '/entertainment/', '/style/', '/travel/', '/sports/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'headline__wrapper'}},
                {'type': 'include', 'name': 'h1', 'attrs': {'data-editable': 'headlineText'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'article__content'}},
                {'type': 'include', 'name': 'p', 'attrs': {'data-component-name': 'paragraph'}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'cnn-page': {
        'url-prefix': 'https://edition.cnn.com',
        'article-links': {
            'overview-urls': ['/us', '/world', '/politics', '/business', '/health', '/entertainment', '/style', '/travel', '/sports'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'a', 'attrs': {'data-link-type': 'article'}}
            ],
            'link-prefix': ('/us/', '/world/', '/politics/', '/business/', '/health/', '/entertainment/', '/style/', '/travel/', '/sports/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'PageHead__component'}},
                {'type': 'include', 'name': 'h1', 'attrs': {'class': 'PageHead__title'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'BasicArticle__main'}},
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'Paragraph__component BasicArticle__paragraph BasicArticle__pad'}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'bbc': {
        'url-prefix': 'https://www.bbc.com',
        'article-links': {
            'overview-urls': ['/news/world'],
            'find-tags': [ 
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'index-page'}},
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'gel-layout__item'}},
                {'type': 'include', 'name': 'a', 'attrs': {}},
            ],
            'link-prefix': ('/news/world')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'h1', 'attrs': {'id': 'main-heading'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'data-component': 'text-block'}},
                {'type': 'include', 'name': 'p', 'attrs': {}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
        'bloomberg': {
        'url-prefix': 'https://www.bloomberg.com',
        'article-links': {
            'overview-urls': ['/markets', '/technology', '/politics', '/world'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'header', 'attrs': {'class': 'story-package-module_ _stories'}},
                {'type': 'include', 'name': 'a', 'attrs': {'class': 'story-package-module_ _story_ _headline-link'}}
            ],
            'link-prefix': ('/news/articles/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'h1', 'attrs': {'class': 'lede-text-v2_ _hed'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'body-copy-v2 fence-body'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
                {'type': 'excludeParent', 'name': 'div', 'attrs': {'class': 'bb-unsupported-inset'}},
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'washingtonpost': {
        'url-prefix': 'https://www.washingtonpost.com',
        'article-links': {
            'overview-urls': ['/politics', '/world', '/business', '/technology', '/sports'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'header', 'attrs': {'class': 'headline'}},
                {'type': 'include', 'name': 'a', 'attrs': {}}
            ],
            'link-prefix': ('/2023/05/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'h1', 'attrs': {'data-qa': 'headline'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {'itemprop': 'articleBody'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    }
}
