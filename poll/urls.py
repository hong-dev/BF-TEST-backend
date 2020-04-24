from .views      import QuestionView, ResultView
from django.urls import path

urlpatterns = [
    path('/<int:question_id>', QuestionView.as_view()),
    path('/result', ResultView.as_view())
]
