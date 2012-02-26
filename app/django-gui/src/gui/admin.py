from gui.models import Task, Subtask, RawResult, InferredResult, TaskSettings
from django.contrib import admin

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1
    
class TaskSettingsInline(admin.TabularInline):
    model = TaskSettings
    extra = 1    

class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskSettingsInline, SubtaskInline]
    list_display = ('task_name', 'user', 'seq_file')

class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'seq_format', 'short_seq', 'seq_id', 'seq_name', 'seq_description', 'seq_letter_annotations', 'seq_annotations', 'seq_features', 'seq_dbxrefs')

class RawResultAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'short_result')

class InferredResultAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'probability', 'short_result')

admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask, SubtaskAdmin)
admin.site.register(RawResult, RawResultAdmin)
admin.site.register(InferredResult, InferredResultAdmin)

