import pandas as pd
import scrapy
import logging
import json

df = pd.read_csv(r'MetacriticScraper\spiders\metacritic.csv')
links = df['link'].values.tolist()
logging.basicConfig(filename='mcScraper2.log', force=True, level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

count = 0

class MetacriticSpider2(scrapy.Spider):
    name = 'mc2'
    allowed_domains = ['metacritic.com']
    download_delay = 0.3
    # needs to be in list format
    start_urls = links
    
    def parse(self, response):
        global count
        # gets the bits of info needed without stripping to prevent exception

        name = response.css('h1::text').get()
        name = name.strip() if name is not None else None

        platform = response.css('span.platform::text').get()
        if name is not None: # if not 404
            if platform.strip() == '':
                platform = response.css('span.platform>a::text').get().strip()
            else:
                platform = platform.strip()
        else:
            platform = None

        numberofuserreviews = response.css('div.userscore_wrap.feature_userscore>div.summary>p>span.count>a::text').get()
        numberofuserreviews = numberofuserreviews.strip() if numberofuserreviews is not None else None
        
        numberofcriticreviews = response.css('div.score_summary.metascore_summary>div.metascore_wrap.highlight_metascore>div.summary>p>span.count>a>span::text').get()
        numberofcriticreviews = numberofcriticreviews.strip() if numberofcriticreviews is not None else None

        genres = response.css('div.details.side_details>ul.summary_details>li.summary_detail.product_genre>span.data::text').getall()
        genres = ', '.join(genres)

        rating = response.css('div.details.side_details>ul.summary_details>li.summary_detail.product_rating>span.data::text').get()
        
        developer = response.css('div.product_data>ul.summary_details>li.summary_detail.publisher>span.data>a::text').get()
        developer = developer.strip() if developer is not None else None
            
        
        if name is None:
            # means page is 404
            yield {
                'name': None,
                'platform': None, 
                'numberofuserreviews': None,
                'numberofcriticreviews': None,
                'genres': None,
                'rating': None,
                'developer': None,
                'url': response.request.url
            }
            count += 1
            logging.info('Count %s', count)
        else:
            yield {
                'name': name,
                'platform': platform, 
                'numberofuserreviews': numberofuserreviews,
                'numberofcriticreviews': numberofcriticreviews,
                'genres': genres,
                'rating': rating,
                'developer': developer,
            }
            count += 1
            logging.info('Count %s', count)
                
#!! cd into MetacriticAnalysis and then .\Scripts\activate to activate venv


# Problem: skipping links
# Reason why: page is deleted, giving 404 code back and therefore skipping
# Solution: accept 404 codes in setting.py of spider

# Problem 2: new scenarios noticed where user and critic is missing but page exists and critic is missing but user exists
# Solution: scrap old method, create new one based on 5 possible scenarios when loading a link and its css

# Problem 3: 4 titles have a missing ' or : when comparing name in first json to second
# Solution: No in script solution, manually fix since only 4 instances

# Problem 4: platform needed to match the json files when merging
# Solution: scrape platform in second spider script

# Problem 5: platform text is sometimes inside a tag, sometimes not
# Solution: add a couple if elses

# After that, converted to csv and compared differences, those that got 404 added name manually and cleaned up names that didn't match, also added platforms to those that were none