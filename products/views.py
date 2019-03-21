from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import AddProductForm

class AddProduct(TemplateView):
    @login_required
    def add_product(request):
        if request.method == 'POST':
            form = AddProductForm(request.POST, request=request)
            if form.is_valid():
                product = form.save(commit=False)
                product.owner = request.user
                product.save()
                return HttpResponse('Product created!')
            else:
                return render(request, 'add_product.html', {'form': form, 'test': 'just_a_test'})

        return render(request, 'add_product.html', {'form': AddProductForm()})
