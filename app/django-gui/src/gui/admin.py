from gui.models import Task, Subtask, RawResult, InferredResult
from django.contrib import admin

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(RawResult)
admin.site.register(InferredResult)
