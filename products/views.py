from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import ProductForm
from .models import Product


class ProductView(TemplateView):
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
            if product.owner != request.user or not product:
                raise Http404()

        if request.method == 'POST':
            if 'save_product' in request.POST:
                form = ProductForm(request.POST, instance=product, request=request, orig_name=orig_name, action_type='EDIT')
                if form.is_valid():
                    form.save()
                    return HttpResponse('Article successfully edited!')
                else:
                    return render(request, 'edit_product.html', {'form': form})
            elif 'delete_product' in request.POST:
                return redirect('delete_product', pk=pk)
        else:
            form = ProductForm(instance=product)
            return render(request, 'edit_product.html', {'form': form})

    @login_required
    def delete_product(request, pk=None):
        product = None
        if pk:
            product = get_object_or_404(Product, pk=pk)
            if product.owner != request.user or not product:
                raise Http404()

        if request.method == 'POST':
            product.delete()
            return HttpResponse('Product deleted from database!')
        else:
            return render(request, 'confirm_product_deletion.html')
