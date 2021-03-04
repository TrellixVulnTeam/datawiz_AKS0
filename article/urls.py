from django.urls import path

from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
