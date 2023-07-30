from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch



def home(request):
    return render(request, 'app/home.html')



def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request, "Note added successfully!")
            form = NotesForm()
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
    # if not homework.is_finished:
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    HomeWork.objects.get(id=pk).delete()
    return redirect('homework')



class HomeworkDetailView(generic.DetailView):
    model = HomeWork
    


def youtube(request):
    form = YoutubeForm()
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