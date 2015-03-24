'''
Created on Mar 23, 2015

@author: mmvazifeh
'''
from os.path import expanduser
import numpy as np
import cPickle as pickle
from operator import itemgetter

def get_list_of_stop_times(window):
    '''Associated with each trip_ID get the
     ordered list of stop_IDs and the corresponding
      scheduled arrival/departure times from 
~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/stop_times.txt file. '''
    

    file_ = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/stop_times.txt'), 'rb')
    
    # trip_dict has trip_ids as keys and list of tuples as values 
    #where each tuple is associated with one stop_ID and it shows the sequence 
    #associated with that stop id on the trip and arrival/departure time
    #the tuples are sorted based on arrival time
    trip_dict = {}
    for i in range(3000):
        lines = file_.readlines(window)
        for line in lines:
            temp_list = line.split(',')
            trip_ID = temp_list[0]
            trip_dict[trip_ID] = []
    file_.close()
    file_ = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/stop_times.txt'), 'rb')
    file_.readline()
    for i in range(3000):
        lines = file_.readlines(window)
        for line in lines:
            temp_list = line.split(',')
            trip_ID = temp_list[0]
#             print temp_list[4]
            trip_dict[trip_ID].append((temp_list[1],temp_list[2],temp_list[3],int(temp_list[4])))
             
        if len(lines) == 0:
            break
    print 'start sorting...'
    #sorting the tuples for each trip_ID according to the trip sequences
    sorted_trip_dict = {}
    for key in trip_dict.keys():
        sorted_trip_dict[key] = sorted(trip_dict[key],key=itemgetter(3))
    
    save_in_file_ = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/trips_dict.pkl'), 'wb')
    
    pickle.dump(sorted_trip_dict, save_in_file_)
                 
    file_.close()
    
    
    
    
if __name__ == '__main__':
    get_list_of_stop_times(100000)