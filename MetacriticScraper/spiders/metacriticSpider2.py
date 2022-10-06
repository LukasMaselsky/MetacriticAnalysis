import pandas as pd
import scrapy
import logging

df = pd.read_csv(r'C:\Users\kukub\Documents\Coding\metacriticScraper\metacriticScraper\spiders\metacritic.csv')
links = df['link'].values.tolist()
logging.basicConfig(filename='mcScraper2.log', force=True, level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
count = 0

class MetacriticSpider2(scrapy.Spider):
    name = 'mc2'
    allowed_domains = ['metacritic.com']
    download_delay = 0.2
    start_urls = links
    
    def parse(self, response):
        global count
        # gets the 3 bits of info needed without stripping to prevent exception
        name = response.css('h1::text').get()
        platform = response.css('span.platform::text').get()
        numberofuserreviews = response.css('div.userscore_wrap.feature_userscore>div.summary>p>span.count>a::text').get()
        numberofcriticreviews = response.css('div.score_summary.metascore_summary>div.metascore_wrap.highlight_metascore>div.summary>p>span.count>a>span::text').get()
        
        # 5 scenarios 
        if name is None:
            # means page is 404
            yield {
                'name': None,
                'platform': None, 
                'numberofuserreviews': None,
                'numberofcriticreviews': None,
                'url': response.request.url
            }
            count += 1
            logging.info('Count %s', count)
        elif numberofuserreviews is None and numberofcriticreviews is None:
            # both crit and user reviews are empty but not a 404
            if platform.strip() == '':
                yield {
                    'name': name.strip(), 
                    'platform': response.css('span.platform>a::text').get().strip(),
                    'numberofuserreviews': None,
                    'numberofcriticreviews': None
                }
                count += 1
                logging.info('Count %s', count)
            else:
                yield {
                    'name': name.strip(), 
                    'platform': platform.strip(),
                    'numberofuserreviews': None,
                    'numberofcriticreviews': None
                }
                count += 1
                logging.info('Count %s', count)
        elif numberofuserreviews is None:
            if platform.strip() == '':
                yield {
                    'name': name.strip(), 
                    'platform': response.css('span.platform>a::text').get().strip(),
                    'numberofuserreviews': None,
                    'numberofcriticreviews': numberofcriticreviews.strip()
                }
                count += 1
                logging.info('Count %s', count)
            else:
                yield {
                    'name': name.strip(), 
                    'platform': platform.strip(),
                    'numberofuserreviews': None,
                    'numberofcriticreviews': numberofcriticreviews.strip()
                }
                count += 1
                logging.info('Count %s', count)
        elif numberofcriticreviews is None:
            if platform.strip() == '':   
                yield {
                    'name': name.strip(), 
                    'platform': response.css('span.platform>a::text').get().strip(),
                    'numberofuserreviews': numberofuserreviews.strip(),
                    'numberofcriticreviews': None
                }
                count += 1
                logging.info('Count %s', count)
            else:
                yield {
                    'name': name.strip(), 
                    'platform': platform.strip(),
                    'numberofuserreviews': numberofuserreviews.strip(),
                    'numberofcriticreviews': None
                }
                count += 1
                logging.info('Count %s', count)
        else:
            # everthing is fine, scrape all fields
            if platform.strip() == '':
                yield {
                    'name': name.strip(),
                    'platform': response.css('span.platform>a::text').get().strip(),
                    'numberofuserreviews': numberofuserreviews.strip(),
                    'numberofcriticreviews': numberofcriticreviews.strip()
                }     
                count += 1
                logging.info('Count %s', count)
            else:
                yield {
                    'name': name.strip(),
                    'platform': platform.strip(),
                    'numberofuserreviews': numberofuserreviews.strip(),
                    'numberofcriticreviews': numberofcriticreviews.strip()
                }     
                count += 1
                logging.info('Count %s', count)
                


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
