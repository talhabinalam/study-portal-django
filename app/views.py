from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
from django.urls import reverse
from wikipedia.exceptions import PageError
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
import wikipedia



def home(request):
    return render(request, 'app/home.html')



@login_required
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



@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')



@method_decorator(login_required, name='dispatch')
class NotesDetailView(generic.DetailView):
    model = Notes
    


@login_required
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



@login_required
def update_homework(request, pk=None):
    homework = HomeWork.objects.get(id=pk)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()

    # Check the referrer to determine where to redirect
    referer = request.META.get('HTTP_REFERER', '')

    # If the referrer contains 'profile' in its URL, redirect to 'profile' view
    if 'profile' in referer:
        return redirect(reverse('profile'))

    # Otherwise, redirect to 'homework' view
    return redirect(reverse('homework'))



@login_required
def delete_homework(request, pk=None):
    homework = HomeWork.objects.get(id=pk)
    homework.delete()

    referer = request.META.get('HTTP_REFERER', '')

    if 'profile' in referer:
        return redirect(reverse('profile'))

    return redirect(reverse('homework'))



@method_decorator(login_required, name='dispatch')
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



@login_required
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



@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()

    referer = request.META.get('HTTP_REFERER', '')

    if 'profile' in referer:
        return redirect(reverse('profile'))

    return redirect(reverse('todo'))



@login_required
def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    todo.delete()

    referer = request.META.get('HTTP_REFERER', '')

    if 'profile' in referer:
        return redirect(reverse('profile'))

    return redirect(reverse('todo'))



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



def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = UniForm(request.POST)
        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary,
            }
        except PageError:
            context = {
                'form': form,
                'error': 'Page not found. Try another search term.',
            }
        return render(request, 'app/wiki.html', context)
    else:
        form = UniForm()
        context = {
            'form': form,
        }
    return render(request, 'app/wiki.html', context)



def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer,
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer,
                } 
            
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False,
        }
    return render(request, 'app/conversion.html', context)
    


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
            return redirect('login')
            
    else:
        form = UserRegForm()
    context = {
        'form': form,
    }
    return render(request, 'app/register.html', context)



class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "You are logged in succesfully!")
        return response



@login_required
def profile(request):
    homeworks = HomeWork.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homeworks_done': homeworks_done,
        'todos_done': todos_done,
    }
    
    return render(request, 'app/profile.html', context)