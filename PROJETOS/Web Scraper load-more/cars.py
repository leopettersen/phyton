import scrapy
from scrapy.crawler import CrawlerProcess
import json

class CarsSpider(scrapy.Spider):
    name = 'cars'
    start_urls = ['https://webscraper.io/test-sites/load-more']

    page = 2
    cars_list = []
    old_rare_cars_list = [] # Carros que tenham sido fabricados antes de 1985

    def parse(self, response):
        cars = response.css('div.card.sitemap-card.test-sites-card')

        if cars:
            for car in cars:
                car_data = {
                    'name': car.css('div.card-body h3.card-title::attr(title)').get(),
                    'description': car.css('div.card-body p.description::text').get().strip(),
                    'year': int(car.css('div.card-body p.card-text:nth-of-type(2)::text').re_first(r'(\s\S+)').strip()),
                    'country': car.css('div.card-body p.card-text:nth-of-type(3)::text').getall()[1].strip(),
                    'mileage': car.css('div.card-body p.card-text:nth-of-type(4)::text').getall()[1].strip(),
                    'rarity_rating': int(car.css('div.card-footer div.rarity-rating::attr(data-rating)').get()),
                    'price': car.css('div.card-footer p.price span::text').get().replace('USD ', '$').strip().replace(' ', '.'),
                    'availability': car.css('div.card-head div.badge::text').get().strip()
                }
                self.cars_list.append(car_data)
            
                if car_data['year'] <= 1985 and car_data['rarity_rating'] >= 4:
                    self.old_rare_cars_list.append(car_data)

            next_url = f'https://webscraper.io/test-sites-ajax?page={self.page}'
            self.page += 1
            yield response.follow(next_url, callback=self.parse)

        else:
            with open('cars.json', 'w', encoding='utf-8') as file:
                json.dump(self.cars_list, file, ensure_ascii=False, indent=4)

            with open('old_rare_cars.json', 'w', encoding='utf-8') as file2:
                json.dump(self.old_rare_cars_list, file2, ensure_ascii=False, indent=4)

process = CrawlerProcess()
process.crawl(CarsSpider)
process.start()