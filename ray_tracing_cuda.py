from PIL import Image
from numba import jit, cuda, float64,guvectorize
from timeit import default_timer as time
import numpy as np
from numpy import zeros, array 


# CUDA returnleyemiyor.
# Numba da __add__'i degistirmeme izin vermiyor.
# Tuple'lar da immutable, hehe


#@jit(target="gpu")
#def lengt(leng,vertex):
#	leng = np.append([(vertex[0] ** 2 + vertex[1] ** 2 + vertex[2] ** 2) ** (1/2)])


@guvectorize(['float32[:],float32[:], float32[:,:], f8[:]'], '(n1),(n2),(n3,n4) -> ()', target='cuda')
def intersect(r0, rd, vertex, t):
	# for i in range(len(vertex)):
		# leng[i] = ((vertex[i][0] ** 2 + vertex[i][1] ** 2 + vertex[i][2] ** 2) ** (1/2))
		# for j in range(3):
			# norm[i][j] = vertex[i][j] / leng[i]
	
	n3, n4 = vertex.shape
	
	for i in range(n3):
		sub_1_x = vertex[i+1][0] - vertex[i][0]
		sub_1_y = vertex[i+1][1] - vertex[i][1]
		sub_1_z = vertex[i+1][2] - vertex[i][2]
	
	
		sub_2_x = vertex[i+2][0] - vertex[i+1][0]
		sub_2_y = vertex[i+2][1] - vertex[i+1][1]
		sub_2_z = vertex[i+2][2] - vertex[i+1][2]
	
	
	
		N_x = sub_1_y * sub_2_z - sub_1_z * sub_2_y
		N_y = sub_1_z * sub_2_x - sub_1_x * sub_2_z
		N_z = sub_1_x * sub_2_y - sub_1_y * sub_2_x
		
		_r0 = (0,0,1)
		_rd = (-6.88, -4.32, 20.0)
		D = vertex[i][0] * N_x + vertex[i][1] * N_y + vertex[i][2] * N_z
		mul = (_r0[0] * N_x + _r0[1] * N_y + _r0[2] * N_z - D)
		div = (_rd[0] * N_x + _rd[1] * N_y + _rd[2] * N_z)
		
		i=i+3
	
		
		t[0] = -(mul/div)
		return
		print(-(mul/div))
		#if (t_ > 0.0 and div != 0):
			#R_x = 
			#R_y = 
			#R_z = 
		#	pass
		
vertex 	= np.array([[0,10,21],[10,-10,21],[-10,-10,21]], np.float32) 

r0 = np.random.uniform(low = 0, high = 1,size =(3)) 
rd = np.random.uniform(low = 0, high = 1,size =(1*1,3)) 

start = time() 
t = np.random.uniform(low = 0, high = 1,size =(1*1*3)) 
r0 	= np.array(r0, dtype=np.float32)
rd 	= np.array(rd, dtype=np.float32)


t = intersect(r0,rd,vertex)

print(t)

print("with GPU:", time()-start) 
