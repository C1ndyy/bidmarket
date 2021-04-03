from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('messages/', views.message_index, name='message_index'),
    path('messages/<int:thread_id>/', views.message_detail, name='message_detail'),
    path('listings/', views.listings_index, name='listings_index'),
]