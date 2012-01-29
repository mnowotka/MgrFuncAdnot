from gui.models import Task, Subtask, RawResult, InferredResult
from django.contrib import admin

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [SubtaskInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask)
admin.site.register(RawResult)
admin.site.register(InferredResult)
