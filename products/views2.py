from decimal import Decimal
from django.shortcuts import render

from .filters import ProductFilter, CategoryFilter
from .models import Product, Category


def all_products(request):
    clicked = None

    products_list = Product.objects.all()
    categories_list = Category.objects.all()

    brands_column = products_list.values_list('brand_name', flat=True).distinct()

    products_filter = ProductFilter(request.GET, queryset=products_list)
    category_filter = CategoryFilter(request.GET, queryset=categories_list)

    overall_rating_selected = 0
    brand_selected = "All Brands"
    category_selected = "All Brands"
    lower_price = 0
    upper_price = 400

    if request.GET:
        if 'overall_rating' in request.GET:
            overall_rating_selected =int(request.GET['overall_rating'])
            clicked = 'rating'
        if 'brand_name' in request.GET:
            brand_selected = (request.GET['brand_name'])
            clicked = 'brand'
        if 'category' in request.GET:
            category_selected = int(request.GET['category'])
            clicked = 'category'
        if 'price__gt' in request.GET:
            clicked = 'price'
            lower_price = Decimal(request.GET['price__gt'])
        if 'price__lt' in request.GET:
            clicked = 'price'
            upper_price = Decimal(request.GET['price__lt'])

    context = {
        'products': products_filter,

        'categories': category_filter,

        'brands': brands_column,

        'clicked': clicked,

        'overall_rating_selected': overall_rating_selected,

        'brand_selected': brand_selected,

        'category_selected': category_selected,

        'lower_price': lower_price,
        'upper_price': upper_price,

    }
    return render(request, 'products/products.html', context)