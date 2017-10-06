
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin



from .views import home, HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^videos/', include('videos.urls', namespace='videos')),
    url(r'^search/', include('search.urls', namespace='search')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
