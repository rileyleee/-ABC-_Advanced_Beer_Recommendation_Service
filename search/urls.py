from django.urls import path
from search import views, ml

urlpatterns = [
     path('', views.keyword),
     path('recommend/', views.predict),
     path('beerprofile/<int:pk>/', views.search_detail),
     path('search/', views.search)
]


    