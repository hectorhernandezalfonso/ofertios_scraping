# Ofertios scraping Project
Testing repository for the scraping of Ofertios project.


## Setup:

Install Scrapy with


    pip install scrapy==2.11.1


## Scraping:

While in the folder that contains the scrapy.cfg execute 

    ./start__scraping.sh



## Database Connection

To modify the database connection go to the pipelines.py file and modify the function:

    SavingToPostgresPipeline
