from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Items

@registry.register_document
class ItemDocument(Document):
	class Index:
		name = "Items"

		settings = {'number_of_shards': 1, 'number_of_replicas': 0}

	class Django:
		model = Items

		fields = [
			'status',
			'description',
			'location',
			'category',
			'key_word',
		]