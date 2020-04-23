import json

from .models import Question, Response, Result

from django.views import View
from django.http  import HttpResponse, JsonResponse

class QuestionView(View):
    def get(self, request, question_id):
        questions = Question.objects.filter(id = question_id).values()

        return JsonResponse({"question" : quetions[0]}, status = 200)

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
