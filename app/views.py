from django.shortcuts import render
from . forms import *
from django.contrib import messages


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
