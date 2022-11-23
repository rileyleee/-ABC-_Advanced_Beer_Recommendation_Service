"""do_it_django_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from beer_recommend_prj import settings


def root(request):
    return redirect("/search/")
    # HttpResponse("/search를 추가해 '오늘 시간 비어: 맥주 추천 페이지'로 이동해주세요")


urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('search/', include('search.urls')),
    path('community/', include('community.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
