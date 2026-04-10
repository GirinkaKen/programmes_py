# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:19:32 2026

@author: PC
"""
import tkinter as tk 
def soumettre():
   nom = entry_nom.get() 
   print(f"Bonjour, {nom}!") 
fenetre = tk.Tk() 
fenetre.title("Formulaire d'Entrée") 
label_nom = tk.Label(fenetre, text="Entrez votre nom :") 
label_nom.pack() 
entry_nom = tk.Entry(fenetre) 
entry_nom.pack() 
button_soumettre = tk.Button(fenetre, text="Soumettre", command=soumettre) 
button_soumettre.pack() 
fenetre.mainloop() 