from django.contrib import admin
from . models import *


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'title', 'due', 'is_finished')
    list_editable = ('is_finished',)


admin.site.register(Notes)
admin.site.register(HomeWork, HomeworkAdmin)
admin.site.register(Todo)
