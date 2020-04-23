import json

from .models import (
    Question,
    Choice,
    Case,
    Stack,
    User,
    Response,
    Result
)

from django.views        import View
from django.http         import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

class QuestionView(View):
    def get(self, request, question_id):
        questions = (
            Question.
            objects.
            get(id = question_id)
        )

        choices = (
            Choice.
            objects.
            filter(question_id = questions.id).
            values()
        )

        question_data = {
            'id'        : questions.id,
            'question'  : questions.question,
            'image_url' : questions.image_url,
            'choice'    : [
                {
                    'id'     : choice["id"],
                    'choice' : choice["choice"]
                } for choice in choices ]
        }

        return JsonResponse({"question_data" : question_data}, status = 200)

#class ResultView(View):
#    def post(self, request):
#        try:
#            score  = json.loads(request.body)["answer"]
#            p_type = json.loads(request.body)["type"]
#            browser = request.META['HTTP_USER_AGENT']
#            ip = request.META.get('HTTP_X_FORWARDED_FOR')
#
#            Response = (
#                response = score,
#                case = p_type,
#                browser = browser,
#                ip_address = ip
#            ).save()
#
#            if sum(score) == len(score)/2:
#                result = Result.objects.filter(id=4).values()
#
#            elif sum(score) > len(score)/2:
#
#            elif sum(score) < len(score)/2:
#
#
#        return JsonResponse({"question" : quetions[0]}, status = 200)
