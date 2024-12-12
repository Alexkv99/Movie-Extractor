import scrapy
import re

class OscarSpider(scrapy.Spider):
    name = "oscar_spider"
    start_urls = [
        'file:///mnt/c/Users/alexa/Documents/Work/University/Dauphine/S1/Data Acquisition, Extraction and Storage/Projet/oscar_scraper/Search Results - Academy Awards Search _ Academy of Motion Picture Arts & Sciences.html'
    ]

    def parse(self, response):
        # Loop through each result group (by award year)
        for year_group in response.css('.result-group'):
            # Extract and clean the year (remove the "(xth)" part)
            year_text = year_group.css('.result-group-title a::text').get()
            year = re.sub(r'\s*\(\d+(st|nd|rd|th)\)', '', year_text)

            # Create a dictionary to store movies with their awards and nominees
            movies = {}

            # Loop through each award category
            for category_group in year_group.css('.result-subgroup'):
                category = category_group.css('.result-subgroup-title a::text').get()

                # Extract nominations
                for nomination in category_group.css('.result-details'):
                    movie = nomination.css('.awards-result-film-title a::text').get()
                    nominee = nomination.css('.awards-result-nominationstatement a::text').get()

                    if movie:
                        # Add the movie to the dictionary if not already there
                        if movie not in movies:
                            movies[movie] = []

                        # Append the award and nominee to the movie's list
                        movies[movie].append({
                            'Award': category,
                            'Nominee': nominee
                        })

            # Yield the final structure for the year
            for movie, details in movies.items():
                yield {
                    'Movie': movie,
                    'Year': year,
                    'Details': details
                }
