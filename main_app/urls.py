from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('messages/', views.message_index, name='message_index'),
    path('messages/<int:thread_id>/', views.message_detail, name='message_detail'),
    path('messages/<int:thread_id>/send_message', views.send_message, name='send_message'),
    path('listings/', views.listings_index, name='listings_index'),
    path('profile/', views.profile, name='profile'),
    path('listings/create/', views.listings_create, name='listings_create'),
    path('listings/new/', views.listings_new, name='listings_new'),
    #listings detail has websockets as well now
    path('listings/<int:listing_id>/', views.listings_detail, name='listings_detail'),
    path('listings/<int:listing_id>/new_message', views.new_message, name='new_message'),
    path('listings/<int:listing_id>/update', views.listings_update, name='listings_update'),
    path('listings/<int:listing_id>/delete', views.listings_delete, name='listings_delete'),
    path('listings/<int:listing_id>/add_photo/', views.add_photo, name='add_photo'),
    path('listings/<int:listing_id>/update_item/', views.update_item, name='update_item'),
    path('listings/<int:photo_id>/delete_photo/', views.delete_photo, name='delete_photo'),
    path('listings/<int:listing_id>/bid', views.bid, name='bid'),
]