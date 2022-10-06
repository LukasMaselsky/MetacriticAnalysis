from itertools import count
import scrapy
import logging

logging.basicConfig(filename='mcScraper.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
count = 0

class MetacriticSpider(scrapy.Spider):
    
    name = 'mc'
    allowed_domains = ['metacritic.com']
    start_urls = ['https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0']

    def parse(self, response):
        global count
        for games in response.css('tr'):
            # checks if item is none to skip it
            if games.css('a.title>h3::text').get() == None:
                continue
            else:
                yield {
                    'name': games.css('a.title>h3::text').get().strip(),
                    'platform': games.css('span.data::text').get().strip(),
                    'date': games.css('div.clamp-details>span::text').get().strip(),
                    'image': games.xpath('td/a/img').attrib['src'],
                    'summary': games.css('div.summary::text').get().strip(),
                    'metascore': games.css('div.clamp-metascore>a.metascore_anchor>div::text').get().strip(),
                    'userscore': games.css('div.clamp-userscore>a.metascore_anchor>div::text').get().strip(),
                    'link': 'https://www.metacritic.com'+ games.css('a.title').attrib['href']
                }
                count += 1
                logging.info('Count %s', count)


        nextPage = response.css('a[rel="next"]').attrib['href']
        if nextPage is not None:
            nextPage = 'https://www.metacritic.com' + str(nextPage) # concatanate into full URL
            yield response.follow(nextPage, callback=self.parse)


        
