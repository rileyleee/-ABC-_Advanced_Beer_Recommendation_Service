from django.contrib import admin
from account.models import User
from account.models import Profile

admin.site.register(User)
admin.site.register(Profile)
