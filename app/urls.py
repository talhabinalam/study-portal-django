from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('note_detail/<int:pk>', views.NotesDetailView.as_view(), name='note_detail'),
    path('homework/', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update_homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete_homework'),
]