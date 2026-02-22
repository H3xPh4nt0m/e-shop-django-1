from django.shortcuts import render, get_object_or_404
from apps.category.models import Category
from apps.store.models import Product

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
    
    return render(request, 'store/store.html', {'categories': categories, 'products': products})