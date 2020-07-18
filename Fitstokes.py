#!python
# -*-coding:Utf-8 -*
import sys
import numpy as np
from scipy import optimize
np.set_printoptions(precision=1)  # For compact display.
if len(sys.argv)>1:
    data=np.loadtxt(sys.argv[1])
else :
    data=np.loadtxt("Stokes")

# param=angle mode propre, angle rotation, angle tilt
def rot_diff(param,vstokes):
    """ 
    Stokes(tourné)-Stokes(Init)
    Stokes(tourné): rotation autours du mode propre de psi
    mode propre= u definit ci dessous
    """
    t0,psi,tilt = param
    # coordonnes ux,uy,uz du mode propre en fonction de teta et de tilt
    ux=np.cos(2*t0)*np.cos(2*tilt)
    uy=np.cos(2*t0)*np.sin(2*tilt)
    uz=np.sin(2*t0)
    # rotation de psi autour de u=(ux,uy,uz)
    S1=vstokes[:,0]*(ux*ux*(1-np.cos(psi))+np.cos(psi))
    S1+=vstokes[:,2]*(ux*uz*(1-np.cos(psi))+uy*np.sin(psi))

    S2=vstokes[:,0]*(ux*uy*(1-np.cos(psi))+uz*np.sin(psi))
    S2+=vstokes[:,2]*(uy*uz*(1-np.cos(psi))-ux*np.sin(psi))

    S3=vstokes[:,1]*(ux*uz*(1-np.cos(psi))-uy*np.sin(psi))
    S3+=vstokes[:,2]*(uz*uz*(1-np.cos(psi))+np.cos(psi))

    diff=np.column_stack((S1,S2,S3))-vstokes[0:,4:]
    #le ravel met a plat le tableau
    return(diff.ravel())

x0=[np.deg2rad(45),np.deg2rad(-45),0]
sol,flag =optimize.leastsq(rot_diff,x0,args=(data))
print(np.cos(2*sol[0])*np.cos(2*sol[2]),np.cos(2*sol[0])*np.sin(2*sol[2]),np.sin(2*sol[2]))
print(-1*np.cos(2*sol[0])*np.cos(2*sol[2]),-1*np.cos(2*sol[0])*np.sin(2*sol[2]),-1*np.sin(2*sol[2]))
print(np.rad2deg(sol)[0],np.rad2deg(sol)[1],np.rad2deg(sol)[2])


