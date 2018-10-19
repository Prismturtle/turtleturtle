import requests
import json
import time
import os

from time import gmtime, asctime
from operator import itemgetter
    
def get_settings():
    """ Loads user settings """
    settings_file = 'settings.json'

    try:
        with open(settings_file,"r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        t = time.gmtime()
        settings = {'file dir':'data\\', 'id':[]}
        
    return settings

def load_compare(settings):
    """ Loads the comparison JSON file"""
    
    compare_file = (settings['file dir'] + 'previous_data.json')

    try:
        with open(compare_file,"r") as f:
            compare_data = json.load(f)
    except FileNotFoundError:
        compare_data = {'1':1}
        
    return compare_data

def load_archive(data_file):
    """ Loads the archive JSON files"""
    
    try:
        with open(data_file,"r") as f:
            archive_data = json.load(f)
    except FileNotFoundError:
        archive_data = {}
        
    return archive_data

def get_data():
    url = 'https://rsbuddy.com/exchange/summary.json'
    errcode = 0
    try:
        r = requests.get(url)
        item_data = r.json()
    except ConnectionError:
        errcode = 1
        item_data = {'1':1}
        
    return item_data, errcode

def data_update(settings, item_data):
    asc_time = time.asctime(gmtime())
    epoch_time = round(time.time() - 1514764800)
    
    
    id_list = list(settings['id'])
    current_date = [time.gmtime()[0],time.gmtime()[1]]
    
    for key in item_data.keys():
        archive_file, archive_loc = get_file_name(settings, current_date, key)  # Returns the active file
        make_dir(archive_loc)         
        file_loc = archive_loc + archive_file                                   # Create the directory
        archive_data = load_archive(file_loc)                                   # Load the active keys data
        
        if key in id_list:
            archive_data = append_data(archive_data, item_data[key])            # Append new data to the existing dictionary
        else:
            archive_data = new_data(item_data[key])                             # Start a new sub-dictionary with proper format
            id_list.append(key)
                
        # pop the key just read, check to see if any keys remain after a pull       
                
        archive_data['time'].append(asc_time)                                   # Append a readable date
        archive_data['epoch'].append(epoch_time)                                # Epoch time starts in 2013
        save_json(file_loc, archive_data, "w+")
        
    if id_list != settings['id']:
        settings['id'] = id_list
        save_json('settings.json', settings, "w+")
        
    return

def get_file_name(settings, year_month, key):
    
    archive_loc = settings['file dir']+key+'\\'   
    archive_file = str(year_month[0])+'_'+str(year_month[1])+'_'+key+'.json'
    
    return archive_file, archive_loc

def make_dir(directory_path):
    try:  
        os.makedirs(directory_path)
    except FileExistsError:
        pass
    return

def append_data(active_data, new_data):
    """ Appends new data to existing database items """
    
    single_entry = ["id", "name", "members", "sp" ]
    listed_entry = ["buy_average", "buy_quantity", "sell_average", 
                "sell_quantity", "overall_average", "overall_quantity"]
    
    for key in new_data.keys():
        if key in single_entry:
            # If the key should be a description, or singular value
            if active_data[key][-1] == new_data[key]:
                continue
            else:
                # Append the new data incase it has changed
                active_data[key].append(new_data[key])
                
        elif key in listed_entry:
            # If the key should be a data value
            active_data[key].append(new_data[key])
            
        else:
            # If an unexpected value is found
            data = {"misc":{key:[new_data[key]]}}
            active_data[key].update(data)
            
    return active_data

def new_data(new_data):
    """ Adds and formats new entries to the database """
    
    active_data = {}
    standard_entry = ["id", "name", "members", "sp", 
                      "buy_average", "buy_quantity", "sell_average", 
                      "sell_quantity", "overall_average", "overall_quantity"]
    
    for key in new_data.keys():
        if key in standard_entry:
            data = {key:[new_data[key]]}
            active_data.update(data)
        else:
            data = {"misc":{key:[new_data[key]]}}
            active_data.update(data)
            
    time_keys = {'time':[],'epoch':[]}
    active_data.update(time_keys)
    
    return active_data

def save_json(file_name, file_data, rw="w+"):
    """ Saves the updated file """
    
    with open(file_name, rw) as f:
        json.dump(file_data, f)
    return








def get_sleep(tp):
    if len(tp) < 3:
        sleep_time = 240
    else:
        sleep_time = (tp[2] - tp[1] + tp[1] - tp[0]) / 2
        
    tp.append(time.time() - 1356998400)
    
    return sleep_time, tp
    