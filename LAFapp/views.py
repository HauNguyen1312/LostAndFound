from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Items

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemsSerializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def index(request):
	return render(request, 'LAF/index.html')

def save_data(request):
	if request.method == "POST":
		status = request.POST.get("status")
		description = request.POST.get("description")
		location = request.POST.get("location")
		email = request.POST.get("email")
		date = request.POST.get("date")
		category = request.POST.get("category")
		key_word = request.POST.get("key_word")
		Items.objects.create(status=status, description=description, location=location, email=email, date=date, category=category, key_word=key_word)
	return redirect(index)


def lost(request):
	list_lost = Items.objects.filter(status = 'lost')
	return render(request, 'LAF/lost_page.html', {'list_lost': list_lost})


def found(request):
	list_found = Items.objects.filter(status = 'found')
	return render(request, 'LAF/found_page.html', {'list_found': list_found})

class LostItemsAPIView(APIView):
	def get(self, request, *args, **kwargs):
		query = self.request.query_params.get('q', '')

		queryset = Items.objects.filter(status='lost')

		if query:
			search_vector = SearchVector('description', 'location', 'category','key_word')
			search_query = SearchQuery(query)


			queryset = queryset.annotate(
				search=search_vector,
				rank = SearchRank('search', search_query)
				).filter(search=search_query).order_by('-rank')

		serializer = ItemsSerializers(queryset, many=True)
		return Response(serializer.data)


class FoundItemsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('q', '')

        # Filter by 'found' status first
        queryset = Items.objects.filter(status='found')

        if query:
            # Create a search vector from the desired fields
            search_vector = SearchVector('description', 'location', 'category', 'key_word')
            search_query = SearchQuery(query)

            # Perform the search and order by relevance (search rank)
            queryset = queryset.annotate(
                search=search_vector
            ).filter(search=search_query).order_by('-rank')
        
        serializer = ItemsSerializer(queryset, many=True)
        return Response(serializer.data)
# class ItemViewSet(viewsets.ModelViewSet):
# 	query_set = Items.objects.all()
# 	seri_class = ItemsSerializers

# 	@action(detail=False, methods=['get'])
# 	def search(self, request):
# 		query = request.query_params.get('query', None)
# 		status_filter = request.query_params.get('status', None)

# 		s = ItemDocument.search()

# 		if status_filter:
# 			s = s.filter('term', status = status_filter)

# 		if query:
# 			s = s.query(
# 				'multi_match',
# 				query = query,
# 				fields = ['description', 'location', 'category', 'key_word'],
# 				fuzziness = 'AUTO'
# 			)

# 		response = s.execute()

# 		item_ids = [hit.meta.id for hit in response]

# 		items = Items.objects.filter(id__in=item_ids)
# 		return Response(serializer.data, status = status.HTTP_200_OK)


# 	@action(detail=False, methods=['get'])
# 	def lost_item(self, request):
# 		items = self.get_queryset().filter(status='lost')
# 		serializer = self.get_serializer(items, many=True)
# 		return Response(serializer.data)


# 	@action(detail=False, methods=['get'])
# 	def found_item(self, request):
# 		items = self.get_queryset().filter(status='found')
# 		serializer = self.get_serializer(items, manay=True)
# 		return Response(serializer.data)