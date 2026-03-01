from django.shortcuts import render
from .models import Good


def product_list(request):
    products = Good.objects.all()
    return render(request, "shop/product_list.html", {"products": products})
