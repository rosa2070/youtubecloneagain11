from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, resolve_url
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Video, Comment
from .forms import VideoForm, CommentForm


class VideoListView(ListView):
    model = Video
    paginate_by = 4

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

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

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        from django.db.models import F
        Video.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['comment_form'] = CommentForm()
        return context_data


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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'form.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.video = get_object_or_404(Video, pk=self.kwargs['video_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('catube:video_detail', self.kwargs['video_pk'])

class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return resolve_url('catube:video_detail', self.kwargs['video_pk'])

