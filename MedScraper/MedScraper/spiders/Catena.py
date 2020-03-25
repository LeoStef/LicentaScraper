import scrapy
import json
class med(scrapy.Item):
    name = scrapy.Field()
    atc = scrapy.Field()




class CatenaSpider(scrapy.Spider):
    name = "catena"


    def start_requests(self):
        domain = "https://www.catena.ro/medicamente/"
        categorii = ["raceala-si-gripa", "durere", "oftalmologie-si-orl", "cardiovascular", "dermatologie",
                     "afectiuni-gastrointestinale", "afectiuni-hepatobiliare",
                     "afectiuni-genito-urinare", "tulburari-tranzit-intestinal", "stres-si-tulburari-de-somn",
                     "vitamine-si-minerale", "diabet", "diverse-otc", "tractul-digestiv-si-metabolism",
                     "sange-si-organe-hematopoietice", "sistem-cardiovascular", "preparate-dermatologice",
                     "aparatul-genito-urinar-si-hormonii-sexuali", "preparate-hormonale",
                     "antiinfectioase", "antineoplazice-si-imunomodulatoare", "sistemul-muscular-scheletic",
                     "sistemul-nervos", "produse-antiparazitare", "aparatul-respirator",
                     "organe-senzitive-orl", "varia-rx"]
        for cat in categorii:
            yield scrapy.Request(url=domain + str(cat)+"/page/1",callback=self.parse)

    def parse(self, response):
        #names
        names = response.css(".product-categories-title a::text").getall()
        pagination = response.css('.pagination a::text').getall()
        URL = response.request.url;
        rawURL = URL[:-1]
        pageNumberNext = int(URL[-1]) + 1

        #prices
        prices = []
        for i in range(int(len(names)/3)):
            for j in range(2):
                prices.append(response.xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div["+ str(i + 3) +"]/ul/li["+str(j + 1)+"]/script[2]/text()").get())
        formattedPrices = []

        for price in prices:
            start = price.index("'price': ") +10
            end = price.index("'price': ") +15
            formattedPrices.append(price[start:end])

        #pictures
        pictures = response.css(".content-box img").xpath('@src').getall()
        picturesFull = []
        for pic in pictures:
            fullPic = "https://www.catena.ro" + pic
            picturesFull.append(fullPic)

        #categorie
        categorie = response.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/ul/li[5]/a/span/text()').getall()


        #array of objects
        objectArray = []
        while len(formattedPrices)<len(names):
            formattedPrices.append("1.000")


        for i in range(len(names)):
            objectArray.append([names[i],formattedPrices[i],picturesFull[i],categorie])




        #conditional scraping
        if str(pageNumberNext) in pagination:
            yield scrapy.Request(url=rawURL + str(pageNumberNext))


        print(len(names))
        print(len(formattedPrices))
        print(len(picturesFull))
        print(len(categorie))


        # #default yield
        # yield {"name": names,
        #         "pret": formattedPrices,
        #        "pic": picturesFull,
        #        "categorie" : categorie
        #    }
        #iterated yield

        for item in objectArray:
            yield {
                "name":item[0],
                "pret":item[1],
                "pic":item[2],
                "categorie":item[3][0]
            }
