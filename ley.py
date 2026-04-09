# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:08:37 2026

@author: PC
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ========================
# Fenêtre principale
# ========================
fenetre = tk.Tk()
fenetre.title("Gestion de Bibliothèque")
fenetre.geometry("800x600")
fenetre.configure(bg="#f0f0f0")

# ========================
# Titre
# ========================
titre = tk.Label(fenetre, text="GESTION DE BIBLIOTHÈQUE", 
                 font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
titre.pack(pady=20)

# ========================
# Onglets
# ========================
tab_control = ttk.Notebook(fenetre)
tab_livres = ttk.Frame(tab_control)
tab_membres = ttk.Frame(tab_control)
tab_emprunts = ttk.Frame(tab_control)

tab_control.add(tab_livres, text="Livres")
tab_control.add(tab_membres, text="Membres")
tab_control.add(tab_emprunts, text="Emprunts")
tab_control.pack(expand=1, fill="both")

# ========================
# --- FORMULAIRE LIVRES ---
# ========================
cadre_livres = tk.Frame(tab_livres, bg="#f0f0f0")
cadre_livres.pack(pady=10)

labels_livres = ["Titre :", "Auteur :", "Genre :", "ISBN :", "Année :"]
entries_livres = []

for i, text in enumerate(labels_livres):
    lbl = tk.Label(cadre_livres, text=text, font=("Arial", 12), bg="#f0f0f0", width=12, anchor='e')
    lbl.grid(row=i, column=0, pady=5, padx=5)
    ent = tk.Entry(cadre_livres, font=("Arial", 12), width=30)
    ent.grid(row=i, column=1, pady=5, padx=5)
    entries_livres.append(ent)

titre_entry, auteur_entry, genre_entry, isbn_entry, annee_entry = entries_livres

# Boutons Livres
cadre_btn_livres = tk.Frame(tab_livres, bg="#f0f0f0")
cadre_btn_livres.pack(pady=10)

btn_ajouter_livre = tk.Button(cadre_btn_livres, text="Ajouter", bg="#4CAF50", fg="white", width=10)
btn_ajouter_livre.pack(side=tk.LEFT, padx=5)
btn_modifier_livre = tk.Button(cadre_btn_livres, text="Modifier", bg="#2196F3", fg="white", width=10)
btn_modifier_livre.pack(side=tk.LEFT, padx=5)
btn_supprimer_livre = tk.Button(cadre_btn_livres, text="Supprimer", bg="#f44336", fg="white", width=10)
btn_supprimer_livre.pack(side=tk.LEFT, padx=5)
btn_rechercher_livre = tk.Button(cadre_btn_livres, text="Rechercher", bg="#FF9800", fg="white", width=10)
btn_rechercher_livre.pack(side=tk.LEFT, padx=5)

# Treeview Livres
tree_livres = ttk.Treeview(tab_livres, columns=("Titre","Auteur","Genre","ISBN","Année"), show="headings")
for col in tree_livres["columns"]:
    tree_livres.heading(col, text=col)
tree_livres.pack(fill="both", expand=True, padx=10, pady=10)

# ========================
# --- FORMULAIRE MEMBRES ---
# ========================
cadre_membres = tk.Frame(tab_membres, bg="#f0f0f0")
cadre_membres.pack(pady=10)

labels_membres = ["Nom :", "Prénom :", "Email :", "Téléphone :", "Date inscription :"]
entries_membres = []

for i, text in enumerate(labels_membres):
    lbl = tk.Label(cadre_membres, text=text, font=("Arial", 12), bg="#f0f0f0", width=15, anchor='e')
    lbl.grid(row=i, column=0, pady=5, padx=5)
    ent = tk.Entry(cadre_membres, font=("Arial", 12), width=30)
    ent.grid(row=i, column=1, pady=5, padx=5)
    entries_membres.append(ent)

nom_entry, prenom_entry, email_entry, tel_entry, date_entry = entries_membres

# Boutons Membres
cadre_btn_membres = tk.Frame(tab_membres, bg="#f0f0f0")
cadre_btn_membres.pack(pady=10)

btn_ajouter_membre = tk.Button(cadre_btn_membres, text="Ajouter", bg="#4CAF50", fg="white", width=10)
btn_ajouter_membre.pack(side=tk.LEFT, padx=5)
btn_modifier_membre = tk.Button(cadre_btn_membres, text="Modifier", bg="#2196F3", fg="white", width=10)
btn_modifier_membre.pack(side=tk.LEFT, padx=5)
btn_supprimer_membre = tk.Button(cadre_btn_membres, text="Supprimer", bg="#f44336", fg="white", width=10)
btn_supprimer_membre.pack(side=tk.LEFT, padx=5)
btn_rechercher_membre = tk.Button(cadre_btn_membres, text="Rechercher", bg="#FF9800", fg="white", width=10)
btn_rechercher_membre.pack(side=tk.LEFT, padx=5)

# Treeview Membres
tree_membres = ttk.Treeview(tab_membres, columns=("Nom","Prénom","Email","Téléphone","Date inscription"), show="headings")
for col in tree_membres["columns"]:
    tree_membres.heading(col, text=col)
tree_membres.pack(fill="both", expand=True, padx=10, pady=10)

# ========================
# --- FORMULAIRE EMPRUNTS ---
# ========================
cadre_emprunts = tk.Frame(tab_emprunts, bg="#f0f0f0")
cadre_emprunts.pack(pady=10)

labels_emprunts = ["ID Membre :", "ID Livre :", "Date emprunt :", "Date retour :"]
entries_emprunts = []

for i, text in enumerate(labels_emprunts):
    lbl = tk.Label(cadre_emprunts, text=text, font=("Arial", 12), bg="#f0f0f0", width=15, anchor='e')
    lbl.grid(row=i, column=0, pady=5, padx=5)
    ent = tk.Entry(cadre_emprunts, font=("Arial", 12), width=30)
    ent.grid(row=i, column=1, pady=5, padx=5)
    entries_emprunts.append(ent)

id_membre_entry, id_livre_entry, date_emprunt_entry, date_retour_entry = entries_emprunts

# Boutons Emprunts
cadre_btn_emprunts = tk.Frame(tab_emprunts, bg="#f0f0f0")
cadre_btn_emprunts.pack(pady=10)

btn_ajouter_emprunt = tk.Button(cadre_btn_emprunts, text="Ajouter", bg="#4CAF50", fg="white", width=10)
btn_ajouter_emprunt.pack(side=tk.LEFT, padx=5)
btn_modifier_emprunt = tk.Button(cadre_btn_emprunts, text="Modifier", bg="#2196F3", fg="white", width=10)
btn_modifier_emprunt.pack(side=tk.LEFT, padx=5)
btn_supprimer_emprunt = tk.Button(cadre_btn_emprunts, text="Supprimer", bg="#f44336", fg="white", width=10)
btn_supprimer_emprunt.pack(side=tk.LEFT, padx=5)
btn_rechercher_emprunt = tk.Button(cadre_btn_emprunts, text="Rechercher", bg="#FF9800", fg="white", width=10)
btn_rechercher_emprunt.pack(side=tk.LEFT, padx=5)

# Treeview Emprunts
tree_emprunts = ttk.Treeview(tab_emprunts, columns=("ID Membre","ID Livre","Date Emprunt","Date Retour"), show="headings")
for col in tree_emprunts["columns"]:
    tree_emprunts.heading(col, text=col)
tree_emprunts.pack(fill="both", expand=True, padx=10, pady=10)

# ========================
# Lancer l'application
# ========================
fenetre.mainloop()