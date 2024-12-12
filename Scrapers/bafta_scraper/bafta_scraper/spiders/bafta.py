import scrapy
import json


class BaftaSpider(scrapy.Spider):
    name = "bafta"
    start_urls = ["https://www.bafta.org/awards/film"]

    # Initialize a dictionary to store all years' data
    bafta_data = {}

    def parse(self, response):
        # Extract the year links from the dropdown menu
        year_links = response.xpath("//ul[@class='dropdown__optionlist']//a")

        # Loop through each year link and extract the year and URL
        for year_link in year_links:
            year = year_link.xpath("./@data-option").get()  # Get the year
            href = year_link.xpath("./@href").get()  # Get the URL

            if year and href:
                full_url = response.urljoin(href)  # Convert to absolute URL
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_year,
                    meta={"year": year},  # Pass the year to the next parse method
                )

    def parse_year(self, response):
        year = response.meta["year"]
        year_data = {}

        # Select all category blocks (accordion items)
        category_blocks = response.xpath(
            './/li[starts-with(@class, "accordion__item")]'
        )

        for block in category_blocks:
            # Extract the category name
            category_name = block.xpath(".//button/text()").get()
            category_name = (
                category_name.strip() if category_name else "Unknown Category"
            )

            # Extract winner information
            winner_block = block.xpath(
                "(.//div[contains(@class, 'nomination__body__top')])[1]"
            )
            winner_title = winner_block.xpath(
                ".//h3[@class='tile__heading nomination__heading text-reg font-bold']/text()"
            ).get()  # Extract the winner title from the h3 element

            winner_persons = winner_block.xpath(
                ".//div[@class='nomination__nominees text-sm o-50']//text()"
            ).getall()  # Extract the associated names (if available)

            # Clean the extracted data
            winner_title = winner_title.strip() if winner_title else None
            winner_persons = [
                name.strip() for name in winner_persons if name.strip()
            ]  # Clean up whitespace

            winner = {
                "title": winner_title,
                "persons_invested": winner_persons,
            }

            # Extract nominees (if available)
            nominees = []
            nominee_items = block.xpath(".//div[@class='nomination__body__top']")
            for nominee in nominee_items:
                nominee_title = nominee.xpath(".//h3/text()").get()
                nominee_persons = nominee.xpath(
                    ".//div[@class='nomination__nominees text-sm o-50']//text()"
                ).getall()

                nominee_persons = [
                    name.strip() for name in nominee_persons if name.strip()
                ]  # Clean up whitespace
                nominees.append(
                    {
                        "title": nominee_title.strip() if nominee_title else None,
                        "persons_invested": nominee_persons,
                    }
                )

            # Add category data to the year's data
            year_data[category_name] = {
                "winner": winner,
                "nominees": nominees,
            }

        # Add this year's data to the main BAFTA dictionary
        self.bafta_data[year] = year_data

    def closed(self, reason):
        # Save the entire BAFTA dictionary as a single JSON file
        with open("bafta_data.json", "w") as f:
            json.dump({"BAFTA": self.bafta_data}, f, indent=4)

        self.log("Saved all BAFTA data to bafta_data.json")
