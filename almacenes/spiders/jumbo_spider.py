import scrapy
import json
import os

class Jumbo_despensa_Spider(scrapy.Spider):
    name = "jumbo_spider"
    allowed_domains = ["www.tiendasjumbo.co"]
    contador = 1
    start_urls = ["https://www.tiendasjumbo.co/tecnologia"+str(contador)]

    def parse(self, response):
        # Extracción de JSON con data-varname="__STATE__"
        script_text = response.xpath('//template[@data-varname="__STATE__"]/script/text()').get()

        # Se busca que tenga texto
        if script_text:
            # Se intenta buscar el JSON específico
            start_index = script_text.find('{')
            end_index = script_text.rfind('}')
            
            # Se toma JSON
            if start_index != -1 and end_index != -1:
                json_str = script_text[start_index:end_index + 1]
                
                # Se agrega el objeto
                json_data = json.loads(json_str)
                
                # Se guarda el JSON y se vuelve a abrir - REFACTOR
                filename = 'jumbo.json'
                with open(filename, 'w') as f:
                    json.dump(json_data, f, indent=4)
                self.log(f'Saved JSON data to {filename}')

                with open('jumbo.json', 'r') as file:
                    data = json.load(file)

                #Se buscan y almacenan los id's del producto
                product_ids = []

                for key, value in data.items():
                    if 'productId' in value:
                        product_ids.append(value['productId'])

                # Se buscan los datos de los productos sacando los JSON no importantes
                filtered_products = {}

                for key, value in data.items():
                    if key.startswith("Product:sp-") and key.split("-")[-1] in product_ids:
                        filtered_products[key] = value

                # Loop sobre Id's para encontrar los atributos
                for i in product_ids:
                    product_info = filtered_products['Product:sp-'+str(i)]  
                    description = product_info['description']
                    product_name = product_info['productName']
                    brand = product_info['brand']
                    link = product_info['link']

                    price_range_key = f"$Product:sp-{i}.priceRange.sellingPrice"
                    if price_range_key in data:
                        high_price = data[price_range_key]['highPrice']
                        low_price = data[price_range_key]['lowPrice']
                    else:
                        high_price = "No hay precio disponible"
                        low_price = "No hay precio disponible"

                    # Yield scrapy.Item para devolver bn
                    yield {
                        'Nombre: ': product_name,
                        #'Marca: ': brand,
                        'Descripcion: ': description,
                        'link: ': "https://www.tiendasjumbo.co"+str(link),
                        'precio_alto': high_price,
                        'precio_bajo: ': low_price,
                        'Almacen': "Jumbo",
                    }
                    #print()
                    #print("Nombre: "+str(product_name))
                    #print("Marca: "+str(brand) )
                    #print("Descripción: "+str(description))
                    #print("Link: "+"https://www.tiendasjumbo.co"+str(link))
                    #print("Precio: "+ str(high_price))
                    #print()
                # Eliminar el archivo jumbo.json al finalizar
                os.remove('jumbo.json')

#ESTO YA FUNCIONA ESTA COMENTADO CON EL PROPOSITO DE QUE NO SE TARDE MUCHO CUANDO SCRAPEA

        self.contador += 1
        if self.contador <=50:
            next_page = 'https://www.tiendasjumbo.co/supermercado/despensa?page='+str(self.contador)
            yield response.follow(next_page, callback=self.parse)

