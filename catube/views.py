from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Video, Comment
from .forms import VideoForm, Commentform


class VideoListView(ListView):
    model = Video
    paginate_by = 4

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'form.html'

    def form_valid(self, form):
        video = form.save(commit=False)
        video.author = self.request.user
        return super().form_valid(form)

class VideoDetailView(DetailView):
    model = Video

class VideoUpdateView(UserPassesTestMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'form.html'

    def test_func(self):
        return self.request.user == self.get_object().author


class VideoDeleteView(UserPassesTestMixin, DeleteView):
    model = Video
    success_url = reverse_lazy('catube:video_list')

    def test_func(self):
        return self.request.user == self.get_object().author
