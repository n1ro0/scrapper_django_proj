# -*- coding: utf-8 -*-
import scrapy, re, datetime
from products_scraper import items
from urllib.parse import parse_qs
from scrapy_redis.spiders import RedisSpider



class LordandtaylorSpider(RedisSpider):
    name = 'lordandtaylor'
    id = 0
    price_id = 0
    domain = 'http://www.lordandtaylor.com'
    #allowed_domains = ['http://www.lordandtaylor.com']
    start_urls = ['http://www.lordandtaylor.com/Women/shop/_/N-4zteyp/Ne-6ja3o7']

    def __init__(self, url='http://www.lordandtaylor.com/Women/shop/_/N-4zteyp/Ne-6ja3o7', *args, **kwargs):
        super(LordandtaylorSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]


    def parse(self, response):
        categories = response.xpath('//ul[contains(@class, "perpetual") and contains(@class, "left-nav-group-container")]/li/a')
        for category in categories:
            #link = category.xpath('@href').extract_first()
            name = category.xpath('text()').extract_first()
            yield response.follow(category, meta={'categories': [name]}, callback=self.parse_category)

    def parse_category(self, response):
        categories = response.xpath(
            '//li[contains(@class, "left-nav-list-show")]/ul/li/a[not(contains(@class, "selected"))]')
        for category in categories:
            name = category.xpath('text()').extract_first().strip('\n\t')
            new_meta = {'categories': [item for item in response.meta['categories']]}
            new_meta['categories'].append(name)
            yield response.follow(category, meta=new_meta, callback=self.parse_subcategory_page)

    def parse_subcategory_page(self, response):
        products = response.xpath(
            '//div[contains(@class, "image-container-large")]/a[1]/@href')
        next_page = response.xpath(
            '//li[contains(@class,"pa-enh-pagination-right-arrow") and not(span[contains(@class,"pa-enh-pagination-arrow-diabled")])]/a/@href').extract_first()
        for product in products:
            yield response.follow(url=product, meta=response.meta, callback=self.parse_product_details, dont_filter=True)
        if next_page:
            yield response.follow(url=next_page, meta=response.meta, callback=self.parse_subcategory_page, dont_filter=True)

    def parse_product_details(self, response):
        product = self.parse_product(response)
        yield product
        price = float(response.xpath(
            '//dl[contains(@class, "product-pricing__container")]//span[@itemprop="price"]/text()').extract_first()
                      .replace(',', ''))
        colors = response.xpath(
        '//ul[contains(@class,"product-variant-attribute-values")]/li[contains(@class, "product-variant-attribute-value--swatch")]/span/text()')
        sizes = response.xpath(
            '//ul[contains(@class,"product-variant-attribute-values")]/li[contains(@class, "product-variant-attribute-value--text")]/span/text()')
        for size in sizes:
            for color in colors:
                price_item = self.parse_price(response, product['site_product_id'], product['id'], price, size, color)
                yield price_item



    def parse_product(self, response):
        item = items.ProductItem()
        item['site_product_id'] = parse_qs(response.url.split("?")[-1]).get("PRODUCT<>prd_id")[0]
        item['id'] = self.id
        self.id += 1
        item['brand'] = response.xpath('//h2[contains(@class, "product-overview__brand")]/a/text()').extract_first()
        item['name'] = response.xpath(
            '//h1[contains(@class, "product-overview__short-description")]/text()').extract_first()
        item['categories'] = response.meta['categories']
        item['description'] = '\n'.join(
            response.xpath('//section[contains(@class, "product-description")]//ul//text()').extract())
        item['url'] = response.url
        item['site'] = 'www.lordandtaylor.com'
        return item

    def parse_price(self, response, site_product_id, product_id, price, size, color):
        price_item = items.ProductPriceItem()
        price_item['id'] = self.price_id
        self.price_id += 1
        price_item['product_id'] = product_id
        price_item['site_product_id'] = site_product_id
        price_item['price'] = price
        price_item['color'] = color.extract()
        price_item['size'] = size.extract()
        price_item['stock_state'] = "In stock"
        price_item['date'] = datetime.datetime.now()
        return price_item