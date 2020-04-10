from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from datetime import datetime

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

    regions = ["a-coruna-provincia", "alava", "albacete-provincia", "alicante", "almeria-provincia",
               "andorra-provincia", "asturias", "avila-provincia", "badajoz-provincia", "balears-illes",
               "barcelona-provincia", "burgos-provincia", "caceres-provincia", "cadiz-provincia", "cantabria",
               "castellon", "cerdanya-francesa", "ceuta-ceuta", "ciudad-real-provincia", "cordoba-provincia",
               "cuenca-provincia", "girona-provincia", "granada-provincia", "guadalajara-provincia", "guipuzcoa",
               "huelva-provincia", "huesca-provincia", "jaen-provincia", "la-rioja", "las-palmas", "leon-provincia",
               "lleida-provincia", "lugo-provincia", "madrid-provincia", "malaga-provincia", "melilla-melilla",
               "murcia-provincia", "navarra", "ourense-provincia", "pais-vasco-frances", "palencia-provincia",
               "pontevedra-provincia", "salamanca-provincia", "santa-cruz-de-tenerife-provincia", "segovia-provincia",
               "sevilla-provincia", "soria-provincia", "tarragona-provincia", "teruel-provincia", "toledo-provincia",
               "valencia-provincia", "valladolid-provincia", "vizcaya", "zamora-provincia", "zaragoza-provincia"]

    for page in range(1,self.PAGES+1) :
      URL="https://www.idealista.com/venta-viviendas/madrid-madrid/pagina-%s.htm"
      print("\n","NEWPAGE: ", URL%str(page),"\n")
      yield scrapy.Request(url = URL % str(page), callback = self.parse_urls)

  def parse_urls(self, response):

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

    #DATE
    dateAndTime = datetime.now()
    item['dateAndTime'] = dateAndTime.strftime("%d/%m/%Y %H:%M:%S")

    #URL
    item['id'] = str(response.request.url).split("/")[-2] #to build up the url from the id, just do: https://www.idealista.com/inmueble/<idHere>/

    #TITLE
    title = response.xpath('//span[contains(@class,"main-info__title-main")]/text()').extract_first()
    item['title'] = title.strip()

    #PRICE
    price = response.xpath('//span[contains(@class,"info-data-price")]//text()').extract()
    item['price'] = price[0].strip().replace(".","")

    #NEIGHBORHOOD AND CITY
    #pillarlo de abajo, //div[contains(@id,"headerMap")]. Creo que guarda: Calle/Barrio/Distrito/CiudadPueblo/Region + provincia (del link)
    #tambien pillar las coordenadas del mapa
    allUbiInfoPre =  response.xpath('//div[contains(@id,"headerMap")]//ul//text()').extract()
    allUbiInfo = [i for i in allUbiInfoPre if i.strip()] #removes empty elements
    item['street'] = allUbiInfo[0]
    item['neighborhood'] = ""
    if (len(allUbiInfo)>3):
      item['neighborhood'] = allUbiInfo[1]
    item['district'] = ""
    if (len(allUbiInfo)>4):
      item['district'] = allUbiInfo[2]
    item['city'] = allUbiInfo[-2]
    item['region'] = allUbiInfo[-1].split(",")[0].strip()
    item['province'] = allUbiInfo[-1].split(",")[-1].strip()

    #OLDVERSION
    #neighborhoodAndCity = response.xpath('//span[contains(@class,"main-info__title-minor")]//text()').extract()
    #if "," in neighborhoodAndCity[0]:
    #  item['neighborhood'] = neighborhoodAndCity[0].split(",")[0].strip()
    #  item['city'] = neighborhoodAndCity[0].split(",")[1].strip()
    #else: #no neighborhood provided
    #  item['neighborhood'] = ""
    #  item['city'] = neighborhoodAndCity[0].strip()

    #WHOSELL
    whoSell = response.xpath('//div[contains(@class,"professional-name")]/div[contains(@class,"name")]//text()').extract()
    if (whoSell[0].strip()==""): #in case no profesional, this should be done to find the name of the particular
      whoSell = response.xpath('//div[contains(@class,"professional-name")]//text()').extract()
      item['whoSell'] = max(whoSell,key=len).strip()
    else:
      item['whoSell'] = whoSell[0].strip()

    #SURFACE
    surface = response.xpath('//div[contains(@class,"info-features")]/span[1]//text()').extract()
    item['surface'] = surface[1].strip(".").replace(".","")

    #NROOMS
    nRooms = response.xpath('//div[contains(@class,"info-features")]/span[2]//text()').extract()
    item['nRooms'] = nRooms[1].strip()

    #FEATURES
    features = response.xpath('//div[contains(@class,"details-property_features")]//li//text()').extract()
    item['features'] = features

    #DESCRIPTION
    #description = response.xpath('//div[contains(@id,"jobDescriptionText")]//text()').extract()
    #description = ' '.join(description)
    #item['description'] = description.replace("\n","").encode('utf-8')

    yield item

