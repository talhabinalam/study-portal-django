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
    homeworks = HomeWork.objects.filter(user=request.user)
    
    context = {
        'homeworks': homeworks,
    }
    return render(request, 'app/homework.html', context)