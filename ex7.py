# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:15:32 2026

@author: PC
"""

import math 

a = int(input("Entrez le nombre a:  "))
b = int(input("Entrez le nombre b:  "))
c = int(input("Entrez le nombre c:  ")) 

delta = b**2 - 4*a*c 

if a == 0 : 
    print("impossible")

else :
    if delta > 0 :
        x1 = (-b + math.sqrt(delta))/2*a
        x2 = (-b - math.sqrt(delta))/2*a
        print(f"x1 = {x1}, x2 = {x2}")
    
    elif delta == 0 :
        x = -b / 2*a
        print(x)
