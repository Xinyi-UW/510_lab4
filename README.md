# 510_lab4

# this is a web scraping lab

# this App can search and filter by factors like book title, price, and start rating

Getting Started

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Some debug experiences - 1.gitclone process

Connecting local git and remote githut repository everytime encounter some similar problem.
Then, trying to polish the process:
1.Create a new repository on your github with README.md
2.Git clone
3.Create app.py, new stuff on vs code, then push them to repository to check how does it wrok

Some debug experiences - 2.scraper - supabase connection
problem: 1k data successfully scraped online and it shows on ternimal as well, but nothing inside supabase.
Solution: I forgot to initialize supabase at the beginning of 'scraper.py' file
