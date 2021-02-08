from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='/'), name='logout'),
]
