from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Items

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemsSerializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail

def index(request):
	return render(request, 'LAF/index.html')

def contact(request):
	return render(request, 'LAF/contact.html')

def save_data(request):
	if request.method == "POST":
		status = request.POST.get("status")
		description = request.POST.get("description")
		location = request.POST.get("location")
		email = request.POST.get("email")
		# date_string = request.POST.get("date")
		date = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
		category = request.POST.get("category")
		key_word = request.POST.get("key_word")
		create_item = Items.objects.create(status=status, description=description, location=location, email=email, date=date, category=category, key_word=key_word)
		if create_item:
			alert = 'Your report is completed...!'
		else:
			alert = 'Your report have something wrong...!'

		if status == "lost":
			start_date = create_item.date - timedelta(days=2)
			end_date = create_item.date + timedelta(days=2)

			# matches = Items.objects.filter(description__icontains=create_item.description).filter(location__icontains=create_item.location).filter(category__icontains=create_item.category).date__range=(start_date, end_date).filter(status='found').values()
			matches = Items.objects.filter(description__icontains=create_item.description).filter(location__icontains=create_item.location).filter(status='found').filter(date__range=[start_date, end_date]).values()

		if status =="found":
			matches = Items.objects.filter(description__icontains=create_item.description).filter(location__icontains=create_item.location).filter(status='lost').values()


		if matches.exists():
			subject = "Potential Match Found for Your Lost Item!"
			message = f"Hello,\n\nWe found potential matches for your lost item:\n\n"
			for match in matches:
				message += f" - Item Description: {match['description']}\n"
				message += f"   Location Found: {match['location']}\n"
				message += f"   Date Found: {match['date'].strftime('%Y-%m-%d')}\n\n"

			message += "Please contact the system administrator for more information."

			send_mail(
				subject,
				message,
				'noreply@gmail.com',
				[create_item.email],
				fail_silently=False,
			)
	return render(request, 'LAF/index.html', {'alert': alert})


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
