from .views      import (
    EachQuestionView,
    QuestionView,
    ResultView,
    StatUserView,
    StatResultView,
    StatQuestionView
)
from django.urls import path

urlpatterns = [
    path('/<int:question_id>', EachQuestionView.as_view()),
    path('/question', QuestionView.as_view()),
    path('/result', ResultView.as_view()),
    path('/stat-user', StatUserView.as_view()),
    path('/stat-result', StatResultView.as_view()),
    path('/stat-question', StatQuestionView.as_view()),
]
