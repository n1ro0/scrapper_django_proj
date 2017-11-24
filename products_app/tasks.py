from __future__ import absolute_import, unicode_literals
from celery import shared_task
from products_app import models


@shared_task()
def save_pack(products, prices):
    save_products(products)
    save_prices(prices)


def save_products(products):
    for item in products:
        models.Product.objects.get_or_create(id=item['id'],
              site_product_id=item['site_product_id'],
              name=item['name'],
              brand=item['brand'],
              categories=' '.join(item['categories']),
              description=item['description'],
              url=item['url'],
              site=item['site']
              )


def save_prices(prices):
    for item in prices:
        models.Price.objects.get_or_create(id=item['id'],
             site_product_id=item['site_product_id'],
             product_id=item['product_id'],
             size=item['size'],
             color=item['color'],
             price=item['price'],
             stock_state=item['stock_state'],
             date=item['date']
             )