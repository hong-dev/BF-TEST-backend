from django.views import View
from django.http  import HttpResponse, JsonResponse

class QuestionView(View):
    def get(self, request, question_id):
        questions = Question.objects.filter(id = question_id).values()

        return JsonResponse({"question" : quetions[0]}, status = 200)
