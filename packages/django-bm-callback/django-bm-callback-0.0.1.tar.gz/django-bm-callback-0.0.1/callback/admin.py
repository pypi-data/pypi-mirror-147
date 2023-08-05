
from django.contrib import admin
from apps.callback.models import Callback

@admin.register(Callback)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'phone', 'descriptions', 'executed', 'outstanding']
