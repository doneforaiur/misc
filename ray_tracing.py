from PIL import Image
import numba
from numba import jit, cuda, float64, int32,int64, njit,deferred_type
from timeit import default_timer as time


class Vertex:
	def __init__(self, _x, _y, _z):
		self.x = _x
		self.y = _y
		self.z = _z
	def _print(self):
		print(self.x, self.y, self.z)
	def __sub__(self, v2):
		return Vertex(self.x - v2.x, self.y - v2.y, self.z - v2.z)
	def __add__(self, v2):
		return Vertex(self.x + v2.x, self.y + v2.y, self.z + v2.z)
	def vekt(v1, v2): #vektorel carpım tho
		return Vertex(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)
	def skalar(self, skalar):
		return Vertex(self.x * skalar, self.y * skalar, self.z * skalar)
	def __mul__(self, v2):
		return self.x * v2.x + self.y * v2.y + self.z * v2.z
	def norm(self):
		len = self.length()
		return Vertex(self.x/len, self.y/len, self.z/len)
	def length(self):
		return ((self.x**2 + self.y**2 + self.z**2)**(1/2))
		



class Triangle:
	def __init__(self, _v1, _v2, _v3):
		self.vertex1 = Vertex(_v1.x, _v1.y, _v1.z)
		self.vertex2 = Vertex(_v2.x, _v2.y, _v2.z)
		self.vertex3 = Vertex(_v3.x, _v3.y, _v3.z)
	def print_vert(self):
		print(self.vertex1.x, self.vertex1.y, self.vertex1.z)
		print(self.vertex2.x, self.vertex2.y, self.vertex2.z)
		print(self.vertex3.x, self.vertex3.y, self.vertex3.z)


def find_coord(x,y,height,width):
	return Vertex(16*x/width - 8.0, 4.5 -  y*9/height, 20.0)


def intersect(r0, rd, triangle):

	vertex1 = triangle.vertex1
	vertex2 = triangle.vertex2
	vertex3 = triangle.vertex3
	
	N = Vertex.vekt((vertex2 - vertex1),(vertex3 - vertex2))
	
	D = -(vertex1 * N)
	
	t = -( N * r0 + D ) / ( N * rd)
	
	if (t > 0 and (r0 + rd.skalar(t)) != 0 ):
		R = r0 + rd.skalar(t)
		S = Vertex.vekt((vertex2 - vertex1),(vertex3 - vertex2)).length()
		s1 = Vertex.vekt((R - vertex1),(vertex3 - vertex1)).length()
		s2 = Vertex.vekt((vertex2 - vertex1),(R - vertex1)).length()
		s3 = Vertex.vekt((vertex2 - R),(vertex3 - R)).length()

		fark = abs(S - (s1 + s2 + s3))
		epsilon = 0.005
		if (fark < epsilon):
			return t
		else:
			return 0
	return 0


width, height = 499,499


triangles = []


vertex1 = Vertex(0,10,50)
vertex2 = Vertex(10,-10,50)
vertex3 = Vertex(-10,-10,50)

tri1 = Triangle(vertex1, vertex2, vertex3)
tri1.color = (0,255,0)
triangles.append(tri1)

vertex1 = Vertex(10,10,50)
vertex2 = Vertex(0,-10,60)
vertex3 = Vertex(15,-10,40)

tri2 = Triangle(vertex1, vertex2, vertex3)
tri2.color = (0,0,255)
triangles.append(tri2)

vertex1 = Vertex(-10,10,50)
vertex2 = Vertex(0,-10,60)
vertex3 = Vertex(-15,-10,40)

tri3 = Triangle(vertex1, vertex2, vertex3)
tri3.color = (255,0,0)
triangles.append(tri3)

img = Image.new( 'RGB', (width,height), "black") 
pixels = img.load()

start = time()
for x in range(width):
	print(x/width*100) 
	for y in range(height):
		t = []
		for triangle in triangles:
			r0 = Vertex(0,0,0)
			rd = find_coord(x,y,height,width)
			t.append(intersect(r0, rd, triangle))
			
		if not all(v == 0 for v in t):
			min_val = min(i for i in t if i > 0) 
			pixels[x,y] = triangles[t.index(min_val)].color

print("\n" + str(time() - start))
img.show()

