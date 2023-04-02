from rest_flex_fields import FlexFieldsModelSerializer
from rachadoc.common.models import Tarif, Picture, Expertise


class TarifSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Tarif
        fields = ("doctor", "clinic", "title", "description", "amount")


class PictureSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Picture
        fields = ("description", "clinic", "url")


class ExpertiseSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Expertise
        fields = ("id", "name", "description")
