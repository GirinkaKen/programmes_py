# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:53:12 2026

@author: PC
"""

nombre = int(input("Entrez un nombre: "))
fact = 1
for i in range(1, nombre+1):
    fact = fact * i 
print(fact)