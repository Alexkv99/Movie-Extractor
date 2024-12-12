import scrapy


class GoldenGlobeSpider(scrapy.Spider):
    name = "golden_globe_spider"
    start_urls = [
        # Add URLs here as you iterate with each new category.
        "https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Motion_Picture_%E2%80%93_Drama",
        "https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Motion_Picture_%E2%80%93_Musical_or_Comedy",
        "https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Foreign_Language_Film",
        "https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Animated_Feature_Film",
        "https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Cinematic_and_Box_Office_Achievement",
        'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Actor_in_a_Motion_Picture_–_Drama',
        'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Actor_in_a_Motion_Picture_–_Musical_or_Comedy',
        'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Actress_in_a_Motion_Picture_–_Drama',
        'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Actress_in_a_Motion_Picture_–_Musical_or_Comedy',
        'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Director',
    ]

    def parse(self, response):
        category = response.css('title::text').get().split(" - ")[0].strip()
        awards_data = []

        if "Drama" in category or "Musical or Comedy" in category:
            rows = response.css("table.wikitable tbody tr")
            for row in rows:
                year = row.css("th a::text").get()
                movie = row.css("td b a::text").get()
                nominees = row.css("td:nth-child(3) a::text, td:nth-child(3)::text").getall()

                if movie and year:
                    awards_data.append({
                        "Movie": movie.strip(),
                        "Year": year.strip(),
                        "Details": {
                            "Award": category,
                            "Nominee(s)": [n.strip() for n in nominees if n.strip()],
                        },
                    })

        elif "Foreign Language Film" in category:
            rows = response.css("table.wikitable tbody tr")
            for row in rows:
                year = row.css("th::text").get()
                english_title = row.css("td i b a::text").get()
                nominees = row.css("td:nth-child(3) a::text, td:nth-child(3)::text").getall()

                if english_title and year:
                    awards_data.append({
                        "Movie": english_title.strip(),
                        "Year": year.strip(),
                        "Details": {
                            "Award": category,
                            "Nominee(s)": [n.strip() for n in nominees if n.strip()],
                        },
                    })

        elif "Animated Feature Film" in category or "Cinematic and Box Office Achievement" in category:
            rows = response.css("table.wikitable tbody tr")
            for row in rows:
                year = row.css("th a::text").get()
                movie = row.css("td i b a::text").get()
                nominees = row.css("td:nth-child(4) a::text, td:nth-child(4)::text").getall()

                if movie and year:
                    awards_data.append({
                        "Movie": movie.strip(),
                        "Year": year.strip(),
                        "Details": {
                            "Award": category,
                            "Nominee(s)": [n.strip() for n in nominees if n.strip()],
                        },
                    })
        elif "Director" in category:
            rows = response.css('table.wikitable tbody tr')
            for row in rows:
                cells = row.css('td')
                if len(cells) >= 2:
                    # Extract movie and year
                    year = cells[0].css('::text').get().strip()
                    title_and_nominees = cells[1].css('::text').getall()
                    movie = title_and_nominees[0].strip() if title_and_nominees else None
                    nominees = [nom.strip() for nom in title_and_nominees[1:] if nom.strip()]

                    if movie and year:
                        awards_data.append({
                            "Movie": movie.strip(),
                            "Year": year.strip(),
                            "Details": {
                                "Award": category,
                                "Nominee(s)": nominees,
                            },
                        })
        elif "Actor in a Motion Picture – Drama'" in category:
            rows = response.css('table.wikitable tbody tr')
            for row in rows[1:]:  # Skip the header row
                cells = row.css('td')
                if len(cells) >= 4:  # Ensure sufficient columns
                    # Extract year, actor, role, and film
                    year = row.css('th::text').get().strip()  # Year is in a header cell
                    nominees = cells[0].css('::text').get().strip()
                    # role = cells[1].css('::text').get().strip()
                    movie = cells[2].css('::text').get().strip()

                    if year and movie:
                        awards_data.append({
                            "Movie": movie.strip(),
                            "Year": year.strip(),
                            "Details": {
                                "Award": category,
                                "Nominee(s)": nominees,
                            },
                        })


        for award in awards_data:
            yield award


# class GoldenGlobeSpider(scrapy.Spider):
#     name = "golden_globe_spider"

#     # Initial list of URLs
#     start_urls = [

#     ]

#     output_file = Path("golden_globe_data.json")

#     def start_requests(self):
#         # Load existing data if it exists
#         if self.output_file.exists():
#             with open(self.output_file, 'r', encoding='utf-8') as f:
#                 self.data = json.load(f)
#         else:
#             self.data = {}

#         for url in self.start_urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         category = response.css('title::text').get().split(" - ")[0].strip()

#         rows = response.css('table.wikitable tbody tr')
#         for row in rows:
#             cells = row.css('td')
#             if len(cells) >= 2:
#                 # Extract movie and year
#                 year = cells[0].css('::text').get().strip()
#                 title_and_nominees = cells[1].css('::text').getall()
#                 movie = title_and_nominees[0].strip() if title_and_nominees else None
#                 nominees = [nom.strip() for nom in title_and_nominees[1:] if nom.strip()]

#                 if movie and year:
#                     # If movie and year exist, append or create
#                     if movie not in self.data:
#                         self.data[movie] = {'Year': year, 'Details': []}
#                     elif self.data[movie]['Year'] != year:
#                         self.data[f"{movie} ({year})"] = {'Year': year, 'Details': []}

#                     # Append details
#                     self.data[movie]['Details'].append({
#                         'Award': category,
#                         'Nominee(s)': nominees,
#                     })

#         # Write the updated data
#         with open(self.output_file, 'w', encoding='utf-8') as f:
#             json.dump(self.data, f, indent=4, ensure_ascii=False)