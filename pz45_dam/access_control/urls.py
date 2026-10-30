from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='access_index'),
    path('requests/', views.requests_list, name='access_requests'),
]
