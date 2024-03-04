from simpletb.system_old import System

import numpy as np
def hopping( x, y ):
    norm = np.linalg.norm(x-y)
    if ( norm< 0.25  and norm >0.24 ):
        return 2.8
    else:
        return 0.0
    
syst = System(graph=("cell.dat","pristinte_graphene.xyz"))
syst.ComputeNeighbors(0.3)
#syst.SetHoppingFunction( hopping)
