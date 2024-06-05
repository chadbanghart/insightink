from django.contrib import admin
from .models import Journal, Entry

# Register your models here.
admin.site.register(Journal)
admin.site.register(Entry)