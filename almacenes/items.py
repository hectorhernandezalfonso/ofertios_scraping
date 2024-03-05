# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlmacenesItem(scrapy.Item):
    nombre = scrapy.Field()
    categoria = scrapy.Field()
    precio = scrapy.Field()
    fecha = scrapy.Field()

    pass
