from django.db import models


class Product(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    site_product_id = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    categories = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    url = models.CharField(max_length=300)
    site = models.CharField(max_length=50)


class Price(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    site_product_id = models.CharField(max_length=30)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=70)
    price = models.FloatField()
    stock_state = models.CharField(max_length=30)
    date = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



