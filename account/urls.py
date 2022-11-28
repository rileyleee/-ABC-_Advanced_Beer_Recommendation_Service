from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'account'
urlpatterns = [
    path("login/",  auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", views.signup, name='signup'),
    path("mypage/", views.mypage, name='mypage'),
    path("mypage_edit/", views.mypage_edit, name='mypage_edit'),
    path("mybeerlist/", views.mybeer, name='mybeerlist')
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
