from django.contrib import admin
from rachadoc.events.models import Appointement


class AppointementAdmin(admin.ModelAdmin):
    pass


admin.site.register(Appointement, AppointementAdmin)
