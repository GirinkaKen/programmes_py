# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:55:53 2026

@author: PC
"""

import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Formulaire")

label1 = tk.Label(fenetre, text="Nom")
label1.grid(row=0, column=0)

label2 = tk.Label(fenetre, text="Prénom")
label2.grid(row=1, column=0)

label3 = tk.Label(fenetre, text="Âge")
label3.grid(row=2, column=0)

entry1 = tk.Entry(fenetre)
entry1.grid(row=0, column=1)

entry2 = tk.Entry(fenetre)
entry2.grid(row=1, column=1)

entry3 = tk.Entry(fenetre)
entry3.grid(row=2, column=1)

bouton_ajouter = tk.Button(fenetre, text="Ajouter")
bouton_ajouter.grid(row=3, column=1)

bouton_supprimer = tk.Button(fenetre, text="Supprimer")
bouton_supprimer.grid(row=3, column=2)

fenetre.mainloop()