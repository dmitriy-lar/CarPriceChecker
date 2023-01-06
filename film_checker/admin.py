from django.contrib import admin
from .models import Film, CheckOne


class CheckOneAdmin(admin.ModelAdmin):
    readonly_fields = ('checked_time',)
    list_display = ('checked_time', )


admin.site.register(Film)
admin.site.register(CheckOne)
