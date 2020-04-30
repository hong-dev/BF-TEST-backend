from django.urls import path, include
from poll.views  import PingView

urlpatterns = [
    path('poll', include('poll.urls')),
    path('ping', PingView.as_view()),
]
