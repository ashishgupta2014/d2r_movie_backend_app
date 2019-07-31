from rest_framework import serializers,validators
from movie.models import *
class MovieSerializer(serializers.ModelSerializer):
	"""
	list or create movie model
	"""
	class Meta:
		model=Movie
		fields = '__all__'