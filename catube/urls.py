from django.urls import path

from . import views

app_name = 'catube'

urlpatterns = [
    path('', views.VideoListView.as_view(), name='video_list'),
    path('new/', views.VideoCreateView.as_view(), name='video_new'),
    path('<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('<int:pk>/edit/', views.VideoUpdateView.as_view(), name='video_edit'),
    path('<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video_delete'),
]