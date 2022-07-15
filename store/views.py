from django.shortcuts import render

from django.views.generic import ListView, DetailView

# Product models
from store.models import Product, Category, ProductImages


class HomeListView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['product_gallery_images'] = ProductImages.objects.filter(product=self.object.id)

        return contex

# def product_details(request, pk):
#     item = Product.objects.get(id = pk)
#     gallery_photos = ProductImages.objects.filter(product=item).order_by('-created')
#     context ={
#         'item' : item
#          'gallery_photos' : gallery_photos
#     }
#     return render(request, 'store/product.html', context)
