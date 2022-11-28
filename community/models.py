from django.db import models
from beer_recommend_prj import settings
from beer_recommend_prj.settings import MEDIA_ROOT


class Column(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # TODO : 장고의 URL Reverse 기능을 사용하기
        return f"/column/{self.pk}/"

    def __str__(self):
        return f"[{self.pk}] {self.title}"


class Event(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # TODO : 장고의 URL Reverse 기능을 사용하기
        return f"/event/{self.pk}/"

    def __str__(self):
        return f"[{self.pk}] {self.title}"