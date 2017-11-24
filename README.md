# scrapper_django_proj
-From default category url It scrapped to my database 55138 products and 303255 product prices.

-To make this project work you have to install requirements, start django proj,
 celery worker and lordandtaylor spider.
 Django app starts Spider with entered url of category to parse and
 shows all products with its prices from database.
 Spider crawls products and all possible product prices from chosen category
 and sends tasks to celery to save packs of it.
 Celery saves it to postgres database. You have to run servers: 
 Redis, Postgres and create user and database in postgresql.

    1. When you install redis server it automatically starts:
        sudo apt-get install redis-server

    2. When you install postgresql its server automatically starts:
        sudo apt-get install postgresql

    3. to install requirements use commands:
        enter folder: scrapper_django_proj
        run command: pip install -r requirements.txt

    4. to create user and database use commands bellow:
        sudo su postgres psql
        CREATE USER scrapy_user with password 'qwerty12';
        CREATE DATABASE scrapy_db2 owner scrapy_user;

    5. to run celery worker:
        enter folder: scrapper_django_proj
        run command: celery -A scrapper_django_proj worker --loglevel=info

    6. to run spider:
        enter folder: scrapper_django_proj/products_scraper
        run command: scrapy crawl lordandtaylor

    7. to run django proj:
        enter folder: scrapper_django_proj
        run command: python manage.py runserver [port]


