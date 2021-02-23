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
    path('on_prepare/<int:pk>', views.on_prepare, name='on_prepare'),
    path('on_orders/', views.on_orders, name="on_orders"),
    path('on_order/<slug:user>/', views.on_order, name='on_order'),
    path('on_allorders/', views.onallorders, name='on_allorders'),

]
