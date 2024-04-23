#ESTA MKDA SACARLA COMO

#scrapy crawl olimpica_spider -o output.json

import scrapy
from datetime import datetime
from datetime import date

class Olimpica_despensa_Spider(scrapy.Spider):

    #CLASE PARECE ESCALABLE AL MODIFICAR start_urls PARA SCRAPEAR LAS DEMÁS URL QUE MUESTREN PRODUCTOS COMO DESPENSA
    #PENDIENTE DE TESTEO DE ESCALABILIDAD


    name = "olimpica_spider"
    allowed_domains = ["www.olimpica.com"]
    contador = 1
    start_urls = ["https://www.olimpica.com/electrodomesticos-y-tecnologia/accesorios-de-informatica/computadores?page="+str(contador),
                  "https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/neveras?page="+str(contador),
                  "https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/lavadoras?page="+str(contador),
                  "https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/aires-acondicionados?page="+str(contador),
                  #"https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/estufas-y-empotrables?page="+str(contador),
                  #"https://www.olimpica.com/cuidado-personal?page="+str(contador),
                  #"https://www.olimpica.com/electrodomesticos-y-tecnologia/comunicaciones/celulares?page="+str(contador),
                  #"https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/pequenos-electrodomesticos?page="+str(contador),
                  #"https://www.olimpica.com/electrodomesticos-y-tecnologia/tv-audio-y-video/televisores?page="+str(contador),
                  #"https://www.olimpica.com/electrodomesticos-y-tecnologia/accesorios-de-informatica/impresoras-y-suministros?page="+str(contador),
                  #"https://www.olimpica.com/electrodomesticos-y-tecnologia/tv-audio-y-video/equipos-de-audio/aiwa/bose/jbl/lg/olimpo/samsung/sonos?initialMap=c,c,c&initialQuery=electrodomesticos-y-tecnologia/tv-audio-y-video/equipos-de-audio&map=category-1,category-2,category-3,brand,brand,brand,brand,brand,brand,brand&order=OrderByTopSaleDESC?page="+str(contador),
                  #"https://www.olimpica.com/16372?map=productClusterIds?page="+str(contador),
                  ]


    def parser_precios(self, prices, url):
        #Esto trata los precios largos de millones
        if url in ["https://www.olimpica.com/electrodomesticos-y-tecnologia/accesorios-de-informatica/computadores?page=",
                   "https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/neveras?page="]:
        
            if len(prices) >= 10:
                precio_original = str(prices[0]) + str(prices[1]) + str(prices[2])
                precio_descuento =  str(prices[3]) + str(prices[4]) + str(prices[5])
                return (precio_original, precio_descuento)
            else:
                precio_original = str(prices[0]) + str(prices[1]) + str(prices[2])
                precio_descuento = "Sin descuento"

            return (precio_original, precio_descuento)
        
        if url in ["https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/lavadoras?page=",
                   "https://www.olimpica.com/electrodomesticos-y-tecnologia/electro-hogar/aires-acondicionados?page=",
                   "https://www.olimpica.com/electrodomesticos-y-tecnologia/comunicaciones/celulares?page=",
                   "https://www.olimpica.com/electrodomesticos-y-tecnologia/tv-audio-y-video/televisores?page=",
                   
                   
                   ]:
            if len(prices) >= 10:
                precio_original = str(prices[0]) + str(prices[1]) + str(prices[2])
                precio_descuento =  str(prices[3]) + str(prices[4]) + str(prices[5])
                return (precio_original, precio_descuento)
            
            if len(prices) == 9:
                precio_original = str(prices[0]) + str(prices[1]) + str(prices[2])
                precio_descuento =  str(prices[3]) + str(prices[4])
                return (precio_original, precio_descuento)

            if len(prices) >=7:
                precio_original = str(prices[0]) + str(prices[1])
                precio_descuento =  str(prices[2]) + str(prices[3])
                return (precio_original, precio_descuento)
            else:
                precio_original = str(prices[0]) + str(prices[1]) + str(prices[2])
                precio_descuento = "Sin descuento"
                return (precio_original, precio_descuento)
        
        return (0, 0)

    def parse(self, response):
        if self.contador<10:
            url = response.url
            url = url[:len(url)-1]
        if self.contador >= 10:
            url = response.url
            url = url[:len(url)-2]

        #Selecciona todos los productos del HTML
        productos = response.xpath("//a[@class='vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--product-summary h-100 flex flex-column']")
        

        
        for producto in productos:
            #Selecciona, filtra y almacena los precios originales y de descuento si los hay.

            prices = producto.xpath(".//span[@class='vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--summary']/text()")
            price_values = [price.get() for price in prices]
            print(price_values)
            precio_original, precio_descuento = self.parser_precios(price_values,url)
            
            
            #Agrega fecha
            current_date = datetime.now()
            fecha = current_date.strftime('%d-%m-%Y')

            
            #Selecciona los campos faltantes y devuelve todo en ese formato
            yield {
            'Nombre': producto.css('div.vtex-product-summary-2-x-nameContainer h3 span::text').get(),
            'Precio original': precio_original,
            'Precio descuento': precio_descuento,
            'Almacen': "Olimpica",
            'Fecha': str(date.today()),
            
        }
            
#Esta sección es funcional y permite el scrapeo de las páginas enteras, está comentada para scrapear solo la primera página

        self.contador += 1
        if self.contador > 50:
            self.contador = 0
        if self.contador <=50:
            next_page = url+ str(self.contador)
            yield response.follow(next_page, callback=self.parse)
        if self.contador > 50:
            self.contador = 0

            
#"""
            
