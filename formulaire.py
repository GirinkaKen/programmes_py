# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:30:37 2026

@author: PC
"""

import tkinter as tk
from tkinter import messagebox

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Mon Formulaire")
fenetre.geometry("400x400")

# Titre du formulaire
tk.Label(fenetre, text="Formulaire d'inscription", font=("Arial", 16)).pack(pady=20)

# Nom
tk.Label(fenetre, text="Nom :").pack(anchor="w", padx=50)
nom = tk.Entry(fenetre, width=30)
nom.pack(pady=5)

# Prénom
tk.Label(fenetre, text="Prénom :").pack(anchor="w", padx=50)
prenom = tk.Entry(fenetre, width=30)
prenom.pack(pady=5)

# Âge
tk.Label(fenetre, text="Âge :").pack(anchor="w", padx=50)
age = tk.Entry(fenetre, width=30)
age.pack(pady=5)

# Ville
tk.Label(fenetre, text="Ville :").pack(anchor="w", padx=50)
ville = tk.Entry(fenetre, width=30)
ville.pack(pady=5)

# Bouton pour soumettre
def soumettre():
    n = nom.get()
    p = prenom.get()
    a = age.get()
    v = ville.get()
    
    if n and p and a and v:
        messagebox.showinfo("Succès", f"Merci {p} {n} !\nÂge : {a} ans\nVille : {v}")
    else:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs !")

tk.Button(fenetre, text="Soumettre", command=soumettre, bg="blue", fg="white", font=("Arial", 12)).pack(pady=30)

# Lancer le formulaire
fenetre.mainloop()