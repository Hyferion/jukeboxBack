from django.contrib import admin

from Juki.models import User, Playlist, Song, Vote

admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(Vote)
