from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from .models import DataSet, Key, KeyValue
from .forms import UpdateDataSetForm, AddDataSetForm
from datetime import datetime, timedelta

#This needs work -- a lot of assumptions, lack of error checking and general ugliness

initial_key = 1000
osdc_prefix = 'osdc'

#does not support time zones -- for now leave it up to the submission scripts to put in UTC.
time_format='%Y-%m-%d %H:%M:%S'

def add_dataset(prefix):
    dataset_list = DataSet.objects.all().order_by('-num')
    #might want to cache last_key in the future -- won't have to do the db query
    if len(dataset_list) == 0:
        new_key = initial_key
    else:
        new_key = dataset_list[0].num + 1
        
    ark_key = prefix + str(new_key)
    d = DataSet(ark_key=ark_key, prefix=prefix, num=new_key)
    d.save()
    return d


def add_keyvalue(d, key_name_str, v):
    k = Key.objects.get(key_name=key_name_str)
    #should some validation be done? -- just going to check for modified so that store it in time_format
    if type(v) is datetime:
        v = v.strftime(time_format)

    key_value = KeyValue(dataset=d, key=k, value=v)
    key_value.save()

#expects ids and values
#again, probably can be done better, need to filter updated fields on the form level somehow?
def update_keyvalues(keyvalues_id_value):
    for (key_id, value) in keyvalues_id_value:
        k = KeyValue.objects.get(id=key_id)
        if type(value) is datetime:
            value = value.strftime(time_format)

        if value != k.value:
            k.value = value
            k.save()


def datasets_list_index(request, category_filter=None):
    titles = dict()
    short_descripts = dict()
    categories = dict()
    modified_times = dict()

    datasets = []

    #this is terrible, executing a query for each key/value, needs to be fixed
    if category_filter is not None:
        kvs = KeyValue.objects.filter(key='category', value=category_filter)
        for kv in kvs:
            datasets.append(kv.dataset)
            titles[kv.dataset.ark_key] = KeyValue.objects.get(dataset=kv.dataset, key='title').value
            short_descripts[kv.dataset.ark_key] = KeyValue.objects.get(dataset=kv.dataset, key='short_description').value
            for category in KeyValue.objects.filter(dataset=kv.dataset, key='category'):
                if kv.dataset.ark_key not in categories:
                    categories[kv.dataset.ark_key] = []
                categories[kv.dataset.ark_key].append(category.value)

            modified_times[kv.dataset.ark_key] = datetime.strptime(KeyValue.objects.get(dataset=kv.dataset, key='modified').value, time_format)
    else:
        datasets = DataSet.objects.all()

        #better way to do this? -- assuming one value for everything except categories
        for title in KeyValue.objects.filter(key='title'):
            titles[title.dataset.ark_key] = title.value

        for descript in KeyValue.objects.filter(key='short_description'):
            short_descripts[descript.dataset.ark_key] = descript.value

        for category in KeyValue.objects.filter(key='category'):
            if category.dataset.ark_key not in categories:
                categories[category.dataset.ark_key] = []
            categories[category.dataset.ark_key].append(category.value)
    
        for time in KeyValue.objects.filter(key='modified'):
            modified_times[time.dataset.ark_key] = datetime.strptime(time.value, time_format)
    
    return render_to_response('datasets/datasets_list_index.html', {'datasets' : datasets, 'titles' : titles, 'categories' : categories, 'short_descripts' : short_descripts, 'modified_times' : modified_times, 'category_filter' : category_filter}, context_instance=RequestContext(request))

def dataset_detail(request, dataset_id):
    d = get_object_or_404(DataSet, pk=dataset_id)
    dataset_dict = dict()
    dataset_dict['title'] = KeyValue.objects.get(dataset=d, key='title').value
    dataset_dict['source'] = KeyValue.objects.get(dataset=d, key='source').value
    dataset_dict['source_url'] = KeyValue.objects.get(dataset=d, key='source_url').value
    dataset_dict['description'] = KeyValue.objects.get(dataset=d, key='description').value
    categories = KeyValue.objects.filter(dataset=d, key='category').order_by('value')
    dataset_dict['categories'] = []
    for category in categories:
    	dataset_dict['categories'].append(category.value)
    dataset_dict['size'] = KeyValue.objects.get(dataset=d, key='size').value
    dataset_dict['osdc_location'] = KeyValue.objects.get(dataset=d, key='osdc_location').value
    dataset_dict['osdc_folder'] = KeyValue.objects.get(dataset=d, key='osdc_folder').value
    dataset_dict['osdc_hs_location'] = KeyValue.objects.get(dataset=d, key='osdc_hs_location').value
    dataset_dict['osdc_hs_folder'] = KeyValue.objects.get(dataset=d, key='osdc_hs_folder').value

    return render_to_response('datasets/dataset_detail.html', {'dataset': dataset_dict}, context_instance=RequestContext(request))

def datasets_admin(request):
    titles = dict()
    #need to add a dataset permissions to check separated from just any authenticated user.
    if request.user.is_authenticated():
        datasets = DataSet.objects.all()
        for title in KeyValue.objects.filter(key='title'):
            titles[title.dataset.ark_key] = title.value
        return render_to_response('datasets/datasets_list_admin.html', {'datasets' : datasets, 'titles' : titles}, context_instance=RequestContext(request))
    else:
        return HttpResponse("Should redirect to login")

def datasets_admin_update(request, dataset_id):
    if request.user.is_authenticated():
        extra_questions = ['What is the velocity of a swallow?', 'African or European?']
        d = get_object_or_404(DataSet, pk=dataset_id)
        kvs = KeyValue.objects.filter(dataset=d).order_by('id')
        form = UpdateDataSetForm(request.POST or None, keyvalues=kvs)
        try:
            title_kv = kvs.get(key='title')
            title = title_kv.value
        except:
            title = None

        ark_key = d.ark_key
        if form.is_valid():
            update_keyvalues(form.keyvalues_id_value())
            return redirect("datasets:datasets_admin_index")
    
        return render_to_response("datasets/datasets_update.html", {'form': form, 'title' : title,  'ark_key' : ark_key}, context_instance=RequestContext(request))
    else:
        #should be the login page
        return redirect("datasets:datasets_list_index")

def datasets_admin_add(request):
    if request.user.is_authenticated():
        k = Key.objects.all()
        form = AddDataSetForm(request.POST or None, keys=k)
        if form.is_valid():
            d = add_dataset(osdc_prefix)
            for name, value in form.cleaned_data.items():
                add_keyvalue(d, name, value)
                print('submitted: ' + str(name) + ' ' + str(value))
            return redirect("datasets:datasets_admin_index")

        return render_to_response("datasets/datasets_add.html", {'form': form}, context_instance=RequestContext(request))
    else:
        #should be the login page
        return redirect("datasets:datasets_list_index")

#just for my convience for now, super unsafe deletes the dataset and all of the keyvalues associated with it, when this is for real don't want to delete for real, but perhaps mark as deactivated?
def datasets_admin_delete(request, dataset_id):
    if request.user.is_authenticated():
        d = get_object_or_404(DataSet, pk=dataset_id)
        d.delete()
        return redirect("datasets:datasets_admin_index")

    else:
        #should be the login page
        return redirect("datasets:datasets_list_index")

def datasets_admin_add_kv(request, dataset_id):
    if request.user.is_authenticated():
        return redirect("datasets:datasets_admin_index")

    else:
        #should be the login page
        return redirect("datasets:datasets_list_index")


      
