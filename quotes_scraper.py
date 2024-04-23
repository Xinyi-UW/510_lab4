import requests
from bs4 import BeautifulSoup
from db import Database  # Make sure this matches your actual import path

# Database URL from your environment or securely configured
DATABASE_URL = 'postgres://postgres.bfalsaypqidxjbgpdeuc:P2IdU9d7zG3mAjpI@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

# Initialize database and create table
db = Database(DATABASE_URL)
db.create_table()

# Initial URL
BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'

books = []
page = 1
while True:
    url = BASE_URL.format(page)
    print(f"Scraping {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print("No more pages to scrape.")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    book_items = soup.select('article.product_pod')

    if not book_items:
        print("No more books to scrape.")
        break

    for book in book_items:
        book_data = {
            'title': book.select_one('h3 a')['title'],
            'price': book.select_one('.price_color').text,
            'rating': book.select_one('p.star-rating')['class'][1]
        }
        books.append(book_data)
        db.insert_book(book_data)

    page += 1

print(f"Total books scraped: {len(books)}")
