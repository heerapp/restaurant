from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.item),
    path('order/', views.order),
    path('table/<int:pk>/order/', views.orders, name='orders'),
    path('allorders/', views.allorders, name='allorders'),
    path('tables/', views.tables, name='tables'),
    path('prepare/<int:pk>', views.prepare, name='prepare'),
]
