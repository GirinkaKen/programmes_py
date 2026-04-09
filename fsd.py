# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:04:43 2026

@author: PC
"""
def triangle_pascal(n):
    for i in range(n):
        nombre = 1
        for j in range(i + 1):
            print(nombre, end=" ")
            nombre = nombre * (i - j) // (j + 1)
        print()
n = int(input("Entrez le nombre de lignes : "))
triangle_pascal(n)