from django.contrib import admin
from community.models import Column, Event


# @admin.register(Column)
# class ColumnAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Column)
admin.site.register(Event)
