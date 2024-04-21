from django.shortcuts import render

from catalog.models import Product


def home(request):
    products_list = Product.objects.all()
    context = {
        'title': 'Каталог продуктов',
        'object_list': products_list
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html')


def product_info(request, pk):
    product_info_list = Product.objects.get(pk=pk)
    context = {
        'title': 'Описание продуктов',
        'object': product_info_list
    }
    return render(request, 'catalog/product_info.html', context)
