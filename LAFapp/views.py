from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Items
from .forms import ItemsForm

def index(request):
	return render(request, 'LAF/index.html')

# def save_data(request):
# 	if request.method == "POST":
# 		print(request)
# 		form = ItemsForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect(index)
# 		else:
fields = ['status', 'description', 'location', 'email', 'date', 'category', 'key_word']
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
	context = {}
	return redirect(index)


def lost(request):
	list_lost = Items.objects.filter(status = 'lost')
	return render(request, 'LAF/lost_page.html', {'list_lost': list_lost})


def found(request):
	list_found = Items.objects.filter(status = 'found')
	return render(request, 'LAF/found_page.html', {'list_found': list_found})