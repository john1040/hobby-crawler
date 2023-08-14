import scrapy

class WingsToysSpider(scrapy.Spider):
    name = "wings_toys"
    start_urls = ('https://www.wingstoys.com.tw/product/all?page={}'.format(i) for i in range(1,81))

    

    def parse(self, response):
        # Extract links to individual product pages from each <li> tag
        
        for products in response.css('a.pt_items_block'):
            # try:
                link = products.css('a.pt_items_block').attrib['href']
                name = products.css('h4.pt_title::text').get().replace('\n                            ','')
                price = 'sold out'
                if products.css('h5.js_origin_price::text').get():
                    price = products.css('h5.js_origin_price::text').get().replace('$','')
                yield response.follow(link, self.parse_quantity, meta={'name': name, 'price': price})
            # except:
            #     link = products.css('a.pt_items_block').attrib['href']
            #     name = products.css('h4.pt_title::text').get().replace('\n                            ','')
            #     price = 'sold out'
            #     yield {
            #         'name': products.css('h4.pt_title::text').get(),
            #         'price': 'sold out',
            #         'link': products.css('a.pt_items_block').attrib['href'],
            #         'quantity': 0,
            #     }  
            # try:
            #     link = products.css('a.pt_items_block').attrib['href']
            #     name = products.css('h4.pt_title::text').get()
            #     price = products.css('h5.js_origin_price::text').get().replace('$','')
            #     # q = response.follow(link, self.parse_quantity(link=link,name=name,price=price))  
            #     yield {
            #         'name': products.css('h4.pt_title::text').get(),
            #         'price': products.css('h5.js_origin_price::text').get().replace('$',''),
            #         'link': products.css('a.pt_items_block').attrib['href'],
            #         # 'q':q,

            #     }
            # except:
            #     yield {
            #         'name': products.css('h4.pt_title::text').get(),
            #         'price': 'sold out',
            #         'link': products.css('a.pt_items_block').attrib['href'],

            #     }  

    def parse_quantity(self, response):
        try: 
            quantity = response.css('input.qty_value').attrib['data-max']
            discount = response.css('span.js_onsale_price_span::text').get()
            # print('TESTSTSTST', discount)
            # if discount:
            #     print('JOJO', discount)
            name = response.request.meta['name']
            # price = response.request.meta['price']
            yield {
                'name': name,
                'price': discount,
                'url': response.url,
                'quantity': quantity,
                # 'discount': discount,
            }
        except:
            quantity = '0'
            name = response.request.meta['name']
            price = response.request.meta['price']
            yield {
                'name': name,
                'price': price,
                'url': response.url,
                'quantity': quantity,
            } 
        # try:
        #     yield {
        #         'name': name,
        #         'price': price,
        #         'link': link,
        #         'quantity': quantity,
        #     }
        # except:
        #     yield {
        #         'name': name,
        #         'price': 'sold out',
        #         'link': link,

        #     }  
