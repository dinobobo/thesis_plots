# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:42:24 2020

@author: kenzo
"""

import quagmire.constants as cs
import numpy as np
def thermal_lambda(T):
    return np.sqrt(2*np.pi*cs.hbar**2/(2*cs.m6*cs.kB*T))


def gaussian_peak_rho(N, x, y, z):
    # x, y and z are the 1/e^2 radius
    return N/1.196**3/(x*y*z)

def M_B_r(T, omg):
    return np.sqrt(cs.kB*T/(cs.m6*2*omg**2))


def psd(T, rho):
    return rho*thermal_lambda(T)**3

def chem2rho(mu, a):
    #mu in frequency
    #a in Bohr radius
    return cs.h*mu*2*cs.m6/(a*cs.a0*4*np.pi*cs.hbar**2)

def ef2n(ef):
    # Convert Fermi energy to local density under LDA
    # Input EF in SI units
    # Return total density
    return (2*cs.m6*ef/cs.hbar**2)**1.5/(3*np.pi**2)

def EF_lda(n):
    # Calculate Fermi energy with peak density using LDA
    # Input is total atom density
    # Ourput Fermi energy
    return cs.hbar**2/(2*cs.m6)*(3*n*np.pi**2)**(2/3)

def pair_size(a):
    pass 

def g(a):
    #convert scattering length to pseudo-potential for molecule
    #enter scattering length of the atoms, but returns for value for molecules.
    return 4*np.pi*cs.hbar**2*a*0.6*cs.a0/(cs.m6*2)

def binding_eng(a):
    return cs.hbar**2/(cs.m6*(a*cs.a0)**2)/cs.kB

def kf_a(a,Ef):
    k_F = np.sqrt(Ef*cs.h*cs.m6)/cs.hbar
    return 1/(a*cs.a0*k_F)

def Ef(N, omg):
    return (15*N/16)**0.4*(cs.hbar/(2*cs.m6*14E-6**2)/omg)**0.2*cs.hbar*omg/cs.h

def tbec_tf(t):
    #for an isentropic process, the relation between T/TBEC to T/TF
    #t is (T/T_BEC)^3
    return 8.32/(2*np.pi**2*1.202)*(t)

def t_BEC_ho(omega, N):
    return 0.94*cs.hbar*omega*N**(1/3)/cs.kB

def t_BEC_ring(omg, N):
    return 0.616*cs.hbar*omg*(np.sqrt(cs.hbar/(cs.m6*2*omg))*N/14E-6)**0.5/cs.kB

def q_depletion(a,n):
    return 8/3*np.sqrt(n*(a*cs.a0)**3/np.pi)

def mol_detuning(a):
    return cs.gammaD/(np.pi*2)*(cs.lambdaD2/(np.pi*2*a*cs.a0))**3


def d2tomu(n2d, g, omg):
    #input: peak 2d density of atoms in a ring with SI units; g is the interaction parameter
    #omg is the trapping frequency in the third dimmension.
    #output: chemical potential of the system in temperature units
    return (np.sqrt(9*cs.m6*2/32)*n2d*g*omg)**(2/3)/cs.kB


if __name__ == '__main__':
    #print(thermal_lambda(1E-6)/cs.a0)
    #print(gaussian_peak_rho(2.5E8, 1.071E-3, 0.883E-3, 1.071E-3))
    #print(chem2rho(70000, 1238))
    ef = Ef(3000, 2500*np.pi*2)
    kfa = kf_a(6000,ef)