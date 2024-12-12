import scrapy


class SpiderPalmeSpider(scrapy.Spider):
    name = "spiderPalme"
    allowed_domains = ["https://fr.wikipedia.org/wiki/Palme_d%27or"]
    start_urls = ["https://fr.wikipedia.org/wiki/Palme_d%27or"]

    DOWNLOAD_DELAY = 1

    def parse(self, response):
        table = response.css("table.wikitable[style='text-align:center'][width='98%']").css("tr")
        rowspan = [0]*5
        memory = ['']*5
        for tr in table:
            tds = tr.css("td")
            if tds == [] or tds[1].css(".table-na").get() is not None:
                continue
            offset = 0
            line = ['']*5
            for i in range(5):
                if rowspan[i] < 1:
                    td = tds[i-offset]
                    line[i] = td.css("i::text, a[title]::text").get()

                    rwsp = td.css("::attr(rowspan)").get()
                    if rwsp is not None:
                        rowspan[i] = int(rwsp) -1
                        memory[i] = line[i]
                else:
                    rowspan[i] -= 1
                    line[i] = memory[i]
                    offset += 1
                    print(line[i])
                    print("- :", rowspan)
                
            yield {
                "prix": "Palme d'or",
                "année": line[0],
                "film": (line[2] if line[2] is not None else line[1]),
                "récipiendaire": line[3],
                "pays": line[4]
            }

