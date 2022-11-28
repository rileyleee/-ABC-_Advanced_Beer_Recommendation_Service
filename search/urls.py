from django.urls import path
from search import views


app_name = 'search'
urlpatterns = [
     path('', views.keyword),
     path('recommend/', views.predict),
     path('beerprofile/<int:pk>/', views.search_detail, name="beerprofile"),
     path('search/', views.search),
     path('like/<int:pk>/', views.like, name="like"),
]


    