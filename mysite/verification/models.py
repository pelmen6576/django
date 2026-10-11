from django.db import models

# Create your models here.

class Person(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    nickname=models.CharField(max_length=10,unique=True)
    password=models.CharField(max_length=100)

class Questions(models.Model):
    id_persons=models.ForeignKey(Person,on_delete=models.CASCADE)
    questions=models.TextField()
    date=models.DateField(auto_now_add=True)

class Answers(models.Model):
    id_persons=models.ForeignKey(Person,on_delete=models.CASCADE)
    id_questions=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answers=models.TextField()
    date=models.DateField(auto_now_add=True)
    