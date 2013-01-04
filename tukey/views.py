from django.template.response import TemplateResponse
from django.shortcuts import render


from .forms import RegisterIdForm

def register_user(request, user=None, template_name='osdc/register.html'):
    if user is None:
	user = request.user

    form = RegisterIdForm()

    return render(request, template_name, 
	{
	    'form': form,
	    'method': user.method, 
	    'identifier': user.identifier
	})
