# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IdealistaItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    dateAndTime = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()

    #UBI
    street = scrapy.Field()
    neighborhood = scrapy.Field()
    district = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    province = scrapy.Field()
    #coordinates = scrapy.Field() cannot be extracted-> view(response) does not show the maps image, where the coordinates are

    whoSell = scrapy.Field()
    surface = scrapy.Field()
    nRooms = scrapy.Field()
    features = scrapy.Field()
    pass
