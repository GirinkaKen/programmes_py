# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:10:46 2026

@author: PC
"""

import matplotlib.pyplot as plt

notes = [12, 15, 8, 17, 14, 9, 16, 13, 11, 18, 7, 14, 15, 10]

plt.hist(notes, bins=8, color='lightblue', edgecolor='navy')

plt.title("Histogramme des notes")
plt.xlabel("Notes")
plt.ylabel("Fréquence")

plt.show()