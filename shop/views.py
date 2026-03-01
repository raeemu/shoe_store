from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Good, Category, Supplier, OrderItem, Order
from .forms import GoodForm
from django.db import connection

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

def product_create(request):
    if request.method == "POST":
        form = GoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = GoodForm()
    return render(request, "shop/product_form.html", {"form": form, "mode": "create"})

def product_update(request, pk):
    product = get_object_or_404(Good, pk=pk)
    if request.method == "POST":
        form = GoodForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = GoodForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "mode": "update"})

def product_delete(request, pk):
    product = get_object_or_404(Good, pk=pk)

    # 1. Проверяем, есть ли позиции заказа с этим товаром
    in_orders = OrderItem.objects.filter(product_id=product.id).exists()

    if request.method == "POST":
        if in_orders:
            # Товар есть в заказах — НЕ удаляем
            return render(
                request, "shop/product_cannot_delete.html", {"product": product}
            )
        else:
            # 2. Товара нет в заказах — удаляем напрямую из таблицы goods
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM goods WHERE id = %s",
                    [product.id],
                )
            return redirect("product_list")

    # GET-запрос — просто страница подтверждения
    return render(
        request,
        "shop/product_confirm_delete.html",
        {
            "product": product,
            "in_orders": in_orders,
        },
    )
def order_list(request):
    orders = Order.objects.select_related("user", "pickup_point", "status")
    return render(request, "shop/order_list.html", {"orders": orders})


def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("user", "pickup_point", "status"),
        pk=pk,
    )
    items = OrderItem.objects.select_related("product").filter(order=order)

    # считаем итоговую сумму с учётом скидки
    total = 0
    for item in items:
        price = item.product.price
        discount = item.product.discount or 0
        price_with_discount = price * (100 - discount) // 100
        total += price_with_discount * item.amount

    context = {
        "order": order,
        "items": items,
        "total": total,
    }
    return render(request, "shop/order_detail.html", context)