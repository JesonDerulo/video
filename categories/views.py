from django.shortcuts import render
from django.views.generic import (
        CreateView,
        DetailView,
        UpdateView,
        ListView,
        DeleteView,
        RedirectView,
)

# Create your views here.
from .models import Category

class CategoryListView(ListView):
    queryset = Category.objects.all()

class CategotyDetailView(DetailView):
    queryset = Category.objects.all()