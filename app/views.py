from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests



def home(request):
    return render(request, 'app/home.html')



def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request, "Note added successfully!")
            return redirect('notes')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    
    context = {
        'notes': notes,
        'form': form,
    }
    
    return render(request, 'app/notes.html', context)



def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')



class NotesDetailView(generic.DetailView):
    model = Notes
    
    
    
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
                
            homeworks = HomeWork(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request, "Homework added successfully!")
            return redirect('homework')
    else:
        form = HomeworkForm()
    homeworks = HomeWork.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    
    context = {
        'homeworks': homeworks,
        'homework_done': homework_done,
        'form': form,
    }
    return render(request, 'app/homework.html', context)



def update_homework(request, pk=None):
    homework = HomeWork.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')



def delete_homework(request, pk=None):
    homework = HomeWork.objects.get(id=pk)
    homework.delete()
    return redirect('homework')



class HomeworkDetailView(generic.DetailView):
    model = HomeWork
    


def youtube(request):
    form = UniForm()
    text = request.GET.get('text', '')  # Get the search query from the URL query parameter
    if text:  # If there is a search query, perform the search
        video = VideosSearch(text, limit=20)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnails': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'viewcount': i['viewCount']['short'],
                'publishedTime': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            
        # pagination
        paginator = Paginator(result_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': form,
            'results': result_list,
            'page_obj': page_obj,
        }
        return render(request, 'app/youtube.html', context)

    context = {
        'form': form,
    }
    return render(request, 'app/youtube.html', context)



def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
                
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished,
            )
            todos.save()
            messages.success(request, "Todo added successfully!")
            return redirect('todo')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
        
    context = {
        'todos': todo,
        'form': form,
        'todos_done': todos_done,
    }
    return render(request, 'app/todo.html', context)



def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')


def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    return redirect('todo')


def books(request):
    form = UniForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        if 'items' in answer:
            for i in range(10):
                result_dict = {
                    'title': answer['items'][i]['volumeInfo']['title'],
                    'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description': answer['items'][i]['volumeInfo'].get('description'),
                    'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories': answer['items'][i]['volumeInfo'].get('categories'),
                    'rating': answer['items'][i]['volumeInfo'].get('averageRating'),
                    'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
                    'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
                }
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list,
            }
            return render(request, 'app/books.html', context)

    else:
        form = UniForm()

    context = {
        'form': form,
    }
    return render(request, 'app/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = UniForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            print('synonyms:', synonyms)
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
                
            }
        except:
             context = {
                'form': form,
                'input': '',
             }
        return render(request, 'app/dictionary.html', context)
    else:
        form = UniForm()
        context = {
            'form': form,
        }
    return render(request, 'app/dictionary.html', context)
