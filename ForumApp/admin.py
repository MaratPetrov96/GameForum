from django.contrib import admin
from .models import *

# Register your models here.

try:
    admin.site.register(Tag)
except:
    pass

class Post(admin.TabularInline):
    model = Idea.tags.through
    extra = 2

try:
    @admin.register(Idea)
    class OfferAdmin(admin.ModelAdmin):
        inlines = (Post,)
        exclude = ('tags',)
except:
    pass

admin.site.register(Comment)
