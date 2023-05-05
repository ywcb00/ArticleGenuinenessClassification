
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
                {'type': 'include', 'name': 'h1', 'attrs':{'class': 'headline'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs':{'class': 'article-content'}},
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
                {'type': 'include', 'name': 'h1', 'attrs':{'data-testid': 'Heading'}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs':{'class': 'article-body__container__3ypuX article-body__over-6-para__1Ov64'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
                {'type': 'exclude', 'name': 'p', 'attrs': {'data-testid': 'Body'}},
                {'type': 'exclude', 'name': 'p', 'attrs': {'data-testid': 'Heading'}},
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    }
}
