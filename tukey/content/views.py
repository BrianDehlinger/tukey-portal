from tukey.content.models import Page
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
import re, os

def page(request, slug=''):
    #slug can either be blank or contain \w and -, safe because from urls.py regex
    p = get_object_or_404(Page, pk=slug)
    nav_pages = Page.objects.order_by('nav_order')
    template = os.path.abspath(os.path.join(settings.ROOT_PATH, '..', 'tukey/templates/page.html'))

    return render_to_response('content/page.html', {'content' : p, 'nav_pages' : nav_pages}, context_instance=RequestContext(request))