from django.contrib import admin

from notification.models import Notification, UserObj

admin.site.register(Notification)
admin.site.register(UserObj)
