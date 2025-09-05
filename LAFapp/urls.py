from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('save_data/', views.save_data, name='save_data'),
	path('lost/', views.lost, name='lost'),
	path('found/', views.found, name='found'),
    path('contact/',views.contact, name='contact'),
	
    path('lost_items/', views.LostItemsAPIView.as_view(), name='lost_items_search'),
    path('found_items/', views.FoundItemsAPIView.as_view(), name='found_items_search'),
]
