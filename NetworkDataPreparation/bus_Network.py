

from os.path import expanduser
import numpy as np
import cPickle as pickle
from operator import itemgetter
import re
import math
import matplotlib.pylab as plt


def get_list_of_stop_times(window):
    '''Associated with each trip_ID get the
     ordered list of stop_IDs and the corresponding
      scheduled arrival/departure times from MBTA_GTFS/stop_times.txt file. '''
    

    file_ = open(expanduser('stop_times.txt'), 'rb')
    
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
    file_ = open(expanduser('stop_times.txt'), 'rb')
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
    
    #save the sequence sorted dict into a file
    save_in_file_ = open(expanduser('trips_dict.pkl'), 'wb')
    pickle.dump(sorted_trip_dict, save_in_file_)
    file_.close()
    
    
def get_network_dict():
    '''saves a dict where keys are pairs of stops and values are list of time tuples
    [(t_d_1,t_transfer_1),(t_d_2,t_transfer_2),...]'''
        
    dict_file_ = open(expanduser('trips_dict.pkl'), 'rb')
    trip_dict = pickle.load(dict_file_)
    dict_file_.close()
    

    network_dict = {}
    stop_list = []
    # for all trip_IDs we get a list of (arrival_time, departure_time,stop_ID, sequence_num)
    for key in trip_dict.keys():
        #load the list of (arrival_time, departure_time,stop_ID, sequence_num)
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
            #arrival time for stop2
            t2_list = temp_list[1][0].split(':')
            print 't2_list',t2_list
            t2 = int(t2_list[0][1:]) * 3600 + int(t2_list[1]) * 60 + int(t2_list[2][:-1])
            # departure time for stop1
            t1_list = temp_list[0][1].split(':')
            print 't1_list',t1_list
            t1 = int(t1_list[0][1:]) * 3600 + int(t1_list[1]) * 60 + int(t1_list[2][:-1])
            # transfer_time is the arrival_time to stop2 - departure_time from stop1
            transfer_time = t2 - t1
            departure_time = t1
            network_dict[(stop_1,stop_2)].append((departure_time,transfer_time))
        elif len(temp_list)>2:
            for ind,item in enumerate(temp_list[:-1]):
                stop_1 = item[2]
                stop_2 = temp_list[ind+1][2]
                # arrival time
                t2_list = temp_list[ind+1][0].split(':')
#                 print 't2_list',t2_list
                t2 = int(t2_list[0][1:]) * 3600 + int(t2_list[1]) * 60 + int(t2_list[2][:-1])
                # departure time
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
    
    
    #dumping the network dict into a file
    dict_file_ = open(expanduser('stop_networks.pkl'), 'wb')
    pickle.dump(network_dict,dict_file_)
    dict_file_.close()
    
    return stop_list


def time_sort_stop_network_dict():
    '''Sorting the list associated with each edge in the stop network based on the t_start '''
    _file = open(expanduser('stop_networks.pkl'), 'rb')
    network_dict = pickle.load(_file) 
    _file.close()
    
    print len(network_dict.keys())
    time_sorted_network_dict = {}
    for key in network_dict.keys():
        time_sorted_network_dict[key] = sorted(network_dict[key],key=itemgetter(0))
    
    _file = open(expanduser('time_sorted_stop_networks.pkl'), 'wb')
    pickle.dump(time_sorted_network_dict,_file) 
    _file.close()
    

def generate_average_and_sigma_transfer_time_networks(time_sorted_network_dict, trials = 100, window_length = 2):
    
    folder_address_temp = expanduser('myData/transfer_time_networks/')
        
    #generating a network for each two hour
    for h in range(0,24,window_length):
        print h
        s_cursor_start = 3600*h
        s_cursor_end = 3600*(h+window_length)
        #a num_edges-by-num_trials array
        time_array = np.random.randint(s_cursor_start,s_cursor_end,(len(time_sorted_network_dict.keys()),trials))
        
        # we genearte a network for each time window,
        # stops are nodes and edges are time tuple 
        #(t_transfer_average, t_transfer_sigma)
        transfer_time_network = {}
        
        for i,key in enumerate(time_sorted_network_dict.keys()):
            # get the list of time tuples (t_departure, t_transit) for each pair of stops
            time_tuple_list = time_sorted_network_dict[key]
#             print time_sorted_network_dict[key]
            # for each trial, get the time when the trip starts
            # which becomes a list for all trials where the i-the 
            #item is the i-th trial time
            trip_begins_times = time_array[i,:]
            
            # get the wait-time for each trial which should be added to the transfer time
            wait_time_list = []
            transit_times_list = []
            for begining_time in trip_begins_times:
                bus_depart_times = np.array([time_tuple[0] for time_tuple in time_tuple_list])
                bus_transit_times = np.array([time_tuple[1] for time_tuple in time_tuple_list])
#                 print bus_transit_times
                # list of all departure times which happen before the cursur_end
                bus_departs_temp = bus_depart_times[bus_depart_times<s_cursor_end]
                
                # if the list is not empty
                if len(bus_departs_temp) >0:
                    last_departure = np.max(bus_departs_temp)
                else:
                    continue
                
                if begining_time<last_departure:
                # get the list of feasible departure times
                    future_buses_ind_list = [item for item in range(len(bus_depart_times)) if (bus_depart_times[item]>=begining_time and bus_depart_times[item]<s_cursor_end)]
                    all_future_departure_times = bus_depart_times[future_buses_ind_list]
                    all_future_transit_times = bus_transit_times[future_buses_ind_list]
                    wait_time_temp = np.min(all_future_departure_times) - begining_time
                    wait_time_list.append(wait_time_temp)
                    transit_times_list.append(np.average(all_future_transit_times))
                else:
                    continue
                    
            average_wait_time = np.mean(np.array(wait_time_list))
            wait_time_sigma = np.std(wait_time_list)
            average_transit_time = np.average(transit_times_list)
            transfer_time_network[key] = (average_wait_time,wait_time_sigma, average_transit_time)
#             print key, transfer_time_network[key]
        print 'saving the network'
        _file = open(folder_address_temp + 'transfer_times_network_' + str(h) , 'wb')
        pickle.dump(transfer_time_network,_file)
        _file.close()
        
def generate_final_networks(window_length = 2):
    
    folder_address_temp = expanduser('myData/transfer_time_networks/')
    
    for h in range(0,24,window_length):
       _file = open(folder_address_temp + 'transfer_times_network_' + str(h) , 'rb')
       network_dict = pickle.load(_file)
       _file.close()
       stop_list = list(set([stop_ID[0] for stop_ID in network_dict.keys()]))
       #a network where the values are just the transit times
       new_transit_time_network = {}
       #a network where the values are list of wait-times for each stop and keys are stop_IDS
       wait_time_network = {stop_id:[] for stop_id in stop_list}
       
       for key in network_dict.keys():
           print network_dict[key]
           new_transit_time_network[key] = network_dict[key][2]
           wait_time_network[key[0]].append(network_dict[key][0])
       
       average_wait_time_network = {stop_id:np.average(wait_time_network[stop_id]) for stop_id in stop_list}
       _file = open(folder_address_temp + 'transit_times_network_' + str(h) , 'wb')
       pickle.dump(new_transit_time_network,_file)
       _file.close()
       
       _file = open(folder_address_temp + 'wait_times_at_stops_' + str(h) , 'wb')
       pickle.dump(average_wait_time_network,_file)
       _file.close()

if __name__ == '__main__':
#     get_list_of_stop_times(100000)
#     stop_list_1 = get_network_dict()
#     stop_list_2 = open_hongmou_stop_list()
#     time_sort_stop_network_dict()
    
    #laoding the network
#     time_sorted_network_dict = load_time_sorted_tuple_list_network()
#     generate_average_and_sigma_transfer_time_networks(time_sorted_network_dict)
#     generate_final_networks()
#     generate_final_networks()
#     Generate_single_networks()
#     load_transit_times()
    
    
    
    
    
    
