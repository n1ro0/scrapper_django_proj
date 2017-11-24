from django.contrib import admin
from . import models


admin.site.register((models.Product, models.Price))

# Register your models here.
