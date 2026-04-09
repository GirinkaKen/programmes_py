# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:01:08 2026

@author: PC
"""

import numpy as np
import matplotlib.pyplot as plt

rayon = 5

theta = np.linspace(0, 2 * np.pi, 1000)

x = rayon * np.cos(theta)
y = rayon * np.sin(theta)

plt.figure(figsize=(8, 8))

plt.plot(x, y, 'b-', linewidth=2.5)

plt.plot(0, 0, 'ro', markersize=6)

plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
plt.grid(True, alpha=0.3)

plt.axis('equal')

plt.title('Cercle mathématique\nÉquation : $x^2 + y^2 = r^2$', fontsize=14, pad=20)
plt.xlabel('Axe des x')
plt.ylabel('Axe des y')

plt.show()