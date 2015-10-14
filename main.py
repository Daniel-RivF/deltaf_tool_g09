#!/usr/bin/python
import tools_deltaf as tools
import os, glob
file_log = raw_input(' Filename of the g09 output (including log) \n, remember, should be a single point TDDFT calculation \n')
incr = float(raw_input('value of chosen increment for f gradient calculation: \n'))

tools.writer_inputs(file_log,incr)

print 'g09 input files were generated, have fun \n' 
answ = int(raw_input(' Type \n 0 if u do not want to launch all the generated jobs or \n 1 if u want to launch them \n'))

if answ == 1:
    inputbasename = os.path.splitext(file_log)[0]
    listinputs = glob.glob(inputbasename + '*.com')
    for com in listinputs:
        os.system('Launch_gaussian ' + com)
        print( 'File %s launched' % com)
else:
    print 'Done , calculations were not launched \n'


