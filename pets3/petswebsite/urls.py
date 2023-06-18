from django.contrib import admin
from django.urls import path, include
from petswebsite import views

urlpatterns = [
    path('', views.index, name='website'),
    path('lostandFound', views.lostandFound, name='lostandFound'),
    path('adoption', views.adoption, name='adoption'),
    path('profile/', views.profile, name='profile'),
    path('predict/', views.predict, name='predict'),
    path('predictimg/', views.predict_image, name='predictimg'),
    path('contact/', views.contact, name='contact'),
    path("login/", views.loginUser, name="loginUser"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logoutUser, name="logout"),
    path("loginSignUp/", views.LSpage, name="LSpage"),
    path("listadoption/", views.listadoption, name="listadoption"),
    path("listlaf/", views.listlaf, name="listlaf")
]