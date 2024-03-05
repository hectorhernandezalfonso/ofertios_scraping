import scrapy
from datetime import datetime

class Olimpica_despensa_Spider(scrapy.Spider):

    #CLASE PARECE ESCALABLE AL MODIFICAR start_urls PARA SCRAPEAR LAS DEMÁS URL QUE MUESTREN PRODUCTOS COMO DESPENSA
    #PENDIENTE DE TESTEO DE ESCALABILIDAD


    name = "olimpica_spider"
    allowed_domains = ["www.olimpica.com"]
    contador = 1
    start_urls = ["https://www.olimpica.com/supermercado/despensa?page="+str(contador)]

    def parse(self, response):
        #Selecciona todos los productos del HTML
        productos = response.xpath("//a[@class='vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--product-summary h-100 flex flex-column']")
        

        
        for producto in productos:
            #Selecciona, filtra y almacena los precios originales y de descuento si los hay.

            prices = producto.xpath(".//span[@class='vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--summary']/text()")
            price_values = [price.get() for price in prices]
            precio_original = []
            precio_descuento = []
            
            if len(price_values) >= 4:
                precio_original = price_values[0]+price_values[1]
                precio_descuento = price_values[2]+price_values[3]
            else:
                precio_original = price_values[0]+price_values[1]
                precio_descuento = 'Sin descuento'
            
            
            #Agrega fecha
            current_date = datetime.now()
            fecha = current_date.strftime('%d-%m-%Y')

            #Selecciona los campos faltantes y devuelve todo en ese formato
            yield{
                'Nombre': producto.css('div.vtex-product-summary-2-x-nameContainer h3 span::text').get(),
                'Precio original': precio_original,
                'Precio descuento': precio_descuento,
                'URL':  'https://www.olimpica.com'+str(producto.css('a.vtex-product-summary-2-x-clearLink').attrib['href']), 
                'Fecha': fecha,
            }
"""
Esta sección es funcional y permite el scrapeo de las páginas enteras, está comentada para scrapear solo la primera página

        self.contador += 1
        if self.contador <=50:
            next_page = 'https://www.olimpica.com/supermercado/despensa?page='+ str(self.contador)
            yield response.follow(next_page, callback=self.parse)

"""
            
