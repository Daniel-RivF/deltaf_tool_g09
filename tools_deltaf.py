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


def writer_inputs(file_log,incr,route_sect):
    data = increment_geoms(file_log,incr)[1:]
    Z, incrementlist_P, incrementlist_N = data[0], data[1], data[2]
    pos = [zip(i,j.tolist()) for i,j  in zip(Z,incrementlist_P)]
    neg = [zip(i,j.tolist()) for i,j  in zip(Z,incrementlist_N)]
    for p in enumerate(pos):
        foutname = os.path.splitext(file_log)[0]
        index = p[0]
        index3 = '%03d' % index
        with open(foutname + '_P_' + str(index3) + '.com', 'w') as fo:
            fo.write('%schk=oscillatorgrad%s \n' %('%',index))
            fo.write('%nproc=4 \n')
            fo.write('%mem=4gb \n')
            ###LEVEL OF THEORY
            fo.write('%s \n' % route_sect)
            fo.write(' \n')
            fo.write('METAL \n')
            fo.write(' \n')
            fo.write('0 1 \n')
            for row in  p[1]:
                 fo.write('%s %s \n' %(row[0], ' '.join(map(str,row[1])) ))
            fo.write(' \n')
    # for incr < 0 shitty:
    for n in enumerate(neg):
        foutname_n = os.path.splitext(file_log)[0]
        index = n[0]
        index3 = '%03d' % index
        with open(foutname_n + '_N_' + str(index3) + '.com', 'w') as fon:
            fon.write('%schk=oscillatorgrad%s \n' %('%',index))
            fon.write('%nproc=4 \n')
            fon.write('%mem=4gb \n')
            ###LEVEL OF THEORY
            fon.write('%s \n' % route_sect)
            fon.write(' \n')
            fon.write('METAL \n')
            fon.write(' \n')
            fon.write('0 1 \n')
            for rown in  n[1]:
                 fon.write('%s %s \n' %(rown[0], ' '.join(map(str,rown[1])) ))
            fon.write(' \n')

    return



###################################
##### Now working with outputs:
###################################

def extract_f(filename):
    first = 'Excitation energies and oscillator strengths'
    second = 'Copying SCF densities to generalized density'
    a = parser(filename,first,second)
    b = [ i.split()[8][2:] for i in a if 'Excited State' in i]
    c = np.array(map(float,b))
    return c

#filelist_N = sorted(glob.glob('*N*.com'))

def gradient_f(incr):
    filelist_N = sorted(glob.glob('*_N*.log'))
    filelist_P = sorted(glob.glob('*_P*.log'))
    f_Ns = []
    for i in filelist_N:
        fN = extract_f(i)
        f_Ns.append(fN)
    f_Ps = []
    for j in filelist_P:
        fP = extract_f(j)
        f_Ps.append(fP)
    list_gradf = []
    for i,j in zip(f_Ps,f_Ns):
        #Gradient calculation, retunrns fot all of the NStates:
        a = (i-j)/(2*incr)
        list_gradf.append(a)
    return list_gradf


######################################
################ Chunks of list #######
######################################
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def Z_to_atomsymbol(listZ):
    for index,z in enumerate(listZ):
        if z == 6:
            listZ[index] = 'C'
        elif z == 8:
            listZ[index] = 'O'
        elif z == 1:
            listZ[index] = 'H'
        elif z == 7:
            listZ[index] = 'N'
    return listZ

def states_gradf(filename,list_gradf,states):
    geom = extractgeom(filename)[0]
    Z = Z_to_atomsymbol(extractgeom(filename)[1])
    Natom = len(Z)
#Tratar list_gradf para escribirla mejor, better in chunks of 3
#states as a list of integers i.e [2,5,6,12]
    states_gradf = []
    for i in states:
        a = [j[i-1] for j in list_gradf]
        states_gradf.append(a)
    for state,gradf in zip(states,states_gradf):
        filevector = 'gradient_f' + str(state) + '.vector.molden'
        gradient_i = list(chunks(gradf, 3))
####    moldenfileformat
        with open(filevector,'w') as fv:
            fv.write('[Molden Format]  \n')
            fv.write(' [GEOMETRIES] (XYZ)  \n')
            fv.write('%s \n' % Natom)
            fv.write('  \n')
            ####GEOMETRY (loop)###
            for i,ii in zip(Z,geom):
                fv.write('%s   %s \n' % (i,' '.join(map(str,ii))))
            fv.write('%s \n' % Natom)
            fv.write('  \n')
            ######geometry Vector (loop,again) #######
            for k,kk in zip(Z,geom):
                fv.write('%s %s \n' % (k,' '.join(map(str,kk))))
            fv.write(' [FORCES] \n')
            fv.write('point     1 \n')
            fv.write('%s \n' % Natom)
            ###### gradf Vector (loop) #######
            for v in gradient_i:
                fv.write('%s  \n' % ' '.join(map(str,v)))
            #for z in list_gradf
            fv.write('   \n')
    return  


