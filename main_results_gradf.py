#!/usr/bin/python
import tools_deltaf as tools
import os, glob
file_log = raw_input(' Filename of the g09 output (including log) \n, remember, should be a single point TDDFT calculation \n')
incr = float(raw_input('value of chosen increment for f gradient calculation: \n'))
#### States of interest ######
input_states = raw_input(' Calculate gradient of states, separated by a SPACE (i.e. 4 5 6 12) \n ')
input_list = input_states.split()
states = map(int,input_list)

list_gradf = tools.gradient_f(incr)
tools.states_gradf(file_log,list_gradf,states)
print 'Done MOLDEN vector files were generated'







