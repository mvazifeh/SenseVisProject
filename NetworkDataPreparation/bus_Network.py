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
    dict_file_.close()
    
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
            network_dict[(stop_1,stop_2)] = []
        elif len(temp_list)>2:
            for ind,item in enumerate(temp_list[:-1]):
                stop_1 = item[2]
                stop_2 = temp_list[ind+1][2]
                stop_list.append(stop_1)
                stop_list.append(stop_2)
                network_dict[(stop_1,stop_2)] = []
        else: 
            print 'hmmm!'
            
    for key in trip_dict.keys():
        temp_list = trip_dict[key]
        if len(temp_list) == 2:
            stop_1 = temp_list[0][2]
            stop_2 = temp_list[1][2]
            t2_list = temp_list[1][0].split(':')
#             print 't2_list',t2_list
            t2 = int(t2_list[0][1:]) * 3600 + int(t2_list[1]) * 60 + int(t2_list[2][:-1])
            t1_list = temp_list[0][1].split(':')
#             print 't1_list',t1_list
            t1 = int(t1_list[0][1:]) * 3600 + int(t1_list[1]) * 60 + int(t1_list[2][:-1])
            transfer_time = t2 - t1
            departure_time = t1
            network_dict[(stop_1,stop_2)].append((departure_time,transfer_time))
        elif len(temp_list)>2:
            for ind,item in enumerate(temp_list[:-1]):
                stop_1 = item[2]
                stop_2 = temp_list[ind+1][2]
                t2_list = temp_list[ind+1][0].split(':')
#                 print 't2_list',t2_list
                t2 = int(t2_list[0][1:]) * 3600 + int(t2_list[1]) * 60 + int(t2_list[2][:-1])
                t1_list = item[1].split(':')
#                 print 't1_list',t1_list
                t1 = int(t1_list[0][1:]) * 3600 + int(t1_list[1]) * 60 + int(t1_list[2][:-1])
                transfer_time = t2 - t1
                departure_time = t1
                if (temp_list[ind+1][3] - item[3]) != 1:
                    print 'Error the sequences are', temp_list[ind+1][3],item[3]
                network_dict[(stop_1,stop_2)].append((departure_time,transfer_time))
        else: 
            print 'hmmm!'
    
    
    
    dict_file_ = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/stop_networks.pkl'), 'wb')
    pickle.dump(network_dict,dict_file_)
    dict_file_.close()
    
    
    return stop_list
    
def open_hongmou_stop_list():
    
    stops_lat_lon_file = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/Hongmou_stop_info/StopCoords.csv'), 'rb')
    stops_lat_lon_file.readline()
    lines = stops_lat_lon_file.readlines()
    stop_list = []
    for line in lines:
        temp_list = line.split(',')
        
        stop_list.append(temp_list[2])
    

    
    stops_lat_lon_file.close()
    return stop_list

def load_stop_network_dict():
    
    _file = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/stop_networks.pkl'), 'rb')
    network_dict = pickle.load(_file) 
    _file.close()
    
    print len(network_dict.keys())
    time_sorted_network_dict = {}
    for key in network_dict.keys():
        time_sorted_network_dict[key] = sorted(network_dict[key],key=itemgetter(0))
    
    _file = open(expanduser('~/Dropbox/SCL-MIT-Research/SCL-Projects/hackathon/MBTAHubHacksData/myData/time_sorted_stop_networks.pkl'), 'wb')
    pickle.dump(time_sorted_network_dict,_file) 
    _file.close()

def generate_average_and_sigma_transfer_time_networks(time_sorted_network_dict, trials = 10):
    
    for h in range(0,24,2):
        s_cursor_start = 3600*h
        s_cursor_end = 3600*(h+1)
    
        t_array = random.randint(s_cursor_start,s_cursor_end,(len(time_sorted_network_dict.keys()),trials))
        
        

if __name__ == '__main__':
#     get_list_of_stop_times(100000)
#     stop_list_1 = get_network_dict()
#     stop_list_2 = open_hongmou_stop_list()
    
    load_stop_network_dict()
    
    