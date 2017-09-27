from django.shortcuts import render
import random
from django.views.generic import (
        CreateView,
        DetailView,
        ListView,
        UpdateView,
        DeleteView,
)

from .models import Video
from .forms import VideoForm
# Create your views here.
class VideoCreateView(CreateView):
    model = Video
    form_class = VideoForm



class VideoDetailView(DetailView):
    queryset = Video.objects.all()

    def get_context_data(self, *args,**kwargs):
        context = super(VideoDetailView, self).get_context_data(*args,**kwargs)
        return context




class VideoListView(ListView):
    def get_queryset(self):
        request = self.request
        qs = Video.objects.all()
        query = request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs





class VideoUpdateView(UpdateView):
    queryset = Video.objects.all()
    form_class = VideoForm

class VideoDeleteView(DeleteView):
    queryset = Video.objects.all()
    success_url = "/videos/"
