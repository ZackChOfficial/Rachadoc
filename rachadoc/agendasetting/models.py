from django.db import models
from agendasetting.managers import AgendaSettingManager
from core.lib.mixins import BaseTimestampedModel


class AgendaSetting(BaseTimestampedModel):
    objects = AgendaSettingManager()
