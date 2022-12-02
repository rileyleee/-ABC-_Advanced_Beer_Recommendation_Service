from django.contrib import admin
from community.models import Column, Event, Board


# @admin.register(Column)
# class ColumnAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Column)
admin.site.register(Event)
admin.site.register(Board)