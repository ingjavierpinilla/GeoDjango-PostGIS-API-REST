from django.contrib import admin
from .models import Dataset, Row

class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Row)