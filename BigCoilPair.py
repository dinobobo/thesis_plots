# -*- coding: utf-8 -*-
"""
Model of big 6x6 winding coil on octagon chamber as built in 2016
"""
from __future__ import division
from numpy import linspace, array, polyfit, poly1d
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from quagmire.magnetics.wire import WireSquareTube
from quagmire.magnetics.coil_array import LoopArrayCoilPair
from quagmire.visual.utils import axisEqual3D
import plot_utilities
            
#------------------------------------------------------------------
# Standard modeling parameters for big coil as of January 2018
#------------------------------------------------------------------            

nv = array([0,0,1])  # normal vector for coil oriented in the z direction

# Axial spacing of the coils: must be minimum 0.0354 m
#"Standard" value for initial 2016 plan was 0.0398 m for a 6x6 coil
# Distance changed to 0.0364 m in Sept 2016 after modeling recessed coil
# Increased to 0.037 m in Dec 2017 after coil mount reconstruction

r0i = array([0, 0, 0.037]) # Distance of coil surface from center plane
radial_coil_thickness = .00352 # +/- .00028 cm
axial_coil_thickness = .00355 # +/- .00028 cm
epoxy_thickness = .0003 # thickness of the layer of epoxy
dR = radial_coil_thickness+epoxy_thickness #
dZ = axial_coil_thickness # spacing of coils axially

Ri = .089  # coil inner radius is 9 cm
NR = 6     # radial coil layers
NZ = 6     # axial coil layers

big_coil_wire = WireSquareTube(outer_side=.0032, inner_side=.0013, material="copper")
BigCoilPair = LoopArrayCoilPair(nv, r0i, Ri, dR, NR, dZ, NZ, big_coil_wire, "HH")

###############################################################################
if __name__ == "__main__":
       
    IHH = 300 # Likely maximum operating current value?
    
    zrng = 0.05
    zvals = linspace(-zrng, zrng, 150) 
    rvals = [ array([0.0,0,z]) for z in zvals]    
    HHvals = BigCoilPair.B(rvals)[:,2] * 10000 * IHH
    
    # Plot on-axis field using the 3D solution implemented in B_loop
    plt.figure(1)
    plt.clf()       
    plt.plot(zvals*100, HHvals, "r.", lw = 2)
    
    #Polynomial fit to the axial Helmholtz data to get field curvature
    HHfitz = polyfit(zvals * 100, HHvals, 7)
    HHfitz_data = poly1d(HHfitz)(zvals * 100)
    plt.plot(zvals * 100, poly1d(HHfitz)(zvals * 100), "r-", label = "Axial Magnetic Field")
    B0 = HHfitz[-1]
    
    plt.xlabel("Z (cm)")
    plt.ylabel("Magnetic Field (G)")
    plt.text(-2, 0.4*B0, "$B_{0}$=%.1f $G$" % HHfitz[-1], fontsize = 12)
    plt.text(-2, 0.2*B0, "$B_z''$=%.3f $G/cm^2$" % HHfitz[-3], fontsize = 12, color = 'r')
    
    R340 = BigCoilPair.resistance(340)
    V = R340 * IHH
    P = R340 * IHH**2
    
    # plt.text(-3, 0.94*B0, "Coil Resistance: %.3f Ohm" %  R340, fontsize=12 )    
    # plt.text(-3, 0.96*B0, "Power Dissipated: %d W" %  P, fontsize=12 )
    # plt.text(-3, 0.98*B0, "Voltage Drop: %.3f V" %  V, fontsize=12 )
    
    # Plot Radial Field
    xrng = zrng
    xvals = linspace(-xrng, xrng, 150)
    rxvals = [ array([x,0,0.0]) for x in xvals]
    HHBx = BigCoilPair.B(rxvals)[:,2] * 10000 * IHH
    plt.plot(xvals*100, HHBx, "b.", lw= 2)
    
    HHfitr = polyfit(xvals * 100, HHBx, 7)
    HHfitr_data = poly1d(HHfitr)(xvals * 100)    
    plt.plot(zvals * 100, poly1d(HHfitr)(xvals * 100), "b-", label = "Radial Magnetic Field")
    plt.text(-2, 0.9*B0, "$B_r''$=%.3f $G/cm^2$" % HHfitr[-3], fontsize = 12, color = 'b')
    plt.legend(loc='lower center')
    plt.show()  



    #Calculate magnetic field drop at different locations
    HHval_max = BigCoilPair.B([array([0.0,0.0,0.0])])[:,2] * 10000 * IHH
    HHval_mm = BigCoilPair.B([array([0.0,0.0,0.001])])[:,2] * 10000 * IHH
    HHval_cm = BigCoilPair.B([array([0.0,0.0,0.01])])[:,2] * 10000 * IHH
    mm_dif = HHval_mm - HHval_max
    cm_dif = HHval_cm - HHval_max

    HHBx_max = BigCoilPair.B([array([0.0,0.0,0.0])])[:,2] * 10000 * IHH
    HHBx_mm = BigCoilPair.B([array([0.001,0.0,0.0])])[:,2] * 10000 * IHH
    HHBx_cm = BigCoilPair.B([array([0.01,0.0,0.0])])[:,2] * 10000 * IHH
    mmx_dif = HHBx_mm - HHBx_max
    cmx_dif = HHBx_cm - HHBx_max
    
    
    
    
    
    
    
# Data ploting
plots = plot_utilities.plot_utilities(xlabel = "Z (cm)", ylabel = "Magnetic Field (G)", marker = '.')

plots.label = "Axial Magnetic Field"
plots.plot(xvals*100, HHvals)

plots.color = 'b'
plots.label = "Radial Magnetic Field"
plots.plot(xvals*100, HHBx)

plots.label = None
plots.ls = '-'
plots.plot(xvals*100, HHfitr_data)

plots.color = 'r'
plots.plot(xvals*100, HHfitz_data)

plots.ax.legend(loc = 'lower center' )

plt.savefig("big_coil_field", quality = 100)
    
    
    
    
    
    
    
    


