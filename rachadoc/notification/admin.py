from django.contrib import admin
from notification.models import Notification, AppointementNotification


class NotificationAdmin(admin.ModelAdmin):
    pass


class AppointementNotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppointementNotification, AppointementNotificationAdmin)
