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
		check = Items.objects.create(status=status, description=description, location=location, email=email, date=date, category=category, key_word=key_word)
		if check:
			message = 'Your report is completed...!'
		else:
			message = 'Your report have something wrong...!'
	return render(request, 'LAF/index.html', {'message': message})


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
			search_vector = SearchVector('description', 'category','key_word')
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
            search_vector = SearchVector('description', 'category', 'key_word')
            search_query = SearchQuery(query)

            # Perform the search and order by relevance (search rank)
            queryset = queryset.annotate(
                search=search_vector,
                rank = SearchRank('search', search_query)
            ).filter(search=search_query).order_by('-rank')
        
        serializer = ItemsSerializers(queryset, many=True)
        return Response(serializer.data)
