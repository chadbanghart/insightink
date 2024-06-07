from django.contrib import admin
from .models import Journal, Entry, Travel, Wellness, Photo

# Register your models here.
admin.site.register(Journal)
admin.site.register(Entry)
admin.site.register(Travel)
admin.site.register(Wellness)
admin.site.register(Photo)