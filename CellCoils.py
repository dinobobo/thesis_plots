# -*- coding: utf-8 -*-
"""
Model of set of three independent coil pairs for the glass cell
"""
from __future__ import division
from numpy import linspace, array, polyfit, poly1d
from matplotlib import pyplot as plt

from quagmire.magnetics.wire import WireSquareTube
from quagmire.magnetics.coil_array import LoopArrayCoilPair

###############################################################################
            
n = array([0,0,1])  # normal vector for coil oriented in the z direction

radial_coil_thickness = .0038 # +/- .00028 cm #In order for 2 windings to be 7.8mm thick
axial_coil_thickness = .0038 # +/- .00028 cm
space_between_windings = 0.002 #Experimental space between successive loops
axial_offset1 = 0.002 #placehlder for axial offset of 2nd coil, Variable 2
axial_offset2 = 0.010 #placehlder for axial offset of 3rd coil

dR = radial_coil_thickness
dZ = axial_coil_thickness 


NR = 2     # radial coil layers
NZ = 3    # axial coil layers
NR2 = 6     #radial coil layers of 3rd coil
NZ2 = 2      #axial coil layers of 3rd coil

r0i1 = array([0, 0, 0.010]) # Distance of coil surface 1 from center plane
r0i2 = array([0, 0, 0.010 +axial_offset1]) # Distance of coil surface 2 from center plane
r0i3 = array([0, 0, 0.010 + axial_offset2]) # Distance of coil surface 3 from center plane
# Minimum axial distance is 10 mm becuse of cell thickness

if __name__ == "__main__":
    
    #------------------------------------------------------------------
    # Generate plots for field in Helmholtz configuration
    #------------------------------------------------------------------
    
    wire = WireSquareTube(outer_side=.0032, inner_side=.0013, material="copper")
    
    IHH1 = 160 # Likely maximum operating current value?
    IHH2 = 160
    IHH3 = 160
    Ri1 = .024  # coil inner radius is 24 mm (minimum radius is 16 mm due to window OD)
    Ri2=Ri1+ dR*NR + space_between_windings
    Ri3=Ri2+ dR*NR + space_between_windings
    CellCoil1 = LoopArrayCoilPair(n,r0i1,Ri1,dR,NR,dZ,NZ,wire,"HH")
    CellCoil2 = LoopArrayCoilPair(n,r0i2,Ri2,dR,NR,dZ,NZ,wire,"HH")

    '''
    radii = linspace(0.016,0.026,11)               # Range over which radius is varied
    axialoffset1range = linspace(0.002,0.006,5)    # Range over which axial offset of 2nd coil 
    for axial_offset1 in axialoffset1range:        # Looping over all possible axial offsets
        r0i2 = array([0, 0, 0.010 +axial_offset1]) # Distance of coil surface from center plane
        print('axial_offset1 '+ str(axial_offset1))
        for Ri1 in radii:                          # Looping over all possible inner radii
            print('Inner Radius ' + str(Ri1))
    '''


    CellCoil3 = LoopArrayCoilPair(n,r0i3,Ri3,dR,NR2,dZ,NZ2,wire,"HH")
    
    zrng = 0.05 #z variable of the centre of upper loop
    zvals = linspace(-zrng, zrng, 150) 
    rvals = [ array([0.0,0,z]) for z in zvals]    
    HHvals = (CellCoil1.B(rvals)[:,2] * IHH1 + \
              CellCoil2.B(rvals)[:,2] * IHH2 + \
              CellCoil3.B(rvals)[:,2] * IHH3 ) * 10000
    '''Bz_max = 0 #Looping to find maximum axial field.
    for B in HHvals:
        if B>Bz_max:
            Bz_max=B'''
             
    # Plot on-axis field using the 3D solution implemented in B_loop
    plt.figure(200)
    plt.clf()       
    plt.plot(zvals*100, HHvals, "r.", lw = 2)
    
    #Polynomial fit to the axial Helmholtz data to get field curvature
    HHfitz = polyfit(zvals * 100, HHvals, 15)
    HHfitz_data = poly1d(HHfitz)(zvals * 100)
    plt.plot(zvals * 100, poly1d(HHfitz)(zvals * 100), "r-")
    #Constant Coefficient in the polynomial
    B0 = HHfitz[-1]
    
    #Axes labels and titles.
    #plt.title("$B_z$ for Helmholtz; $I_{HH}$= %d Amps" % IHH1, fontsize=20)
    plt.xlabel("Z (cm)", fontsize=20)
    plt.ylabel("Magnetic Field (G)", fontsize=20)
      
    #plt.annotate("$B_{0}$=%.1f $G$" % HHfitz[-1], xy=(0.4, 0.3), xycoords='axes fraction', fontsize=15)
    #plt.annotate("$B_z(z)''$=%.3f $G/cm^2$" % HHfitz[-3], xy=(0.4, 0.2), xycoords='axes fraction', fontsize = 15, color = 'r') 
    
    R340 = CellCoil1.resistance(340)
    V = R340 * IHH1 + R340 * IHH2 + R340 * IHH3
    P = R340 * IHH1**2 + R340 * IHH2**2 + R340 * IHH3**2    
    #plt.annotate("Coil Resistance: %.3f Ohm" %  R340, xy=(0.4, 0.8), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Power Dissipated: %d W" %  P, xy=(0.4, 0.7), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Voltage Drop: %.3f V" %  V, xy=(0.4, 0.6), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Inner Radius: %.3f m" %  Ri1, xy=(0.4, 0.5), xycoords='axes fraction', fontsize=15)
    #plt.annotate("Axial Offset: %.3f m" %  axial_offset1, xy=(0.4, 0.4), xycoords='axes fraction', fontsize=15)
    
    # Plot Radial Field
    xrng = zrng
    xvals = linspace(-xrng, xrng, 150)
    rxvals = [ array([x,0,0.0]) for x in xvals]
    HHBx =( CellCoil1.B(rxvals)[:,2] * IHH1 + \
            CellCoil2.B(rxvals)[:,2] * IHH2 + \
            CellCoil3.B(rxvals)[:,2] * IHH3 ) * 10000
    '''
    Br_max = 0 #Looping to find maximum radial field.
    for B in HHBx:
        if B>Br_max:
            Br_max=B
    plt.plot(xvals*100, HHBx, "b.", lw= 2)
    '''
    
    HHfitr = polyfit(xvals * 100, HHBx, 15)    
    HHfitr_data = poly1d(HHfitr)(xvals * 100) 
    plt.plot(zvals * 100, poly1d(HHfitr)(xvals * 100), "b-")
    #plt.annotate("$B_z(x)''$=%.3f $G/cm^2$" % HHfitr[-3], xy=(0.4, 0.1), xycoords='axes fraction', fontsize = 15, color = 'b') 
    #plt.savefig('OuterCoilDim'+ str(NR2) +'.png',edgecolor='w',orientation='portrait', transparent=False)
        #plt.savefig('InnerRadius'+str(Ri1)+'AxialOffset'+str(axial_offset1)+'.png',edgecolor='w',orientation='portrait', transparent=False)
        #print ('Maximum axial field = ' + str(Bz_max))
        #print('Maximum radial field = ' + str(Br_max)) #Command to find the maximum fields of all conifgurations.

    #Calculate magnetic field drop at different locations
        

    IHH = IHH1
    rvals = [array([0.0,0.0,0.00]), array([0.0,0.0,0.001]), array([0.0,0.0,0.01])]
    HHval_max, HHval_mm, HHval_cm = (CellCoil1.B(rvals)[:,2] * IHH1 + \
              CellCoil2.B(rvals)[:,2] * IHH2 + \
              CellCoil3.B(rvals)[:,2] * IHH3 ) * 10000

    mm_dif = HHval_mm - HHval_max
    cm_dif = HHval_cm - HHval_max
    
    rvals = [array([0.0,0.0,0.00]), array([0.001,0.0,0.0]), array([0.01,0.0,0.0])]
    HHBx_max, HHBx_mm, HHBx_cm = (CellCoil1.B(rvals)[:,2] * IHH1 + \
              CellCoil2.B(rvals)[:,2] * IHH2 + \
              CellCoil3.B(rvals)[:,2] * IHH3 ) * 10000

    mmx_dif = HHBx_mm - HHBx_max
    cmx_dif = HHBx_cm - HHBx_max

 
# Data ploting
     
import plot_utilities
plots = plot_utilities.plot_utilities(xlabel = "Z (cm)", ylabel = "Magnetic Field (G)", marker = '.')
plots.label = "Axial Magnetic Field"
plots.plot(zvals*100, HHvals)
axins = plots.inset(zvals*100, HHvals, xlim = [-0.2, 0.2], ylim = [860,870], label = "hhvals", zoom = 6, yticks = 3)
plots.label = None
plots.plot(ax = axins, xdata = zvals*100, ydata = HHvals)

plots.color = 'b'
plots.label = "Radial Magnetic Field"
plots.plot(zvals*100, HHBx)
plots.label = None
plots.plot(ax = axins, xdata = zvals*100, ydata = HHBx)


plots.label = None
plots.ls = '-'
plots.plot(zvals*100, HHfitr_data)

plots.color = 'r'
plots.plot(zvals*100, HHfitz_data)

plots.ax.legend(loc = 'lower center' )
axins.set_xlabel(None)
axins.set_ylabel(None)

plt.savefig("cell_coil_field", quality = 100)
