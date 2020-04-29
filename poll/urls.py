from .views      import QuestionView, ResultView, PingView
from django.urls import path

urlpatterns = [
    path('/<int:question_id>', QuestionView.as_view()),
    path('/result', ResultView.as_view()),
    path('', PingView.as_view()),
]
