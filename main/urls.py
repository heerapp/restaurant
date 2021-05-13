from django.urls import path
from . import views
from .views import CartDeleteView

urlpatterns = [
    path('', views.index, name="home"),
    path('<int:pk>/', views.item),
    path('order/', views.order, name='order'),
    path('table/<int:pk>/order/', views.orders, name='orders'),
    # path('allorders/', views.allorders, name='allorders'),
    path('tables/', views.tables, name='tables'),
    path('prepare/<int:pk>', views.prepare, name='prepare'),
    path('on_prepare/<int:pk>', views.on_prepare, name='on_prepare'),
    path('on_orders/', views.on_orders, name="on_orders"),
    path('on_order/<slug:user>/', views.on_order, name='on_order'),
    path('on_allorders/', views.onallorders, name='on_allorders'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/', CartDeleteView.as_view(), name='remove-from-cart'),
    path('ordered/', views.order_item, name='ordered'),
    path('order_details/', views.order_details, name='order_details'),
    path('result-page/', views.schedule_queue, name="result-page"),

]
