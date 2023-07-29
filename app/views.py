from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.views import generic


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
    if homework.is_finished == True:
    # if not homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    HomeWork.objects.get(id=pk).delete()
    return redirect('homework')