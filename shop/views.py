from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Good, Category, Supplier


def product_list(request):
    products = Good.objects.all()

    # Поиск по названию и артикулу
    search_query = request.GET.get("search", "")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(product_code__icontains=search_query)
        )

    # Фильтр по категории
    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category_id=category_id)

    # Фильтр по поставщику
    supplier_id = request.GET.get("supplier")
    if supplier_id:
        products = products.filter(supplier_id=supplier_id)

    # Сортировка
    sort_by = request.GET.get("sort", "name")
    if sort_by == "name":
        products = products.order_by("name")
    elif sort_by == "name_desc":
        products = products.order_by("-name")
    elif sort_by == "price_asc":
        products = products.order_by("price")
    elif sort_by == "price_desc":
        products = products.order_by("-price")

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "suppliers": suppliers,
        "search_query": search_query,
        "current_category": category_id,
        "current_supplier": supplier_id,
        "current_sort": sort_by,
    }
    return render(request, "shop/product_list.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Good, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})