from django.shortcuts import render
from django.shortcuts import render

def product_list(request):
    items = [
        {"id": 1, "name": "Seramik Kupa", "price": "149₺"},
        {"id": 2, "name": "Poster", "price": "89₺"},
    ]
    return render(request, "products/list.html", {"items": items})


def product_detail(request, id):
    item = {"name": "Seramik Kupa", "price": "149₺", "desc": "El yapımı seramik kupa."}
    return render(request, "products/detail.html", {"item": item})

def product_list(request):
    return render(request, "products/list.html")
