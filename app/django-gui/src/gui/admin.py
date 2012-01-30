from gui.models import Task, Subtask, RawResult, InferredResult
from django.contrib import admin

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [SubtaskInline]
    list_display = ('task_name', 'user', 'seq_file')

class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'seq_format', 'short_seq')

class RawResultAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'short_result')

class InferredResultAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'probability', 'short_result')

admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask, SubtaskAdmin)
admin.site.register(RawResult, RawResultAdmin)
admin.site.register(InferredResult, InferredResultAdmin)

