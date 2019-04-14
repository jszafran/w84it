from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import ProductForm
from .models import Product


def user_owns_product(user, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    return product.owner == user


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
                print(request.LANGUAGE_CODE)
                return render(request, 'add_product.html', {'form': form})

        return render(request, 'add_product.html', {'form': ProductForm()})

    @login_required
    def edit_product(request, pk=None):
        if not user_owns_product(request.user, pk):
            raise Http404()
        else:
            product = Product.objects.get(pk=pk)
            orig_name = product.name

        if request.method == 'POST':
            if 'save_product' in request.POST:
                form = ProductForm(request.POST, instance=product, request=request, orig_name=orig_name, action_type='EDIT')
                if form.is_valid():
                    form.save()
                    return HttpResponse('Product successfully edited!')
                else:
                    return render(request, 'edit_product.html', {'form': form})
            elif 'delete_product' in request.POST:
                return redirect('delete_product', pk=pk)
        else:
            form = ProductForm(instance=product)
            return render(request, 'edit_product.html', {'form': form})

    @login_required
    def delete_product(request, pk):
        if not user_owns_product(request.user, pk):
            raise Http404()
        else:
            product = Product.objects.get(pk=pk)

        if request.method == 'POST':
            product.delete()
            return HttpResponse('Product deleted from database!')
        else:
            return render(request, 'confirm_product_deletion.html', {'product': product})
