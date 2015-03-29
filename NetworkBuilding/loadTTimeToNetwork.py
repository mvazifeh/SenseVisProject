'''
Created on Mar 29, 2015

@author: Hongmou
'''

import cPickle


ttime = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/Processed_data_mohammad/transit_times_network_24_2'
f = open(ttime, 'rb')
nd = cPickle.load(f) # travel time dictionary
f.close()

bus_segment = ''