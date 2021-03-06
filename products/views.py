from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .filters import ProductFilter, CategoryFilter
from .form import ProductForm
from .models import Product, Category


def all_products(request):
    clicked = None

    products_list = Product.objects.all()
    categories_list = Category.objects.all()

    brands_column = products_list.values_list('brand_name', flat=True).distinct()

    products_filter = ProductFilter(request.GET, queryset=products_list).qs

    list_to_show = []
    list_popular_exclusive = []
    for product in products_list:
        if product.exclusive:
            list_popular_exclusive.append(product)

    list_to_show = list(filter(lambda product: product not in list_popular_exclusive, products_filter))
    if request.user.is_authenticated:
        list_to_show = products_filter  # ALL

    category_filter = CategoryFilter(request.GET, queryset=categories_list)

    overall_rating_selected = 0
    brand_selected = "All Brands"
    category_selected = "All Brands"
    lower_price = 0
    upper_price = 400
    current_sorting = None

    if request.GET:
        if 'overall_rating' in request.GET:
            overall_rating_selected = int(request.GET['overall_rating'])
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

        if 'ordering' in request.GET:
            clicked = 'filter'
            current_sorting = (request.GET['ordering'])

    context = {
        'products': list_to_show,

        'categories': category_filter,

        'brands': brands_column,

        'clicked': clicked,

        'overall_rating_selected': overall_rating_selected,

        'brand_selected': brand_selected,

        'category_selected': category_selected,

        'lower_price': lower_price,
        'upper_price': upper_price,

        'current_sorting': current_sorting,

    }
    return render(request, 'products/products.html', context)


def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    from_add_products = request.GET.get('from_add_products')
    context = {
        'product': product,
        'from_add_products': from_add_products
    }
    return render(request, 'products/product_details.html', context)


@login_required()
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you don't seem to have clearance to do that 🤭")
        return redirect(reverse('products'))

    products_list = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            the_product = form.save()
            messages.success(request, 'SUCCESS | Product added Successfully')
            return redirect(reverse('product_details', args=[the_product.id]))
        else:
            messages.success(request, 'ERROR | Sorry there is some error in your form')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'products': products_list,
        # 'from_add_products': request.GET.get('from_add_products')
        'from_add_products': True
    }
    return render(request, 'products/add_product.html', context)


@login_required()
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you don't seem to have clearance to do that 🤭")
        return redirect(reverse('products'))

    products_list = Product.objects.all()
    the_product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # form = ProductForm(request.POST, request.FILES, instance=the_product)
        form = ProductForm(request.POST, request.FILES, instance=the_product)
        if form.is_valid():
            form.save()
            messages.success(request, 'The product have been successfully updated')
            return redirect(reverse('product_details', args=[the_product.id]))
        else:
            messages.error(request, 'ERROR | Update failed. Please check the form')
    else:
        form = ProductForm(instance=the_product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'products': products_list,
        'product': the_product,
        'from_edit_products': True
    }
    return render(request, template, context)


@login_required()
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you don't seem to have clearance to do that 🤭")
        return redirect(reverse('products'))

    product = get_object_or_404(Product, pk=product_id)
    bag = request.session.get('bag', {})
    if str(product_id) in list(bag.keys()):
        messages.info(request, f'Please check your bag first and delete {product} from it')
        return redirect(reverse('shopping_bag'))
    else:
        messages.info(request, f'Product  {product} successfully deleted')
        product.delete()
    return redirect(reverse('products'))
