import numpy as np


lat = np.loadtxt("unit_cell.dat").T # Vector are loaded in column form
dims= 3,3, 1 
np.savetxt("cell.dat",np.diag((dims))@lat)

#Metric matrix should be defined within the system once the vectors are loaded
def Metric(lat): #This matrix is compatible with submiting the points in fractional coordinates as column vector
    return ((lat.T)@(lat))
metric_tensor = Metric(lat);

frac_Apoints= np.array([x.flatten() for x in np.mgrid[0:dims[0], 0:dims[0], 0:1] ]) #Generates the lattice points in the fractional coordinates as column vectors
frac_Bpoints= np.array([[1/3],[1/3],[0]])+frac_Apoints #Generates the lattice points in the fractional coordinates as column vectors
frac_points = np.concatenate((frac_Apoints,frac_Bpoints), axis=1)
cart_points = lat@frac_points

import matplotlib.pyplot as plt

plt.scatter(cart_points[0],cart_points[1])
plt.title('Pristine Graphene')
plt.xlabel('x (nm)')
plt.ylabel('y (nm)')
# Set aspect ratio to be equal
plt.axis('equal')
plt.savefig('pristinte_graphene.png')
np.savetxt("pristinte_graphene.xyz", cart_points.T)


#DISORDERED GRAPHENE
frac_points = np.transpose([ (np.random.rand(3)-1)*0.2+x for x in frac_points.T])
cart_points = lat@frac_points

import matplotlib.pyplot as plt

plt.scatter(cart_points[0],cart_points[1])
plt.title('Disordered Graphene')
plt.xlabel('x (nm)')
plt.ylabel('y (nm)')
# Set aspect ratio to be equal
plt.axis('equal')
plt.savefig('disordered_graphene.png')
np.savetxt("disordered_graphene.xyz", cart_points.T)





#from scipy.spatial.distance import cdist
#a = 2.46;
#a1 = np[1,0,0]

#point_frac = [ x.flatten() for x in np.mgrid[0:5, 0:5, 0:1] ];
#print(  [ x.flatten() for x in np.mgrid[0:5, 0:5, 0:1] ]   )
