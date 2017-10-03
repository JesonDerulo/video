from django.conf.urls import url

from .views import (
    CategoryListView,
    CategotyDetailView,
)

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', CategotyDetailView.as_view(), name='detail'),

]