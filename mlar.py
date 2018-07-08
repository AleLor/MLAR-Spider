# -*- coding: utf-8 -*-
import scrapy
import time

class MlarSpider(scrapy.Spider):
    name = "mlar"
    allowed_domains = ["mercadolibre.com.ar"]
    start_urls = ['https://celulares.mercadolibre.com.ar/']

    def parse(self, response):
    	time.sleep(2)
        SET_SELECTOR = '.results-item'
        for item in response.css(SET_SELECTOR):
        	PRODUCTO_SELECTOR = '.item__info-title span ::text'
        	PRECIO_SELECTOR = '.price-fraction ::text'
        	ENVIO_SELECTOR = '.stack-item-info ::text'
        	IMAGEN_SELECTOR = '.image-content a img'
        	LINK_SELECTOR = '.item__title a::attr(href)'
        	CONDICION_SELECTOR = '.item__condition ::text'
        	IXPATH= '@src'
        	if item.css(IMAGEN_SELECTOR).xpath(IXPATH).extract_first() is None:
        		IXPATH = '@data-src'
        	yield {
        		'producto': item.css(PRODUCTO_SELECTOR).extract_first().replace(',',' '),
               	'precio': item.css(PRECIO_SELECTOR).extract_first(),
               	'envio': item.css(ENVIO_SELECTOR).extract_first(),
                'condicion': item.css(CONDICION_SELECTOR).extract_first().replace(',',' '),
               	'imagen': item.css(IMAGEN_SELECTOR).xpath(IXPATH).extract_first(),
               	'link': item.css(LINK_SELECTOR).extract_first(),
            }

        	NEXT_PAGE_SELECTOR = '.pagination__next a::attr(href)'
        	next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        	if next_page:
        		yield scrapy.Request(
               	response.urljoin(next_page),
             	  	callback=self.parse
            	)	


