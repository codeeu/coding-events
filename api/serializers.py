from django.utils.text import Truncator
from rest_framework import serializers

from api.models.events import Event


class EventListSerializers(serializers.ModelSerializer):
    description_short = serializers.CharField(source='description')

    class Meta:
        model = Event
        fields = (
            'geoposition',
            'title',
            'id',
            'slug',
            'description_short',
            'picture')

    def transform_description_short(self, obj, value):
        return Truncator(value).chars(160)


class ScoreboardSerializer(serializers.Serializer):
    country_name = serializers.CharField()
    score = serializers.FloatField()
    events = serializers.IntegerField()
    country_code = serializers.CharField(max_length=2)
