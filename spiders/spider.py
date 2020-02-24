from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

import scrapy
from idealista.items import IdealistaItem

class IdealistaSpider(CrawlSpider):
  name                    =   "idealista"
  allowed_domains         =   ["idealista.com"]
  #handle_httpstatus_list  =   [301, 302]
  item_count = 0
  page_count = 0

  def __init__(self, *a, **kw) :
    super(IdealistaSpider, self).__init__(*a, **kw)

    self.PAGES  = 2

  def start_requests(self) :
    #if not self.PAGES :
    #  raise CloseSpider("ERROR: <PAGES> is not defined [0-]")
    #else :
    #  self.PAGES = int(self.PAGES)

    for page in range(1,self.PAGES+1) :
      URL="https://www.idealista.com/venta-viviendas/madrid-madrid/pagina-%s.htm"
      print("\n","NEWPAGE: ", URL%str(page),"\n")
      yield scrapy.Request(url = URL % str(page), callback = self.parse_urls)

  def parse_urls(self, response ):
    self.page_count += 1
    print "page_count:", self.page_count
    housePages = response.xpath('//a[contains(@class,"item-link")]/@href').extract()
    URL = "https://www.idealista.com"
    for hp in housePages :
      yield scrapy.Request(url = URL+hp, callback = self.parse_results )

  def parse_results(self, response):
    self.log("Iniciando")
    #LIMIT
    """
    self.item_count += 1
    if self.item_count > 10:
        raise CloseSpider('item_exceeded')
    """

    # To extract elements, add them here
    item  = IdealistaItem()

    #TITLE
    title = response.xpath('//span[contains(@class,"main-info__title-main")]/text()').extract_first()
    item['title'] = title.strip()

    #PRICE
    price = response.xpath('//span[contains(@class,"info-data-price")]//text()').extract()
    item['price'] = price[0].strip().replace(".","")

    #SURFACE
    surface = response.xpath('//div[contains(@class,"info-features")]/span[1]//text()').extract()
    item['surface'] = surface[1].strip(".").replace(".","")

    #DESCRIPTION
    #description = response.xpath('//div[contains(@id,"jobDescriptionText")]//text()').extract()
    #description = ' '.join(description)
    #item['description'] = description.replace("\n","").encode('utf-8')

    yield item

