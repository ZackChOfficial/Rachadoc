from rest_flex_fields import FlexFieldsModelSerializer
from clinic.models import Clinic
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class ClinicSerializer(GeoFeatureModelSerializer, FlexFieldsModelSerializer):
    class Meta:
        model = Clinic
        fields = ("name", "address", "point", "description", "phone_number", "email_address")
