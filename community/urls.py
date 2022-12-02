from django.urls import path
from community import views

app_name = 'community'
urlpatterns = [
    path('column/', views.columns),
    path('column/new/', views.column_new),
    path('column/<int:pk>/', views.column_detail),
    path("column/<int:pk>/edit/", views.column_edit),
    path('event/', views.events),
    path('event/new/', views.event_new),
    path('event/<int:pk>/', views.event_detail),
    path("event/<int:pk>/edit/", views.event_edit),
    path('board/', views.board),
    path('board/new/', views.board_new),
    path('board/<int:pk>/', views.board_detail),
    path("board/<int:pk>/edit/", views.board_edit),
]

