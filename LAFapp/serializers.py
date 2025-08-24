from rest_framework import serializers
from LAFapp import models

class ItemsSerializers(serializers.ModelSerializer):
	class Meta:
		model = models.Items
		fields = "__all__"