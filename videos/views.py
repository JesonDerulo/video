from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import MemberRequiredMixin, StaffMemberRequiredMixin
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
class VideoCreateView(StaffMemberRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm



class VideoDetailView(MemberRequiredMixin, DetailView):
    queryset = Video.objects.all()






class VideoListView(ListView):
    def get_queryset(self):
        request = self.request
        qs = Video.objects.all()
        query = request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs





class VideoUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Video.objects.all()
    form_class = VideoForm

class VideoDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Video.objects.all()
    success_url = "/videos/"
