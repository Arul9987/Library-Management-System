from django.urls import path
from .views import *
from . import views
#from django.contrib.auth import views


urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    #Registrations
    path('register/',views.register_view, name='register'),
    path('logout/', custom_logout, name='custom_logout'),
    path('login/',login_view,name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    #dashboard
    path('board/', dashboard, name='dashboard'),
]