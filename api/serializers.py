from rest_framework import serializers

from api.models.events import Event

class EventListSerializers(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('geoposition', 'title', 'id' , 'slug', 'description', 'picture')