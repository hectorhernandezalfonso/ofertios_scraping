# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class AlmacenesPipeline:
    def process_item(self, item, spider):
        return item
    

import psycopg2
import psycopg2

class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        # Connect to the default database (usually 'postgres') to create 'ofertios' database if it doesn't exist
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password"
        )
        conn.autocommit = True
        curr = conn.cursor()

        # Create the 'ofertios' database if it doesn't exist
        curr.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ofertios'")
        exists = curr.fetchone()
        if not exists:
            curr.execute("CREATE DATABASE ofertios")

        conn.close()

        # Connect to the 'ofertios' database
        self.conn = psycopg2.connect(
            host="localhost",
            database="ofertios",
            user="postgres",
            password="password"
        )
        self.curr = self.conn.cursor()

        # Create the 'productos' table if it doesn't exist
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                foto TEXT,
                nombre TEXT,
                descripcion TEXT,
                precio NUMERIC,
                almacen TEXT,
                fecha DATE
            );
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_in_db(item)
        return item

    def store_in_db(self, item):
        # Insert item into the database
        self.curr.execute(
            """INSERT INTO productos (nombre, foto, descripcion, precio, almacen, fecha) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                item.get('name', ''),
                item.get('image', ''),
                item.get('description', ''),  # Adjust as per your item fields
                item.get('low_price', 0),   #Always save the lowest price
                item.get('almacen', ''),
                item.get('fecha', None)  # Assuming 'fecha' is properly formatted for PostgreSQL DATE type
            )
        )
        self.conn.commit()

    def close_spider(self, spider):
        # Close the database connection on spider close
        self.curr.close()
        self.conn.close()

