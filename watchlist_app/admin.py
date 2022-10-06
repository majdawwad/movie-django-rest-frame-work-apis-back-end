from django.contrib import admin
from watchlist_app import models

admin.site.register(models.WatchList)
admin.site.register(models.StreamPlatform)
admin.site.register(models.Review)
