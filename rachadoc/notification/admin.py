from django.contrib import admin
from rachadoc.notification.models import Notification, AppointementNotification


class NotificationAdmin(admin.ModelAdmin):
    pass


class AppointementNotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppointementNotification, AppointementNotificationAdmin)
