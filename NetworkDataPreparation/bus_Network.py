'''
Created on Mar 23, 2015

@author: mmvazifeh
'''
from os.path import expanduser
import numpy as np
import cPickle as pickle
from operator import itemgetter
import re
def get_list_of_stop_times(window):
    '''Associated with each trip_ID get the
     ordered list of stop_IDs and the corresponding
      scheduled arrival/departure times from 
~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/stop_times.txt file. '''
    

    file_ = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/stop_times.txt'), 'rb')
    
    # trip_dict has trip_ids as keys and list of tuples as values 
    #where each tuple is associated with one stop_ID and it shows the sequence 
    #associated with that stop id on the trip and arrival/departure time
    #the tuples are sorted based on arrival time (arrival_time, departure_time,stop_ID, sequence_num)
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
#             print (temp_list[1],temp_list[2],temp_list[3],int(temp_list[4]))
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
    
def get_network_dict():
    '''saves a dict where keys are pairs of stops and values are list of time tuples
    [(t_d_1,t_transfer_1),(t_d_2,t_transfer_2),...]'''
        
    dict_file_ = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/trips_dict.pkl'), 'rb')
    trip_dict = pickle.load(dict_file_)
    print len(trip_dict.keys())
    print len(set(trip_dict.keys()))
    
    network_dict = {}
    stop_list = []
    for key in trip_dict.keys():
        temp_list = trip_dict[key]
        if len(temp_list) == 2:
            stop_1 = temp_list[0][2]
            stop_2 = temp_list[1][2]
            stop_list.append(stop_1)
            stop_list.append(stop_2)
#             print stop_1,stop_2
            network_dict[(stop_1,stop_2)] = []
        elif len(temp_list)>2:
            for ind,item in enumerate(temp_list[:-1]):
                stop_1 = item[2]
                stop_2 = temp_list[ind+1][2]
                stop_list.append(stop_1)
                stop_list.append(stop_2)
                network_dict[(stop_1,stop_2)] = []
#                 print stop_1,stop_2
    
    print len(stop_list)
    print len(set(stop_list))
                
    dict_file_.close()
    return stop_list
    
def open_hongmou_stop_list():
    
    stops_lat_lon_file = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/Hongmou_stop_info/StopCoords.csv'), 'rb')
    stops_lat_lon_file.readline()
    lines = stops_lat_lon_file.readlines()
    stop_list = []
    for line in lines:
        temp_list = line.split(',')
        print temp_list
        
        stop_list.append(temp_list[2])
    
    print len(stop_list)
    print len(set(stop_list))

    
    stops_lat_lon_file.close()
    return stop_list
        
    
if __name__ == '__main__':
#     get_list_of_stop_times(100000)
    stop_list_1 = get_network_dict()
    stop_list_2 = open_hongmou_stop_list()
    stop_list_A = []
    stop_list_B = []
    for item in stop_list_1:
        temp = re.findall(r'\d+',item)
        if len(temp)==1:
#             print temp[0]
            stop_list_A.append(int(temp[0]))
        else:
#             print item,'A'
            pass
    
    print len(set(stop_list_A))        
    for item in stop_list_2:
        temp = re.findall(r'\d+',item)
        if len(temp)==1:
            stop_list_B.append(int(temp[0]))
        else:
            print item, 'B'
             
    print len(set(stop_list_A) - set(stop_list_B))
    print set(stop_list_B) - set(stop_list_A)
    print set(stop_list_B) - set(stop_list_A)
#     
#     
    
    
    