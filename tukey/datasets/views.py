from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from .models import DataSet, Key, KeyValue
from .forms import UpdateDataSetForm, AddDataSetForm
from datetime import datetime, timedelta
import uuid

#This needs work -- a lot of assumptions, lack of error checking and general ugliness

osdc_prefix = 'osdc'

#does not support time zones -- for now leave it up to the submission scripts to put in UTC.
time_format='%Y-%m-%d %H:%M:%S'

valid_keys = ['source', 'source_url', 'description', 'short_description', 'category', 'size', 'modified', 'license', 'osdc_location', 'osdc_folder', 'osdc_hs_location', 'osdc_hs_folder']

def init_keys():
    for key in valid_keys:
        k = Key(key_name=key, public=True)
        k.save()

def add_dataset(title, prefix):
    key = str(uuid.uuid4())
    slug = slugify(title)

    d = DataSet(key=key, prefix=prefix, title=title, slug=slug)
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
            titles[kv.dataset.slug] = kv.dataset.title
            try:
                short_descripts[kv.dataset.slug] = KeyValue.objects.get(dataset=kv.dataset, key='short_description').value
            except KeyValue.DoesNotExist:
                short_descripts[kv.dataset.slug] = ''

            for category in KeyValue.objects.filter(dataset=kv.dataset, key='category'):
                if kv.dataset.slug not in categories:
                    categories[kv.dataset.slug] = []
                categories[kv.dataset.slug].append(category.value)

            try:
                modified_times[kv.dataset.slug] = datetime.strptime(KeyValue.objects.get(dataset=kv.dataset, key='modified').value, time_format)
            except KeyValue.DoesNotExist:
                modified_times[kv.dataset.slug] = ''
    else:
        datasets = DataSet.objects.all()

        #better way to do this? -- assuming one value for everything except categories
        #for title in KeyValue.objects.filter(key='title'):
        #    titles[title.dataset.ark_key] = title.value
        for dataset in datasets:
            titles[dataset.slug] = dataset.title

        for descript in KeyValue.objects.filter(key='short_description'):
            short_descripts[descript.dataset.slug] = descript.value

        for category in KeyValue.objects.filter(key='category'):
            if category.dataset.slug not in categories:
                categories[category.dataset.slug] = []
            categories[category.dataset.slug].append(category.value)
    
        for time in KeyValue.objects.filter(key='modified'):
            modified_times[time.dataset.slug] = datetime.strptime(time.value, time_format)
    
    return render_to_response('datasets/datasets_list_index.html', {'datasets' : datasets, 'titles' : titles, 'categories' : categories, 'short_descripts' : short_descripts, 'modified_times' : modified_times, 'category_filter' : category_filter}, context_instance=RequestContext(request))

def dataset_detail(request, dataset_id):
    d = get_object_or_404(DataSet, pk=dataset_id)
    dataset_dict = dict()
    dataset_dict['title'] = d.title
    #dataset_dict['title'] = KeyValue.objects.get(dataset=d, key='title').value
    #only special case is category
    for key in Key.objects.all():
        key_name = key.key_name
        value_list = KeyValue.objects.filter(dataset=d, key=key_name).values_list('value',flat=True).order_by('value')
        if key_name == 'category':
            dataset_dict[key_name] = value_list
        else:
            #probably more than 1 is an error/warning, just returning the first found
            if len(value_list) > 0:
                if key_name == 'modified':
                    dataset_dict[key_name] = datetime.strptime(value_list[0], time_format)
                else:
                    dataset_dict[key_name] = value_list[0]
            else:
                dataset_dict[key_name] = ''

    print('dataset_dict: ' + str(dataset_dict))
    return render_to_response('datasets/dataset_detail.html', {'dataset': dataset_dict}, context_instance=RequestContext(request))
