import os
from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def include_task_list():
    url = getattr(settings, 'MEDIA_URL')
    if hasattr(settings, 'STATIC_URL'):
        url = getattr(settings, 'STATIC_URL')

    return "<script type='text/javascript' src='%s'></script>" % os.path.join(url, 'taskList.js')
    
@register.simple_tag
def include_custom_styles():
    url = getattr(settings, 'MEDIA_URL')
    if hasattr(settings, 'STATIC_URL'):
        url = getattr(settings, 'STATIC_URL')

    return "<link rel='stylesheet' href='%s' type='text/css' media='all' />" % os.path.join(url, 'blastula-custom.css')    
