from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/new/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_update, name='property_update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('register/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),
] 