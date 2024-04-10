import scrapy
import json
import html
import re

from datetime import datetime



class CarullaSpiderSpider(scrapy.Spider):
    name = "carulla_spider"
    allowed_domains = ["www.carulla.com"]
    contador = 1
    start_urls = ["https://www.carulla.com/tecnologia?page="+str(contador)]

    def parse(self, response):
        # Extracting script containing JSON-LD
        scripts = response.xpath('//script[@type="application/ld+json"]/text()').extract()
        
        for script in scripts:
            # Parsing JSON
            data = json.loads(script)
            
            # Extracting required information
            for item in data.get('itemListElement', []):
                product = item.get('item', {})
                name = product.get('name')
                brand = product.get('brand', {}).get('name')
                description = product.get('description')
                image = product.get('image')
                low_price = None
                high_price = None
                offers = product.get('offers', {})
                if 'lowPrice' in offers:
                    low_price = offers['lowPrice']
                if 'highPrice' in offers:
                    high_price = offers['highPrice']

                if description:
                    description = html.unescape(description)
                    strings = description
                    pattern = re.compile(r'<.*?>|\r|\n')
                    description = pattern.sub('', strings)
                else:
                    description = 'No description'  # Or simply set it to an empty string
                current_date = datetime.now()
                fecha = current_date.strftime('%d-%m-%Y')
                
                yield {
                    'name': name,
#                    'description': description,
                    'image': image,
                    'low_price': low_price,
                    'high_price': high_price,
                    'almacen': "Carulla",
                    'fecha':fecha,
                    # Include other fields as required
                }

        # Right before the end of your parse method
#        self.contador += 1
#        if self.contador <= 70:
#            next_page = f'https://www.carulla.com/tecnologia?page={self.contador}'
#            yield response.follow(next_page, callback=self.parse)
        # No need to reset contador to 0 here unless it's used elsewhere for a similar purpose
