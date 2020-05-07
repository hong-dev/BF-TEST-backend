import json
import datetime

from .models import (
    Question,
    Choice,
    Case,
    Stack,
    User,
    Response,
    Result,
)

from django.views     import View
from django.shortcuts import render
from django.http      import HttpResponse, JsonResponse
from django.db        import connection


class PingView(View):
    def get(self, request):
        return HttpResponse("pong")

class EachQuestionView(View):
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
                    'choice' : choice["choice"],
                } for choice in choices ]
        }

        return JsonResponse({"question_data" : question_data}, status = 200)

class QuestionView(View):
    def get(self, request):
        question_data = [
            {
                'id'        : question.id,
                'question'  : question.question,
                'image_url' : question.image_url,
                'choice'    : [
                    {
                        'id'     : choice.id,
                        'choice' : choice.choice,
                    } for choice in Choice.objects.filter(question_id = question.id)]
            } for question in Question.objects.all() ]

        return JsonResponse({"question_data" : question_data}, status = 200)

class ResultView(View):
    def post(self, request):
        try:
            score      = json.loads(request.body)["answer"]
            p_type     = json.loads(request.body)["type"]
            browser    = request.META['HTTP_USER_AGENT']
            ip_address = request.META['REMOTE_ADDR']

            user = User(
                browser    = browser,
                ip_address = ip_address
            )
            user.save()

            count_front = 0
            count_valid_question = 0
            for question_id, choice_id in score.items():
                Response(
                    user_id     = user.id,
                    question_id = int(question_id),
                    choice_id   = choice_id
                ).save()

                if Choice.objects.select_related('stack').get(id = choice_id).stack.id == 1:
                    count_front += 1

                if Choice.objects.select_related('stack').get(id = choice_id).stack.id != 4:
                    count_valid_question += 1

            if count_front == count_valid_question/2:
                result  = Result.objects.get(stack = 3)
                dev_fit = Result.objects.get(stack = 3)
            elif count_front > count_valid_question/2:
                result  = Result.objects.get(case__name = p_type, stack = 1)
                dev_fit = Result.objects.get(case__name = p_type, stack = 2)
            else:
                result  = Result.objects.get(case__name = p_type, stack = 2)
                dev_fit = Result.objects.get(case__name = p_type, stack = 1)

            user.result_id = result.id
            user.save()

            user_result = {
                'name'        : result.name,
                'description' : result.description,
                'image_url'   : result.image_url,
                'audio_url'   : result.audio_url,
                'dev_fit'     : dev_fit.name
            }

            return JsonResponse({"result" : user_result}, status = 200)

        except KeyError:
            return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)

class StatUserView(View):
    def get(self, request):
        today = datetime.datetime.today()
        start_at = request.GET.get('start', today.strftime('%Y%m%d00'))
        end_at   = request.GET.get('end', (today + datetime.timedelta(days=1)).strftime('%Y%m%d00'))
        query    = """select
                    r.user_id,
                    count(case when s.name = 'Front' then s.name end) as Front,
                    count(case when s.name = 'Back' then s.name end) as Back,
                    concat(round(count(case when s.name = 'Front' then s.name end) * 100 / 8), '%') as 'F/Total(%)',
                    re.name as Result, u.created_at,
                    u.ip_address,
                    u.browser
                    from responses as r
                    left join users as u on u.id = r.user_id
                    left join results as re on re.id = u.result_id
                    left join choices as c on r.choice_id = c.id
                    left join stacks as s on s.id = c.stack_id
                    where r.user_id > 0"""\
                    + ' AND r.created_at >= ' +"'"+ str(datetime.datetime.strptime(start_at, '%Y%m%d%H'))+"'"\
                    + ' AND r.created_at <= ' +"'"+ str(datetime.datetime.strptime(end_at, '%Y%m%d%H'))+"'"\
                    + ' group by r.user_id'
        with connection.cursor() as cursor:
            cursor.execute(query)
            query = cursor.fetchall()
        return render(request, 'stat_user.html', {'query': query})

class StatResultView(View):
    def get(self, request):
        today = datetime.datetime.today()
        start_at = request.GET.get('start', today.strftime('%Y%m%d00'))
        end_at   = request.GET.get('end', (today + datetime.timedelta(days=1)).strftime('%Y%m%d00'))
        query    = """select r.id, r.name, count(r.id) as count
                    from users as u
                    left join results as r on r.id = u.result_id
                    where u.id > 0"""\
                    + ' AND r.created_at >= ' +"'"+ str(datetime.datetime.strptime(start_at, '%Y%m%d%H'))+"'"\
                    + ' AND r.created_at <= ' +"'"+ str(datetime.datetime.strptime(end_at, '%Y%m%d%H'))+"'"\
                    + ' group by r.id with ROLLUP;'
        with connection.cursor() as cursor:
            cursor.execute(query)
            query = cursor.fetchall()
        return render(request, 'stat_result.html', {'query': query})

class StatQuestionView(View):
    def get(self, request):
        today = datetime.datetime.today()
        start_at = request.GET.get('start', today.strftime('%Y%m%d00'))
        end_at   = request.GET.get('end', (today + datetime.timedelta(days=1)).strftime('%Y%m%d00'))
        query    = """SELECT q.question, c.choice, count(r.id) as count, CONCAT(TRUNCATE(100*count(r.id)/cr.crt,1), '%') as '(%)'
                    from responses as r
                    left join questions as q on r.question_id = q.id
                    left join choices as c on c.id = r.choice_id
                    left join users as u on u.id = r.user_id
                    left join (select question_id, count(question_id) as crt
                    from responses
                    where user_id > 0
                    group by question_id) as cr on cr.question_id = r.question_id
                    where r.user_id > 0"""\
                    + ' AND r.created_at >= ' +"'"+ str(datetime.datetime.strptime(start_at, '%Y%m%d%H'))+"'"\
                    + ' AND r.created_at <= ' +"'"+ str(datetime.datetime.strptime(end_at, '%Y%m%d%H'))+"'"\
                    + ' group by q.question, c.choice with ROLLUP;'
        with connection.cursor() as cursor:
            cursor.execute(query)
            query = cursor.fetchall()
        return render(request, 'stat_question.html', {'query': query})
