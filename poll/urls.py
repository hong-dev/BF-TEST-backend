from .views      import EachQuestionView, QuestionView, ResultView
from django.urls import path

urlpatterns = [
    path('/<int:question_id>', EachQuestionView.as_view()),
    path('/question', QuestionView.as_view()),
    path('/result', ResultView.as_view()),
]
