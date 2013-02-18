from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def index(request):
    # for testing
    return render(request, 'discovery/discovery.html')

def discoFeed(request):
    return HttpResponseRedirect('/demo/shibboleth-ds/disco.json')
    #return HttpResponse(disco, mimetype='application/json')


def config(request):
    return render(request,'discovery/idpselect_config.js') 
    #return HttpResponseRedirect('/demo/shibboleth-ds/idpselect_config.js')
    #return render(request, '/etc/shibboleth-ds/idpselect_config.js')

def idpselect(request):
    return HttpResponseRedirect('/demo/shibboleth-ds/idpselect.js')
#    return render_shib_ds(request, '/etc/shibboleth-ds/idpselect.js')
