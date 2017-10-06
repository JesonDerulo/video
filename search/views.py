from django.shortcuts import render
from courses.models import Course, Lecture
from categories.models import Category
from django.views.generic import View
# Create your views here.

class SearchView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET.get('q'))
        return render(request, "search/default.html", {})
