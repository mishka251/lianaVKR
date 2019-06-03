from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lesson(models.Model):
    name = models.CharField(max_length=60)

class Word(models.Model):
    english = models.CharField(max_length=60)
    russian = models.CharField(max_length=60)
    picture = models.FilePathField()
    lessonID = models.ForeignKey(Lesson, on_delete=models.CASCADE)
	
class WordToUser(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    wordID = models.ForeignKey(Word, on_delete=models.CASCADE)
    trainCounts = models.IntegerField()
    successCounts = models.IntegerField()
	
class LessonToUser(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    lessID = models.ForeignKey(Lesson, on_delete=models.CASCADE)	
	

	
