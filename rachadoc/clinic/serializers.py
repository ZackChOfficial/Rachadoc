from rest_flex_fields import FlexFieldsModelSerializer
from rachadoc.clinic.models import Clinic
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class ClinicSerializer(GeoFeatureModelSerializer, FlexFieldsModelSerializer):
    class Meta:
        model = Clinic
        geo_field = "point"
        fields = ("id", "name", "address", "point", "description", "phone_number", "email_address")
