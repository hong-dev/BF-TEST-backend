from django.db import models

class Question(models.Model):
    question   = models.CharField(max_length = 1000, null = True)
    choice_1   = models.CharField(max_length = 500, null = True)
    choice_2   = models.CharField(max_length = 500, null = True)
    image_url  = models.URLField(max_length = 2000, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'questions'

class Response(models.Model):
    response   = models.CharField(max_length = 500, null = True)
    case       = models.CharField(max_length = 20, null = True)
    result     = models.ForeignKey('Result', on_delete = models.SET_NULL, null = True)
    browser    = models.CharField(max_length = 100, null = True)
    ip_address = models.CharField(max_length = 100, null = True)

    class Meta:
        db_table = 'responses'

class Result(models.Model):
    name        = models.CharField(max_length = 500, null = True)
    description = models.TextField(null = True)
    image_url   = models.URLField(max_length = 2000, null = True)
    audio_url   = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = 'results'
