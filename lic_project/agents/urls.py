from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.add_agent),
    path('update/<int:id>/', views.update_agent),
    path('delete/<int:id>/', views.delete_agent),
    path('dashboard/', views.dashboard, name='dashboard'),
]
