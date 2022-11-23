from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings


def user_path(instance, filename):  # 파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string  # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)  # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1]  # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.user.username, pid, extension)  # 예 : wayhome/abcdefgs.png


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # User모델과 Profile을 1:1로 연결



class User(AbstractUser):
    class GenderChoices(models.IntegerChoices):
        MALE = 0, "남성"
        FEMALE = 1, "여성"

    gender = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(2),
        ],
        null=True,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE,
    )

    age = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(100),
        ],
        null=True,
    )
    nickname = models.CharField(max_length=40, blank=True)

    email = models.EmailField(max_length=40, blank=True)

    image = models.ImageField(upload_to="user_path/%Y/%m/%d", blank=True, null=True)
