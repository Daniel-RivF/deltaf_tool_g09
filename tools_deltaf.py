import os, glob
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
    z = map(int,[i[1] for i in geom_z])
    geom = np.array(geom)
    return (geom, z)


def increment_geoms(filename,incr):
    geom = extractgeom(filename)[0]
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
    Z = [ extractgeom(filename)[1] ] * len(a)
    return (a, Z, incrementlist_P, incrementlist_N)


def writer_inputs(file_log,incr,filename_out):
    data = increment_geoms(file_log,incr)[1:]
    Z, incrementlist_P, incrementlist_N = data[0], data[1], data[2]
    pos = [zip(i,j.tolist()) for i,j  in zip(Z,incrementlist_P)]
    neg = [zip(i,j.tolist()) for i,j  in zip(Z,incrementlist_N)]
    for p in enumerate(pos):
        foutname = os.path.splitext(file_log)[0]
        index = p[0]
        with open(foutname + '_' + str(index) + '_P.com', 'w') as fo:
            fo.write('%schk=oscillatorgrad%s \n' %('%',index))
            fo.write('%nproc=4 \n')
            fo.write('%mem=4gb \n')
            ###LEVEL OF THEORY
            fo.write('#p B3LYP/6-31+g** geom=allcheck guess=read TD=(Nstates=20) Nosymm GFinput \n')
            fo.write(' \n')
            fo.write('METAL \n')
            fo.write(' \n')
            for row in  p[1]:
                 fo.write('%s %s \n' %(row[0], ' '.join(map(str,row[1])) ))
            fo.write(' \n')
    # for incr < 0 shitty:
    for n in enumerate(neg):
        foutname_n = os.path.splitext(file_log)[0]
        index = n[0]
        with open(foutname_n + '_' + str(index) + '_N.com', 'w') as fon:
            fon.write('%schk=oscillatorgrad%s \n' %('%',index))
            fon.write('%nproc=4 \n')
            fon.write('%mem=4gb \n')
            ###LEVEL OF THEORY
            fon.write('#p B3LYP/6-31+g** geom=allcheck guess=read TD=(Nstates=20) Nosymm GFinput \n')
            fon.write(' \n')
            fon.write('METAL \n')
            fon.write(' \n')
            for rown in  n[1]:
                 fon.write('%s %s \n' %(rown[0], ' '.join(map(str,rown[1])) ))
            fon.write(' \n')






    return

