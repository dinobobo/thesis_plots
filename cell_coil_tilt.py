# -*- coding: utf-8 -*-
"""
Model of set of three independent coil pairs for the glass cell
Updated with latest axial offset values and radius values.
Contains Module for saving multiple plots.
3/1/2019 -  Added Modules for stimation of Zeeman Shifts.
"""
from __future__ import division
from numpy import linspace, array, polyfit, poly1d, savetxt, arange,polyder,roots, isreal, delete, sin, cos, pi
from matplotlib import pyplot as plt

from quagmire.magcoils.coil_array import LoopArrayCoil, LoopArrayCoilPair
from quagmire.magcoils.wire import Wire

###############################################################################
coil_tilt = 0.2 * pi/180   #coil tilt in degrees          
ntop = array([0,0,1])  # normal vector for coil oriented in the z direction
nbot = array([sin(coil_tilt), 0, cos(coil_tilt)])
#nbot = ntop
radial_coil_thickness = .0035 # +/- .00028 cm #In order for 2 windings to be 7.8mm thick
axial_coil_thickness = .0035 # +/- .00028 cm
space_between_windings = 0.0014 #Experimental space between successive loops
axial_offset1 = 0.0018 #axial offset of 2nd coil, Variable 2
axial_offset2 = 0.0093 #axial offset of 3rd coil
IHH1 = 150
IHH2 = 150
IHH3 = 150
Ri = [.02387, .03202, .04025] # coil inner radius is 24 mm (minimum radius is 16 mm due to window OD)
Ro = [.03202, .040065, .062365]# coil outer radius is 24 mm (minimum radius is 16 mm due to window OD)
NR = [2, 2, 6]    # radial coil layers
NZ = [3, 3, 2]    # axial coil layers
r0i = []
r0i.append(array([0, 0, 0.010])) # Distance of coil surface 1 from center plane #Z coordinate
r0i.append(array([0, 0, 0.010 +axial_offset1]))# Distance of coil surface 2 from center plane
r0i.append(array([0, 0, 0.010 + axial_offset2]))
dR= [0,0,0]
dZ = dR
CellCoil = []
CellCoilx = []
hbar =  1.054*(10**(-34)) #Planck's constant by 2*pi
ub = 9.274*(10**(-24)) #Bohr Magneton
gI= -0.000446540 #Nuclear g factor
gJset = [[2.0023010,0.5,"2S1/2"], [0.6668,0.5,"2P1/2"], [1.335,1.5,"2P3/2"]] #Electronic G factors along with J values and names of fine levels
material = Wire("Copper")

def ZeemanShift(gJ, mJ, mI, B):
    Eset= []
    for l in B:
        E= (ub/hbar)*(gJ*mJ + gI*mI)*l/(10**10)#Dividing by 10^10 to account for Gauss->Tesla and to return in Mhz.
        Eset.append(E)
    return Eset


if __name__ == "__main__":
    
    #------------------------------------------------------------------
    # Generate plots for field in Helmholtz configuration
    #------------------------------------------------------------------
    
    zrng = 0.015 #z variable of the centre of upper loop
    zvals = linspace(-zrng, zrng, 150) 
    rvals = [ array([0,0,z]) for z in zvals]   
    
    for i in range(0,3,1):
        dR[i] = (Ro[i] -  Ri[i])/NR[i]
        dZ[i] = axial_coil_thickness
        CellCoil.append(LoopArrayCoil(ntop,r0i[i],Ri[i],dR[i],NR[i],dZ[i],NZ[i],material).B(rvals)[:,2]+ \
                        LoopArrayCoil(nbot, -r0i[i], Ri[i], dR[i], NR[i], -dZ[i], NZ[i], material).B(rvals)[:,2])
        

    '''
    [RETIRED]This part was inserted to study the effect of axial offsets on the field.
    radii = linspace(0.016,0.026,11)               # Range over which radius is varied
    axialoffset1range = linspace(0.002,0.006,5)    # Range over which axial offset of 2nd coil 
    for axial_offset1 in axialoffset1range:        # Looping over all possible axial offsets
        r0i2 = array([0, 0, 0.010 +axial_offset1]) # Distance of coil surface from center plane
        print('axial_offset1 '+ str(axial_offset1))
        for Ri1 in radii:                          # Looping over all possible inner radii
            print('Inner Radius ' + str(Ri1))
    '''
       
    HHvals = (CellCoil[0] * IHH1 + 
              CellCoil[1] * IHH2 +
              CellCoil[2] * IHH3) * 10000
                       
    '''Bz_max = 0 #Looping to find maximum axial field.
    for B in HHvals:
        if B>Bz_max:
            Bz_max=B
         '''  

                        
    xrng = zrng
    xvals = linspace(-xrng, xrng, 150)
    rxvals = [ array([x,0,0]) for x in xvals]
    
    for i in range(0,3,1):
        dR[i] = (Ro[i] -  Ri[i])/NR[i]
        dZ[i] = axial_coil_thickness
        CellCoilx.append(LoopArrayCoil(ntop,r0i[i],Ri[i],dR[i],NR[i],dZ[i],NZ[i],material).B(rxvals)[:,2]+ \
                        LoopArrayCoil(nbot, -r0i[i], Ri[i], dR[i], NR[i], -dZ[i], NZ[i], material).B(rxvals)[:,2])
                        
    HHBx =( CellCoilx[0] * IHH1 +
            CellCoilx[1] * IHH2 +
            CellCoilx[2] * IHH3) * 10000
    # Plot on-axis field using the 3D solution implemented in B_loop
    plt.figure(200)
    plt.clf()       
    #plt.plot(zvals*100, HHvals, "r.", lw = 2)
    
    #Polynomial fit to the axial and radial Helmholtz data to get field curvature
    HHfitz = polyfit(zvals * 100, HHvals, 15)
    HHfitr = polyfit(xvals * 100, HHBx, 15)
    HHfitzder = polyder(HHfitz) #Derivative of field
    HHfitxder = polyder(HHfitr)
    #Constant Coefficient in the polynomial
    #B0 = HHfitz[-1]
    
    #Axes labels and titles.
    #plt.title("$B_z$ for Helmholtz; $I_{HH}$= %d Amps" % IHH1, fontsize=20)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Gauss", fontsize=20)
    plt.annotate("$B_{0}$=%.1f $G$" % HHfitz[-1], xy=(0.4, 0.3), xycoords='axes fraction', fontsize=15)
    plt.annotate("$B_z(z)''$=%.3f $G/cm^2$" % HHfitz[-3], xy=(0.4, 0.2), xycoords='axes fraction', fontsize = 15, color = 'r') 
    plt.plot(zvals * 100, poly1d(HHfitz)(zvals * 100), "r-") #Plotting the axial field along z direction
    plt.plot(xvals * 100, poly1d(HHfitr)(xvals * 100), "b-") #Plotting the axial-field along x coordinates
    plt.annotate("$B_z(x)''$=%.3f $G/cm^2$" % HHfitr[-3], xy=(0.4, 0.1), xycoords='axes fraction', fontsize = 15, color = 'b') 
    print("Central Field"+str(poly1d(HHfitz)(0))) #Print Central Field Value.
    
    #R340 = CellCoil1.resistance(340)
    #V = R340 * IHH1 #+ R340 * IHH2 + R340 * IHH3
    #P = R340 * IHH1**2 #+ R340 * IHH2**2 + R340 * IHH3**2    
    #plt.annotate("Coil Resistance: %.3f Ohm" %  R340, xy=(0.4, 0.8), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Power Dissipated: %d W" %  P, xy=(0.4, 0.7), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Voltage Drop: %.3f V" %  V, xy=(0.4, 0.6), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Inner Radius: %.3f m" %  Ri1, xy=(0.4, 0.5), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Axial Offset: %.3f m" %  axial_offset1, xy=(0.4, 0.4), xycoords='axes fraction', fontsize=15)
     
    #savetxt("foo.csv",xvals*100 , delimiter=",")
    #savetxt("foo1.csv",poly1d(HHfitr)(xvals * 100) , delimiter=",")
    #plt.savefig('OuterCoilDim'+ str(NR2) +'.png',edgecolor='w',orientation='portrait', transparent=False)
    #print(NR2)    
# =============================================================================
#     import os
#     i = 0
#     while os.path.exists('{}{:d}.png'.format('pics2/MoreMagnifiedRangeAxialOffset1'+str(axial_offset1)+'AxialOffset2'+str(axial_offset2), i)):
#         i += 1
#     plt.savefig('{}{:d}.png'.format('pics2/MoreMagnifiedRangeAxialOffset1'+str(axial_offset1)+'AxialOffset2'+str(axial_offset2), i))
#     print ('Maximum axial field = ')
# =============================================================================
        #print('Maximum radial field = ' + str(Br_max)) #Command to find the maximum fields of all conifgurations.
# =============================================================================
    #Zeeman Shift Calculation
    #Axes labels and titles.
    '''
    for g in gJset:
        mJvals = arange(-1*g[1],g[1]+1,1)
        print(mJvals)
        for mJ in mJvals:
            plt.title("Zeeman Shift map for " + str(g[2])+ " and mJ "+ str(mJ) , fontsize=20)
            plt.xlabel("z (cm)", fontsize=20)
            plt.ylabel("MHz", fontsize=20)
            plt.plot(zvals * 100, ZeemanShift(g[0],mJ,1,poly1d(HHfitzder)(zvals * 100)), "r-")
            plt.annotate("Red mI=1", xy=(0.4, 0.7), xycoords='axes fraction', fontsize=15)
            plt.plot(zvals * 100, ZeemanShift(g[0],mJ,0,poly1d(HHfitzder)(zvals * 100)), "b-")
            plt.annotate("Blue mI=0", xy=(0.4, 0.6), xycoords='axes fraction', fontsize=15)
            plt.plot(zvals * 100, ZeemanShift(g[0],mJ,-1,poly1d(HHfitzder)(zvals * 100)), "g-")
            plt.annotate("Green mI=-1", xy=(0.4, 0.5), xycoords='axes fraction', fontsize=15)
            plt.show()
            '''
    #Solve for the radius of peak.
    drop=20
    HHfitz[-1]=drop #Value of the drop in field
    fwhm=roots(HHfitz)# List of radii in cm where field drops by above given amount.
    fwhm = fwhm[(isreal(fwhm)) & (fwhm<3) & (fwhm>0)] #removing non-real, negative and large values
    print("Field drops by "+str(drop)+" within "+ str(abs(fwhm))+" cm.")
    plt.figure(300)
    plt.plot(zvals*100, poly1d(HHfitzder)(zvals*100))
    plt.plot(xvals*100, poly1d(HHfitxder)(xvals*100))
    grad=poly1d(HHfitxder)(0)
    print("Central r-gradient is " + str(grad))
    
    