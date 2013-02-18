from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CGQueryForm

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CGQueryForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            ignore = ['csrfmiddlewaretoken']
            rest_url = "https://cghub.ucsc.edu/cghub/metadata/analysisObject?"
            q_str = ''
            for attr in request.POST:
                if attr not in ignore and request.POST[attr] != '' :
                    q_str += "&" + attr + "=" + request.POST[attr]
        
            return HttpResponseRedirect(rest_url + q_str[1:])
            
    else:
        form = CGQueryForm()

    return render(request, 'cgquery/form.html', {
        'form': form,
    })


#def query(request):
#    #return HttpResponse(request.POST['choice'])
#
#    q_str = ''
#    for attr in request.POST:
#        q_str += attr + ":" + request.POST[attr]
#
#    #return HttpResponse(q_str)
#    return HttpResponse("The post : " +str(request.POST))
