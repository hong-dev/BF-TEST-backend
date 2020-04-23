from .views      import QuestionView
from django.urls import path

urlpatterns = [
    path('/<int:question_id>', QuestionView.as_view()),
]
