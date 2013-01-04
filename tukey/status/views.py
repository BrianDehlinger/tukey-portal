# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib2, json



def get_percent(used, total):
    if float(total) == 0:
        return 0
    else:
        return float(used)/float(total)

def append_status(data, cloud_status_data, currcloud, label, idprefix, value_name):
    cloud_status_data.append( (label, idprefix + '-' + value_name, data[currcloud][value_name]['val'], data[currcloud][value_name]['max'], get_percent(data[currcloud][value_name]['val'], data[currcloud][value_name]['max']) ) )

def status_public(request):
    status_req = urllib2.Request('http://dashboard.opensciencedatacloud.org/state.json')
    opener = urllib2.build_opener()
    data = json.loads(str(opener.open(status_req).read()), 'utf-8')
    
    cloud_names = ['Adler', 'Sullivan', 'OCC-Y', 'OCC-Root']

    update_times = {}
    status_data = {}

    #There's gotta be a better way to do this -- probably fix the json... ok this is slightly better for now.
    for cloud_name in cloud_names:
        status_data[cloud_name] = []
        standard = False
        
        if(cloud_name == 'Adler'):
            currcloud = 'OSDC Cloud2'
            idprefix = 'adler'
            standard = True
        elif(cloud_name == 'Sullivan'):
            currcloud = 'OSDC-Sullivan'
            idprefix = 'sullivan'
            standard = True
        elif(cloud_name == 'OCC-Y'):
            currcloud = 'OCC-Y'
            idprefix = 'occ-y'
            standard = False
        elif(cloud_name =='OCC-LVOC'):
            currcloud = 'OCC-LVOC-HADOOP'
            idprefix = 'occ-lvoc'
            standard = False
        elif(cloud_name == 'OCC-Root'):
            continue

        if currcloud in data:    
            if standard:
                append_status(data, status_data[cloud_name], currcloud, 'Storage Used (GB): ', idprefix, 'cluster')
                append_status(data, status_data[cloud_name], currcloud, 'Active Users: ', idprefix, 'users')
                append_status(data, status_data[cloud_name], currcloud, 'VM Instances: ', idprefix, 'vms')
                append_status(data, status_data[cloud_name], currcloud, 'VM Cores: ', idprefix, 'cores')
                append_status(data, status_data[cloud_name], currcloud, 'VM RAM (GB): ', idprefix, 'ram')
                append_status(data, status_data[cloud_name], currcloud, 'VM Instance Storage (GB): ', idprefix, 'ldisk')
            else:
                append_status(data, status_data[cloud_name], currcloud, 'HDFS Storage (GB): ', idprefix, 'hdfsdu')
                append_status(data, status_data[cloud_name], currcloud, 'Active Jobs: ', idprefix, 'jobs')
                append_status(data, status_data[cloud_name], currcloud, 'Active Users: ', idprefix, 'users')
            
            
            update_times[cloud_name] = data[currcloud]['users']['stsh']
        else:
            update_times[cloud_name] = "None"

    #special for root here        
    storage_names = ['OCC-Root']

    old_ncbi_total = 333832
    old_ncbi_max = 333832

    storage_total = old_ncbi_total
    max_storage = 0.0
    storage_percent = 0
    status_time = ""
    for storage_name in storage_names:
        if storage_name in data:
            idprefix = 'occ-root'
            value_name = 'disk'
            status_data[storage_name] = []
            for data_set_name in data[storage_name]:
                val = float(data[storage_name][data_set_name]['val'])
                storage_total = storage_total + val
                max_storage = float(data[storage_name][data_set_name]['max'])
                status_time = data[storage_name][data_set_name]['stsh']

            max_storage = max_storage / 1024
            max_storage = max_storage + old_ncbi_max
            if max_storage != 0:
                storage_percent = storage_total / max_storage

            status_data[storage_name].append( ('Storage Used (GB): ', idprefix + '-' + value_name, storage_total, max_storage, storage_percent) )
            update_times[storage_name] = status_time
            print('storage_total: ' + str(storage_total) + ' max_storage: ' + str(max_storage))
        else:
            update_times[storage_name] = "None"

    print(status_data)

    return render_to_response('status/status_public.html', {'status_data' : status_data, 'cloud_names' : cloud_names, 'update_times' : update_times}, context_instance=RequestContext(request))
