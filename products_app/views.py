from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from redis.client import Redis
from . import models
client = Redis()

class ProductListView(generic.ListView):
    template_name = 'products.html'
    model = models.Product
    context_object_name = 'products'


class IndexView(generic.TemplateView):
    template_name = 'index.html'
    def post(self, request, *args, **kwargs):
        url = request.POST['url']
        client.lpush('lordandtaylor:start_urls', url)
        return render(request, template_name="success_start.html")
