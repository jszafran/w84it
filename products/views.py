from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import ProductForm
from .models import Product


class Product(TemplateView):
    @login_required
    def add_product(request):
        if request.method == 'POST':
            form = ProductForm(request.POST, request=request, action_type='ADD')
            if form.is_valid():
                product = form.save(commit=False)
                product.owner = request.user
                product.save()
                return HttpResponse('Product created!')
            else:
                return render(request, 'add_product.html', {'form': form})

        return render(request, 'add_product.html', {'form': ProductForm()})

    @login_required
    def edit_product(request, pk=None):
        orig_name = None
        if pk:
            product = get_object_or_404(Product, pk=pk)
            orig_name = product.name
            if product.owner != request.user:
                raise Http404()

        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product, request=request, orig_name=orig_name, action_type='EDIT')
            if form.is_valid():
                form.save()
                return HttpResponse('Article successfully edited!')
            else:
                return render(request, 'add_product.html', {'form': form})
        else:
            form = ProductForm(instance=product)
            return render(request, 'add_product.html', {'form': form})
