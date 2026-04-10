# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 21:51:18 2026

@author: PC
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime

# ========================
# Connexion MySQL avec pymysql
# ========================
try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",                    # Change si tu as un mot de passe
        database="Bibliotheques",
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("✅ Connexion réussie avec pymysql !")
except Exception as err:
    messagebox.showerror("Erreur de connexion", f"Impossible de se connecter à MySQL :\n{err}")
    conn = None
    cursor = None

# ========================
# Fenêtre principale
# ========================
root = tk.Tk()
root.title("Gestion de Bibliothèque - Professionnel")
root.geometry("1280x860")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=32)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

style.configure("success.TButton", background="#28a745", foreground="white")
style.configure("info.TButton", background="#17a2b8", foreground="white")
style.configure("danger.TButton", background="#dc3545", foreground="white")
style.configure("warning.TButton", background="#ffc107", foreground="black")

# ========================
# Variables globales
# ========================
entries_livres = tree_livres = None
entries_membres = tree_membres = None
entries_emprunts = tree_emprunts = None

# ========================
# Utilitaires
# ========================
def check_connexion():
    if conn is None or cursor is None:
        messagebox.showerror("Erreur", "Pas de connexion à la base de données")
        return False
    return True

def confirm_suppression():
    return messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élément ?", icon="warning")

# ========================
# Validation champs obligatoires
# ========================
def valider_champs(entries, obligatoires):
    for i, est_obligatoire in enumerate(obligatoires):
        if est_obligatoire and not entries[i].get().strip():
            messagebox.showwarning("Champ obligatoire", f"Le champ '{labels[i]}' est obligatoire !")
            entries[i].focus()
            return False
    return True

# ========================
# Création onglet
# ========================
def create_tab(parent, labels, tree_columns, table_name, champs_obligatoires):
    main_frame = ttk.Frame(parent)
    main_frame.pack(expand=True, fill="both", padx=20, pady=15)

    form_frame = ttk.LabelFrame(main_frame, text=" Formulaire ", padding=20)
    form_frame.pack(fill="x", pady=(0, 20))

    entries = []
    for i, text in enumerate(labels):
        ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=(0,15), pady=9)
        
        if "Livre" in text or "Membre" in text:
            widget = ttk.Combobox(form_frame, width=47, font=("Segoe UI", 11), state="readonly")
        else:
            widget = ttk.Entry(form_frame, width=50, font=("Segoe UI", 11))
        
        widget.grid(row=i, column=1, pady=9, padx=5)
        entries.append(widget)

    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=18)

    ttk.Button(btn_frame, text="Ajouter", style="success.TButton",
               command=lambda: globals()[f"ajouter_{table_name}"](entries)).pack(side=tk.LEFT, padx=8)
    ttk.Button(btn_frame, text="Modifier", style="info.TButton",
               command=lambda: globals()[f"modifier_{table_name}"](entries, tree)).pack(side=tk.LEFT, padx=8)
    ttk.Button(btn_frame, text="Supprimer", style="danger.TButton",
               command=lambda: globals()[f"supprimer_{table_name}"](tree)).pack(side=tk.LEFT, padx=8)
    ttk.Button(btn_frame, text="Rechercher", style="warning.TButton",
               command=lambda: globals()[f"rechercher_{table_name}"](entries, tree)).pack(side=tk.LEFT, padx=8)
    ttk.Button(btn_frame, text="Actualiser",
               command=lambda: actualiser(table_name, tree)).pack(side=tk.LEFT, padx=8)

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings", height=18)
    for col in tree_columns:
        tree.heading(col, text=col)
        tree.column(col, width=155, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    return entries, tree

def actualiser(table_name, tree):
    if not check_connexion(): return
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute(f"SELECT * FROM {table_name}")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# ========================
# Onglets
# ========================
tab_control = ttk.Notebook(root)

labels_livres = ["Titre :", "Auteur :", "Genre :", "ISBN :", "Année :"]
cols_livres = ("ID", "Titre", "Auteur", "Genre", "ISBN", "Année")
tab_livres_frame = ttk.Frame(tab_control)
entries_livres, tree_livres = create_tab(tab_livres_frame, labels_livres, cols_livres, "livres", [True, True, False, False, False])
tab_control.add(tab_livres_frame, text=" Livres ")

labels_membres = ["Nom :", "Prénom :", "Email :", "Téléphone :", "Adresse :", "Date Inscription (AAAA-MM-JJ) :"]
cols_membres = ("ID", "Nom", "Prénom", "Email", "Téléphone", "Adresse", "Date Inscription")
tab_membres_frame = ttk.Frame(tab_control)
entries_membres, tree_membres = create_tab(tab_membres_frame, labels_membres, cols_membres, "membres", [True, True, False, False, False, False])
tab_control.add(tab_membres_frame, text=" Membres ")

labels_emprunts = ["Livre :", "Membre :", "Date Emprunt :", "Date Retour Prévue :", "Date Retour Effective :", "Statut :"]
cols_emprunts = ("ID", "ID Livre", "ID Membre", "Date Emprunt", "Date Retour Prévue", "Date Retour Effective", "Statut")
tab_emprunts_frame = ttk.Frame(tab_control)
entries_emprunts, tree_emprunts = create_tab(tab_emprunts_frame, labels_emprunts, cols_emprunts, "emprunts", [True, True, False, True, False, False])
tab_control.add(tab_emprunts_frame, text=" Emprunts ")

# ========================
# Fonctions CRUD (je te donne seulement les principales pour ne pas allonger trop)
# Tu peux garder les fonctions que tu avais avant pour ajouter_livres, modifier_livres, etc.
# ========================

def charger_listes_emprunts():
    if not check_connexion(): return
    try:
        cursor.execute("SELECT id, titre FROM livres ORDER BY titre")
        livre_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        entries_emprunts[0]['values'] = livre_list

        cursor.execute("SELECT id, nom, prenom FROM membres ORDER BY nom")
        membre_list = [f"{row[0]} - {row[1]} {row[2]}" for row in cursor.fetchall()]
        entries_emprunts[1]['values'] = membre_list
    except Exception as e:
        print("Erreur chargement listes :", e)

# ========================
# Lancement
# ========================
tab_control.pack(expand=True, fill="both", padx=10, pady=10)

if conn is not None:
    actualiser("livres", tree_livres)
    actualiser("membres", tree_membres)
    actualiser("emprunts", tree_emprunts)
    charger_listes_emprunts()

root.mainloop()

if conn is not None:
    conn.close()