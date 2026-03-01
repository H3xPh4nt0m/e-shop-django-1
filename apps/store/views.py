from urllib import request

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from apps.carts.models import CartItem
from apps.carts.views import _cart_id
from apps.category.models import Category
from .models import Product

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        # 'categories': categories,
        'products': paged_products,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    return render(request, 'store/product-detail.html', {'single_product': single_product, 'in_cart': in_cart})

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = Product.objects.order_by('-created_at').filter(description__icontains=keyword) | Product.objects.order_by('-created_at').filter(name__icontains=keyword)
        # or we can use Q objects to search in multiple fields
        # from django.db.models import Q
        # products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products': paged_products,
            'product_count': products.count(),
        }
    return render(request, 'store/store.html', context)