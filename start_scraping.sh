#!/bin/bash

scrapy crawl carulla_spider -o carulla_productos.json
scrapy crawl olimpica_spider -o olimpica_productos.json
python almacenes/spiders/alkosto_selenium.py