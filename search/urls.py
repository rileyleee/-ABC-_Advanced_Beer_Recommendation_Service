from django.urls import path
from search import views, ml

urlpatterns = [
     path('', views.search),
     path('recommend/', views.recommend),
     path('beerprofile/<int:pk>/', views.search_detail),

]

    