from django.contrib import admin
from .models import Player,Match
# Register your models here. Used to let the admin modify stuff

admin.site.register(Player)
admin.site.register(Match)