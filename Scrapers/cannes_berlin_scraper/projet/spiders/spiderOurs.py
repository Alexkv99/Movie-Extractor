import scrapy


class SpiderOursSpider(scrapy.Spider):
    name = "spiderOurs"
    allowed_domains = ["www.berlinale.de"]
    start_urls = ["https://www.berlinale.de/en/archive/awards-juries/awards.html/y=1951,2024/o=desc/p=1/rp=40"]

    root = "https://www.berlinale.de/en/archive/awards-juries/awards.html/y=1951,2024/o=desc/p="
    end = "/rp=40"
    DOWNLOAD_DELAY = 1

    def parse(self, response):
        for i in range(1,39):
            link = self.root + str(i) + self.end
            yield from response.follow_all(link, lambda x :self.parse_page(x,i))


    def parse_page(self, response, page):
        for div in response.css("div.award-list__item"):
            award = div.css("strong.award-list__type::text").get()
            film = div.css("div.award-list__details > p > a::text").get()
            opt_receiver = div.css("div.award-list__details").css(" b::text").get()
            if opt_receiver == "produced by:":
                opt_receiver = None
            yield {
                "film" : film,
                "prix" : award,
                "récipiendaire" : opt_receiver,
                "année" : str(2024-page+1)
            }
