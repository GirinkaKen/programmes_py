# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:12:42 2026

@author: PC
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ========================
# Fenêtre principale
# ========================
fenetre = tk.Tk()
fenetre.title("Gestion de Bibliothèque")
fenetre.geometry("900x650")
fenetre.configure(bg="#eef1f5")

# ========================
# Titre
# ========================
titre = tk.Label(fenetre, text="GESTION DE BIBLIOTHÈQUE",
                 font=("Arial", 20, "bold"),
                 bg="#eef1f5", fg="#2c3e50")
titre.pack(pady=15)

# ========================
# Onglets
# ========================
tab_control = ttk.Notebook(fenetre)
tab_livres = ttk.Frame(tab_control)
tab_control.add(tab_livres, text="Livres")
tab_control.pack(expand=1, fill="both")

# ========================
# Cadre formulaire
# ========================
cadre = tk.Frame(tab_livres, bg="white", bd=2, relief="groove")
cadre.pack(pady=15, padx=20)

# Champs
tk.Label(cadre, text="Titre :", bg="white").grid(row=0, column=0, pady=5)
tk.Label(cadre, text="Auteur :", bg="white").grid(row=1, column=0, pady=5)
tk.Label(cadre, text="Genre :", bg="white").grid(row=2, column=0, pady=5)
tk.Label(cadre, text="ISBN :", bg="white").grid(row=3, column=0, pady=5)
tk.Label(cadre, text="Année :", bg="white").grid(row=4, column=0, pady=5)

titre_entry = tk.Entry(cadre, width=30)
auteur_entry = tk.Entry(cadre, width=30)
genre_entry = tk.Entry(cadre, width=30)
isbn_entry = tk.Entry(cadre, width=30)
annee_entry = tk.Entry(cadre, width=30)

titre_entry.grid(row=0, column=1, padx=10)
auteur_entry.grid(row=1, column=1, padx=10)
genre_entry.grid(row=2, column=1, padx=10)
isbn_entry.grid(row=3, column=1, padx=10)
annee_entry.grid(row=4, column=1, padx=10)

# ========================
# Treeview
# ========================
tree = ttk.Treeview(tab_livres, columns=("Titre","Auteur","Genre","ISBN","Année"), show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True, padx=20, pady=10)

# ========================
# Fonctions
# ========================
def ajouter():
    tree.insert("", "end", values=(
        titre_entry.get(),
        auteur_entry.get(),
        genre_entry.get(),
        isbn_entry.get(),
        annee_entry.get()
    ))

def supprimer():
    selected = tree.selection()
    if selected:
        tree.delete(selected[0])
    else:
        messagebox.showwarning("Attention", "Sélectionne un élément")

def modifier():
    selected = tree.selection()
    if selected:
        tree.item(selected[0], values=(
            titre_entry.get(),
            auteur_entry.get(),
            genre_entry.get(),
            isbn_entry.get(),
            annee_entry.get()
        ))

def remplir(event):
    selected = tree.selection()
    if selected:
        valeurs = tree.item(selected[0], "values")

        titre_entry.delete(0, tk.END)
        titre_entry.insert(0, valeurs[0])

        auteur_entry.delete(0, tk.END)
        auteur_entry.insert(0, valeurs[1])

        genre_entry.delete(0, tk.END)
        genre_entry.insert(0, valeurs[2])

        isbn_entry.delete(0, tk.END)
        isbn_entry.insert(0, valeurs[3])

        annee_entry.delete(0, tk.END)
        annee_entry.insert(0, valeurs[4])

def rechercher():
    mot = titre_entry.get().lower()

    for item in tree.get_children():
        valeurs = tree.item(item, "values")
        if mot in valeurs[0].lower():
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
            return

    messagebox.showinfo("Recherche", "Livre non trouvé")

tree.bind("<<TreeviewSelect>>", remplir)

# ========================
# Boutons stylés
# ========================
cadre_btn = tk.Frame(tab_livres, bg="#eef1f5")
cadre_btn.pack(pady=10)

def bouton(txt, cmd, color):
    return tk.Button(cadre_btn, text=txt, command=cmd,
                     bg=color, fg="white",
                     font=("Arial", 11, "bold"),
                     width=12)

bouton("Ajouter", ajouter, "#27ae60").pack(side=tk.LEFT, padx=5)
bouton("Modifier", modifier, "#2980b9").pack(side=tk.LEFT, padx=5)
bouton("Supprimer", supprimer, "#c0392b").pack(side=tk.LEFT, padx=5)
bouton("Rechercher", rechercher, "#f39c12").pack(side=tk.LEFT, padx=5)

# ========================
# Lancer
# ========================
fenetre.mainloop()