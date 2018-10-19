import data_functions as df
import time

active = 1
errcode = 0
time_polled = []

while active:
    archive_data = {}
    compare_data = {}
    time.sleep(2)
    
    settings = df.get_settings()

    compare_data = df.load_compare(settings)                                # Pull the previously polled data
    item_data, errcode = df.get_data()                                                   # Pull potentially new data
    
    if errcode > 0:
        print(errcode)
        continue
    
    if item_data == compare_data:                                               # If the json has not changed

        continue                                                                # Exit the loop
    else:
        archive_data = df.data_update(settings, item_data)         # Update each item JSON with the new Data
        df.save_json(settings['file dir']+'previous_data.json', item_data)  # can probably be moved to the data for loop
        print('done')