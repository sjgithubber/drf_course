from django.contrib import admin
from .models import Contact
# Register your models here.

# we register this new model this way???
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # why are we doing this one?
    list_display = ('id', 'title', 'description', 'email')