from django.shortcuts import render,redirect
from dictApp.models import *
from dictApp.forms import WordForm
def home(request):
    if request.method=="GET":
        context = {
            'Title': 'My dictionary',
            'active': 'My dictionary'
        }
        return render(request,"home.html",context=context)

def words_list(request):
    if request.method=="GET":
        words = Word.objects.all()
        context = {
            'Title': 'My dictionary',
            'active': 'Words list',
            
        }
        if words:
            context['words'] = words
        
        return render(request, 'words_list.html', context)

def add_word(request):
    if request.method=="GET":
        context = {
            'Title': 'My dictionary',
            'active': 'Add word',
            'form' : WordForm()
        }
        return render(request, 'add_word.html', context)
    else:
        context = {
            'Title': 'My dictionary',
            'active': 'Add word',
            'form' : WordForm()
        }
        try:
            data = request.POST
            word = Word.objects.create(word=data["word"], translation=data["translation"])
            word.save()
            success = f'Слово "{str(word)}" добавлено'
            context['success'] = success
            return render(request, 'add_word.html', context)
        except Exception as ex:
            context['error'] = ex
            return render(request, 'add_word.html', context)
# Create your views here.
