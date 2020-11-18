# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:05:27 2020

@author: kenzo
"""
import numpy as np
import matplotlib.pyplot as plt
from quagmire.utils.image_mask import circular_mask
from quagmire.fit.sample import az_section



class smooth_check():
    def __init__(self, data, center, r_range, theta_range, N):
        self.data = data
        self.y, self.x = center
        self.r1, self.r2 = r_range
        self.r = np.arange(self.r1, self.r2 + 1)
        self.theta1, self.theta2 = theta_range
        self.N = N
        
    def check_center(self, r = 10):
        mask = circular_mask(radius = r, array_shape = self.data.shape, center = [self.y, self.x], inside_is=False)
        plt.figure(0)
        plt.clf()
        plt.imshow(self.data*mask)

        
    def sample_ring(self, avg = 1):
        theta = []
        theta_val = []  
        r = np.linspace(self.r1, self.r2 + 1, 100)
        for i in r:
            az = az_section(self.data, self.y, self.x, i, self.theta1, self.theta2, self.N)
            az_temp = [[],[]]
            for j in range(int(self.N/avg)):
                az_temp[0].append(np.average(az[0][j*avg:(j + 1)*avg]))
                az_temp[1].append(np.average(az[1][j*avg:(j + 1)*avg]))
            theta.append(az_temp[0])
            theta_val.append(az_temp[1])
        fig, (ax1, ax2) = plt.subplots(1,2)
        ax1.plot(r, np.average(theta_val, axis = 1))
        ax2.plot(theta[0], np.average(theta_val, axis = 0))
        ax2.set_ylim(0, 1)
        return (theta[0], theta_val)
    
        
            
            
            
        
        