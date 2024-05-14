from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .forms import CartAddProductForm


@method_decorator(csrf_exempt, name='dispatch')
class CartAddView(View):
    def post(self, request):
        field_mapping = {
            'product-id': 'product_id',
            'num-product': 'quantity',
            'size': 'size_id',
            'color': 'color_id',
        }

        # Create a dictionary containing data with form field names
        form_data = {field_mapping[key]: value for key, value in request.POST.items()}
        form = CartAddProductForm(data=form_data, product_id=request.POST.get('product-id'))

        if form.is_valid():
            print()
        return HttpResponse("good")

    def get(self, request):
        form = CartAddProductForm()
        return render(request, "list.html", {'form': form})
