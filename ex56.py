# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:01:39 2026

@author: PC
"""
import matplotlib.pyplot as plt
import numpy as np

# Paramètres du cercle
rayon = 8
centre_x = 0
centre_y = 0

theta = np.linspace(0, 2*np.pi, 100)

x = centre_x + rayon * np.cos(theta)
y = centre_y + rayon * np.sin(theta)

plt.plot(x, y)

plt.gca().set_aspect('equal')

plt.title("Cercle avec matplotlib")

plt.show()