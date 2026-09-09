import scrapy
from scrapy.crawler import CrawlerProcess
import json

class CountriesSpider(scrapy.Spider):
    name = "countries"
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    countries_list = []
    big_countries_list = [] # Países com população acima de 50 milhões de habitantes e área acima de 500 mil km²

    def parse(self, response):
        for country in response.css('div.country'):
            country_data = {
                'name': ''.join(country.css('h3.country-name::text').getall()).strip(),
                'capital': country.css('span.country-capital::text').get().strip(),
                'population': int(country.css('span.country-population::text').get().replace(',', '')),
                'area_km2': float(country.css('span.country-area::text').get()),
            }
            self.countries_list.append(country_data)

            if country_data['population'] > 50000000 and country_data['area_km2'] > 500000:
                self.big_countries_list.append(country_data)

        with open('countries.json', 'w', encoding='utf-8') as file:
            json.dump(self.countries_list, file, ensure_ascii=False, indent=4)

        with open('big_countries.json', 'w', encoding='utf-8') as file2:
            json.dump(self.big_countries_list, file2, ensure_ascii=False, indent=4)

process = CrawlerProcess()
process.crawl(CountriesSpider)
process.start()