# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:48:38 2026

@author: PC
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ========================
# Fenêtre
# ========================
fenetre = tk.Tk()
fenetre.title("Gestion Bibliothèque")
fenetre.geometry("900x600")
fenetre.configure(bg="#eef1f5")

# ========================
# Titre
# ========================
tk.Label(fenetre, text="GESTION DE BIBLIOTHÈQUE",
         font=("Arial", 18, "bold"),
         bg="#eef1f5").pack(pady=10)

# ========================
# Cadre formulaire
# ========================
cadre = tk.Frame(fenetre, bg="white", bd=2, relief="groove")
cadre.pack(pady=10)

# Champs
tk.Label(cadre, text="Titre :", bg="white").grid(row=0, column=0)
tk.Label(cadre, text="Auteur :", bg="white").grid(row=1, column=0)
tk.Label(cadre, text="Genre :", bg="white").grid(row=2, column=0)
tk.Label(cadre, text="ISBN :", bg="white").grid(row=3, column=0)
tk.Label(cadre, text="Année :", bg="white").grid(row=4, column=0)

titre_entry = tk.Entry(cadre)
auteur_entry = tk.Entry(cadre)
genre_entry = tk.Entry(cadre)
isbn_entry = tk.Entry(cadre)
annee_entry = tk.Entry(cadre)

titre_entry.grid(row=0, column=1)
auteur_entry.grid(row=1, column=1)
genre_entry.grid(row=2, column=1)
isbn_entry.grid(row=3, column=1)
annee_entry.grid(row=4, column=1)

# ========================
# Fonctions
# ========================
def ajouter():
    tree.insert("", "end", values=(
        titre_entry.get(),
        auteur_entry.get(),
        genre_entry.get(),
        isbn_entry.get(),
        annee_entry.get(),
        "Modifier | Supprimer"
    ))

def rechercher():
    mot = titre_entry.get().lower()
    for item in tree.get_children():
        valeurs = tree.item(item, "values")
        if mot in valeurs[0].lower():
            tree.selection_set(item)
            tree.focus(item)
            return
    messagebox.showinfo("Recherche", "Non trouvé")

# ========================
# Boutons sous formulaire
# ========================
cadre_btn = tk.Frame(fenetre, bg="#eef1f5")
cadre_btn.pack(pady=10)

tk.Button(cadre_btn, text="Ajouter", command=ajouter,
          bg="#27ae60", fg="white", width=12).pack(side=tk.LEFT, padx=5)

tk.Button(cadre_btn, text="Rechercher", command=rechercher,
          bg="#f39c12", fg="white", width=12).pack(side=tk.LEFT, padx=5)

# ========================
# Treeview
# ========================
tree = ttk.Treeview(fenetre, columns=("Titre","Auteur","Genre","ISBN","Année","Action"),
                    show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True, padx=20, pady=10)

# ========================
# Clique sur Actions
# ========================
def action_click(event):
    item = tree.identify_row(event.y)
    col = tree.identify_column(event.x)

    if not item:
        return

    # colonne 6 = Action
    if col == "#6":
        x, y, width, height = tree.bbox(item, col)

        if event.x < x + width/2:
            # Modifier
            valeurs = tree.item(item, "values")

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

        else:
            # Supprimer
            tree.delete(item)

tree.bind("<Button-1>", action_click)

# ========================
# Lancer
# ========================
fenetre.mainloop()