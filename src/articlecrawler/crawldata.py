
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
            'link-prefix': ('/news/world-')
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
    'nytimes': {
        'url-prefix': 'https://www.nytimes.com',
        'article-links': {
            'overview-urls': ['/section/world', '/section/sports', '/section/science', '/section/us', '/section/politics', '/section/technology'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'a', 'attrs': {}},
            ],
            'link-prefix': ('/202')
        },
        'heading': {
            'driver': 'Firefox',
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'h1', 'attrs': {'data-testid': 'headline'}}
            ]
        },
        'article': {
            'driver': 'Firefox',
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'section', 'attrs': {'name': 'articleBody'}},
                {'type': 'include', 'name': 'p', 'attrs': {}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'npr': {
        'url-prefix': 'https://www.npr.org',
        'article-links': {
            'overview-urls': ['/sections/world', '/sections/national', '/sections/politics', '/sections/business', '/sections/climate', '/sections/science', '/sections/health'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'item-info'}},
                {'type': 'include', 'name': 'a', 'attrs': {}},
            ],
            'link-prefix': ('https://www.npr.org/202')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {'class': 'story'}},
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'storytitle'}},
                {'type': 'include', 'name': 'h1', 'attrs': {}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {'class': 'story'}},
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'storytext'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
                {'type': 'excludeParent', 'name': 'div', 'attrs': {'class': 'caption'}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'theguardian': {
        'url-prefix': 'https://theguardian.com',
        'article-links': {
            'overview-urls': ['/world', '/uk-news', '/environment', '/science', '/global-development', '/football', '/technology', '/business'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'main', 'attrs': {'id': 'maincontent'}},
                {'type': 'include', 'name': 'a', 'attrs': {}},
            ],
            'link-prefix': ('/world/', '/uk-news/', '/environment/', '/science/', '/global-development/', '/football/', '/technology/', '/business/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {}},
                {'type': 'include', 'name': 'div', 'attrs': {'data-gu-name': 'headline'}},
                {'type': 'include', 'name': 'h1', 'attrs': {}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {}},
                {'type': 'include', 'name': 'div', 'attrs': {'data-gu-name': 'body'}},
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'maincontent'}},
                {'type': 'include', 'name': 'p', 'attrs': {}},
                {'type': 'excludeParent', 'name': 'ul', 'attrs': {}},
                {'type': 'excludeParent', 'name': 'div', 'attrs': {'class': 'ad-slot-container '}},
                {'type': 'excludeParent', 'name': 'figure', 'attrs': {}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
# === Begin of evaluation section
    'nbcnews': {
        'url-prefix': 'https://www.nbcnews.com',
        'article-links': {
            'overview-urls': ['/us-news', '/politics', '/world', '/opinion', '/tech-media', '/health'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'layout-grid-item'}},
                {'type': 'include', 'name': 'h2', 'attrs': {}},
                {'type': 'include', 'name': 'a', 'attrs': {}}
            ],
            'link-prefix': ('https://www.nbcnews.com/us-news', 'https://www.nbcnews.com/politics', 'https://www.nbcnews.com/world', 'https://www.nbcnews.com/opinion', 'https://www.nbcnews.com/tech-media', 'https://www.nbcnews.com/health')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {}},
                {'type': 'include', 'name': 'header', 'attrs': {}},
                {'type': 'include', 'name': 'h1', 'attrs': {}}
            ]
        },
        'article': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {}},
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'article-body'}},
                {'type': 'include', 'name': 'p', 'attrs': {}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'sciencedaily': {
        'url-prefix': 'https://www.sciencedaily.com',
        'article-links': {
            'driver': 'Firefox',
            'overview-urls': ['/news/health_medicine', '/news/mind_brain', '/news/living_well', '/news/matter_energy', '/news/space_time', '/news/computers_math', '/news/plants_animals', '/news/earth_climate', '/news/fossil_ruins', '/news/science_society', '/news/business_industry', '/news/education_learning'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'contents'}},
                {'type': 'include', 'name': 'a', 'attrs': {}}
            ],
            'link-prefix': ('/releases/202')
        },
        'heading': {
            'driver': 'Firefox',
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'contents'}},
                {'type': 'include', 'name': 'h1', 'attrs': {'id': 'headline'}}
            ]
        },
        'article': {
            'driver': 'Firefox',
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'contents'}},
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'story_text'}},
                {'type': 'include', 'name': 'p', 'attrs': {}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
    'pcmag': {
        'url-prefix': 'https://uk.pcmag.com',
        'article-links': {
            'overview-urls': ['/article/news'],
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'article', 'attrs': {'class': 'articlewrapper'}},
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'articlecontainer'}},
                {'type': 'include', 'name': 'a', 'attrs': {}}
            ],
            'link-prefix': ('/')
        },
        'heading': {
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'class': 'hero'}},
                {'type': 'include', 'name': 'hgroup', 'attrs': {}},
                {'type': 'include', 'name': 'h1', 'attrs': {'id': 'id_title'}}
            ]
        },
        'article': {
            'driver': 'Firefox',
            'find-tags': [ # Hierarchy
                {'type': 'include', 'name': 'div', 'attrs': {'id': 'content'}},
                {'type': 'include', 'name': 'article', 'attrs': {'class': 'article'}},
                {'type': 'include', 'name': 'p', 'attrs': {}}
            ],
            'regex-filter': ['.*[a-z]+.*$']
        }
    },
#    #the sun 
#     'thesun': {
#         'url-prefix': 'https://www.thesun.co.uk',
#         'article-links': {
#             'overview-urls': ['/tech', '/health', '/news', '/money', '/sport'],
#             'find-tags': [
#                 {'type': 'include', 'name': 'a', 'attrs': {'class': 't-p-color__hover'}}
#             ],
#             'link-prefix': ('https://www.thesun.co.uk/tech/', 'https://www.thesun.co.uk/health/', 'https://www.thesun.co.uk/news/', 'https://www.thesun.co.uk/money/', 'https://www.thesun.co.uk/sport/')
#         },
#         'heading': {
#             'find-tags': [
#                 {'type': 'include', 'name': 'h1', 'attrs': {'class': 'article__headline'}}
#             ]
#         },
#         'article': {
#             'find-tags': [
#                 {'type': 'include', 'name': 'div', 'attrs': {'class': 'article__content'}},
#                 {'type': 'include', 'name': 'p', 'attrs': {}}
#             ],
#             'regex-filter': ['.*[a-z]+.*$']
#         }
#     },
#     'dailymail': {
#     'url-prefix': 'https://www.dailymail.co.uk',
#     'article-links': {
#         'overview-urls': ['/sport', '/royals', '/news', '/femail', '/health'],
#         'find-tags': [
#             {'type': 'include', 'name': 'a', 'attrs': {'href': lambda value: value and value.endswith('.html')}},
#             {'type': 'include', 'name': 'h2', 'attrs': {'class': 'linkro-darkred'}}
#         ],
#         'link-prefix': ('https://www.dailymail.co.uk', 'https://www.dailymail.co.uk', 'https://www.dailymail.co.uk', 'https://www.dailymail.co.uk', 'https://www.dailymail.co.uk')
#     },
#     'heading': {
#         'find-tags': [
#             {'type': 'include', 'name': 'h2', 'attrs': {'class': 'linkro-darkred'}}
#         ]
#     },
#     'article': {
#         'find-tags': [
#             {'type': 'include', 'name': 'div', 'attrs': {'class': 'articletext-holder'}},
#             {'type': 'include', 'name': 'p', 'attrs': {}}
#         ],
#         'regex-filter': ['.*[a-z]+.*$']
#     }
# }
}
