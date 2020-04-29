from django.urls import path, include

urlpatterns = [
    path('poll', include('poll.urls')),
    path('ping', include('poll.urls')),
]
