from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from tests.models import Word, WordToUser, Lesson, LessonToUser
from random import randint
from django.http import HttpResponse
import json
import os
from lianaSite.settings import STATIC_URL

def learn(request):

    user = request.user
    #print(user)
    if not user.is_authenticated:
        return HttpResponseRedirect("/login/login")	
    
    lessID = request.GET.get("id", None)
	
    if lessID ==None:
        lessonsAll = Lesson.objects.all()
        usedLessons = list(map(lambda less: less.lessID, LessonToUser.objects.filter(userID = user)))
        lessons = list(filter(lambda les: usedLessons.count(les)==0, lessonsAll))
        return TemplateResponse(request,  "lessons.html", {'lessons':lessons})
    else:
        lesson = Lesson.objects.get(id = lessID)
        words = Word.objects.filter(lessonID=lesson)
		
        wordsToUser = WordToUser.objects.filter(userID=user)#все слова, которые смотрел юзер
        wordsIDs = list(map(lambda wtu:wtu.wordID, wordsToUser))
        words = list(filter(lambda word: wordsIDs.count(word)==0, words))
	
        if len(words)==0:
            ltw = LessonToUser(userID = user, lessID = lesson)
            ltw.save()			
            return TemplateResponse(request, "no_words_learn.html", {'lesson':lesson})
		
        ind = randint(0,len(words)-1)
        word = words[ind]
	
        wTU = WordToUser(userID=user, wordID=word, trainCounts=0, successCounts=0)
        wTU.save()
        return TemplateResponse(request,  "learn.html", {'word':word})
	
def train(request):
    user = request.user
    #print(user)
    if not user.is_authenticated:
        return HttpResponseRedirect("/login/login")	
    
    words = Word.objects.all()	

	
    wordsToUser = WordToUser.objects.filter(userID=user)#все слова, которые смотрел юзер
    wordsIDs = list(map(lambda wtu:wtu.wordID, wordsToUser))
    words = list(filter(lambda word: wordsIDs.count(word)!=0, words))

    words = [ (wTU.successCounts/wTU.trainCounts if wTU.trainCounts > 0 else 0, word) for wTU in wordsToUser for word in words if wTU.wordID == word] 	
   
    if len(words)==0:
	    return render(request, "no_words_train.html")

    words = list(sorted(words, key = lambda c: c[0]))	
    word = words[0]

    return TemplateResponse(request,  "train.html", {'word':word[1]})
	
def trainCheck(request):
    user = request.user
    wordRus = request.POST["rus"]
    wordEng = request.POST["eng"]
	
    word = Word.objects.get(english=wordEng)
    wTU = WordToUser.objects.get(wordID=word, userID=user)
    wTU.trainCounts+=1
    res = None
    if wordRus==word.russian:
        wTU.successCounts+=1
        wTU.save()
        res = "Ok"
        #return HttpResponse("Ok")
    else:
        wTU.save()
        res = "No"
        #return HttpResponse("No")
    toJSON ={'state':res, 'rus':word.russian, 'img':os.path.join(STATIC_URL, word.picture)} 	
    return HttpResponse(json.dumps(toJSON))