
import numpy as np

def parseALL(filename,first,second):
    parsing = False
    name = []
    f = open(filename)
    for line in f.readlines():
        if line.startswith(first):
            parsing = True
            continue
        elif line.startswith(second):
            parsing = False
        if parsing:
            a = line.split()
            name.extend(a)
#    name = map(float,name)
    return name

#################################################
#################################################
#################################################

def parser(filename,first,second):
    whole_data = []
    parse = False
    with open(filename,'r') as out:
     for line in out:
        if str(first) in line:
            parse = True
#            continue
        elif str(second) in line:
            parse = False
        if parse:
            whole_data.append(line)
    out.close()
    return whole_data


def extractgeom(filename):
    first = 'Input orientation:'
    second = 'Distance matrix'
    a = parser(filename,first,second)
    b = [i.split()[3:] for i in a][5:-1]
    geom = [map(float,i) for i in b]
    geom_z = [i.split() for i in a][5:-1]
    z = map(int,[i[1] for i in geomz])
    geom = np.array(geom)
    return geom


def increment_geoms(filename,incr):
    geom = extractgeom(filename)
    nrows, ncols = len(geom),len(geom[0])
    zeros_matrix = np.zeros((nrows,ncols))
    a = []
    for i in xrange(0,nrows):
        for j in xrange(0,ncols):
          # print i,j
           zeros_matrix_1 = np.zeros((nrows,ncols)) 
           zeros_matrix_1[i,j] = incr
           a.append(zeros_matrix_1)
    incrementlist_P, incrementlist_N = [],[]
    for k in a:
        sum_P = geom + k
        incrementlist_P.append(sum_P)
        sum_N = geom - k
        incrementlist_N.append(sum_N)
    return (a, incrementlist_P, incrementlist_N)


def writer_inputs(file_log,incr,filename_out):
    return

