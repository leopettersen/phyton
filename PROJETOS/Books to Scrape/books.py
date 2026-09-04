import scrapy
from scrapy.crawler import CrawlerProcess
import json

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    books_list = []
    cost_benefit_books_list = [] # Lista para livros que estão abaixo de 50 euros e tem entre 4 e 5 estrelas de avaliação

    def parse (self, response):
        for book in response.css('article.product_pod'):
            book_data = {
                'title': book.css('h3 a::attr(title)').get(),
                'price': float(book.css('p.price_color::text').get().replace('£', '')),
                'stars': book.css('p.star-rating::attr(class)').re_first('star-rating (\w+)'),
                'availability': book.css('p.instock.availability::text').re_first(r'(\S+\s\S+)'),
            }
            self.books_list.append(book_data)

            if book_data['price'] <= 50 and (book_data['stars'] in ['Four', 'Five']):
                self.cost_benefit_books_list.append(book_data)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            with open('books.json', 'w', encoding='utf-8') as file:
                json.dump(self.books_list, file, ensure_ascii=False, indent=4)

            with open('cost_benefits_books.json', 'w', encoding='utf-8') as file2:
                json.dump(self.cost_benefit_books_list, file2, ensure_ascii=False, indent=4)

process = CrawlerProcess()
process.crawl(BooksSpider)
process.start()