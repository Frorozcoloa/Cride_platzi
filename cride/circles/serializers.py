"""Circle serializer. """

#DRF
from rest_framework import serializers

# Models
from cride.circles.models import Circle
from rest_framework.validators import UniqueValidator

class CircleSerializer(serializers.Serializer):
    """Circle serializer. """

    name = serializers.CharField(max_length=100)
    slug_name = serializers.SlugField(max_length=100)
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()

class CreateCircleSerializer(serializers.Serializer):
    """Create circle serializer. """

    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(max_length=140, validators=[UniqueValidator(queryset=Circle.objects.all())])
    about = serializers.CharField(max_length=255, required=False)
    members_limit = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """Create and return a new `Circle` instance, given the validated data."""

        return Circle.objects.create(**validated_data)