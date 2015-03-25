'''
Created on Mar 25, 2015

@author: Hongmou
@summary: This py gets the scheduled travel time from the pkl file the Mohammad made
'''

import cPickle as pickle

# Scheduled time for several buses
file_  = open('C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/Processed_data_mohammad/transfer_times_network.pkl', 'rb')
network_dictionary = pickle.load(file_)
file_.close()

splitStops = 'C:/users/hongmou/desktop/BUS_SPLIT_STOPS.csv'