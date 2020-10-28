# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:00:35 2016

@author: ppzfrp
"""
# set up random 3-d positions
#
import numpy as np
import time
import errno
from numba import jit
N=np.int(input('N = '))
seed=np.int(input('Random number seed = '))
np.random.seed(seed)
pos=np.random.random((3,N))
start_time=time.time()
# deliberately slow code to find nearest neighbours within periodic unit cube
#
#  You may only change the code in this cell (i.e. between here and "toc")
"""@jit(nopython=True)
def choose_vals(sq_dist, a):
    val = np.argsort(sq_dist)[1]
    return val"""

def find_nearest_neghbour(N):
    #array to store nearest neighbours
    match=np.zeros(N)

    for a in range(N):
        #find distance between coordinates of a given point and all other points
        distance = np.abs(pos - pos[:, a].reshape(3, 1))
        #take the fact that space loops around into account
        distance = np.where(distance < 0.5, distance, distance - 1)
        #find total ditance squared with pythagoras and sort the array
        #sort array with distances to get corresponding indecies and store smallest distance
        match[a] = np.argsort(np.add.reduce(distance**2, axis=0))[1]

    return match

match = find_nearest_neghbour(N)
#print(match)

end_time=time.time() #toc
print('Elapsed time = ',repr(end_time-start_time))

# generate filename from N and seed
filename='pyneigh'+str(N)+'_'+str(seed)
# if a file with this name already exists read in the nearest neighbour
# list found before and compare this to the current list of neighbours,
# else save the neighbour list to disk for future reference
try:
    fid=open(filename,'rb')
    matchold=np.loadtxt(fid)
    fid.close()
    if (matchold==match).all():
        print('Checked match')
    else:
        print('Failed match')
except OSError as e:
    if e.errno == errno.ENOENT:
        print('Saving neighbour list to disk')
        fid=open(filename,'wb')
        np.savetxt(fid,match,fmt="%8i")
        fid.close()
    else:
        raise
#
