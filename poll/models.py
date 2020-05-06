from django.db import models

class Question(models.Model):
    question   = models.CharField(max_length = 1000, null = True)
    image_url  = models.URLField(max_length = 2000, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'questions'

class Choice(models.Model):
    choice     = models.CharField(max_length = 500, null = True)
    question   = models.ForeignKey(Question, on_delete = models.SET_NULL, null = True)
    stack      = models.ForeignKey('Stack', on_delete = models.SET_NULL, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'choices'

class Case(models.Model):
    name       = models.CharField(max_length = 100, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'cases'

class Stack(models.Model):
    name       = models.CharField(max_length = 100, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'stacks'

class User(models.Model):
    name       = models.CharField(max_length = 100, null = True)
    result     = models.ForeignKey('Result', on_delete = models.SET_NULL, null = True)
    browser    = models.CharField(max_length = 100, null = True)
    ip_address = models.CharField(max_length = 100, null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'users'

class Response(models.Model):
    user       = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    question   = models.ForeignKey(Question, on_delete = models.SET_NULL, null = True)
    choice     = models.ForeignKey(Choice, on_delete = models.SET_NULL, null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'responses'

class Result(models.Model):
    name        = models.CharField(max_length = 500, null = True)
    description = models.TextField(null = True)
    case        = models.ForeignKey(Case, on_delete = models.SET_NULL, null = True)
    stack       = models.ForeignKey(Stack, on_delete = models.SET_NULL, null = True)
    image_url   = models.URLField(max_length = 2000, null = True)
    audio_url   = models.URLField(max_length = 2000, null = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'results'