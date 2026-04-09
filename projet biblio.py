# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:12:21 2026

@author: PC
"""

import tkinter as tk
from tkinter import ttk



import mysql.connector

# Connexion
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Bibliotheques"
)

cursor = conn.cursor()


# ========================
# Fenêtre principale
# ========================
fenetre = tk.Tk()
fenetre.title("Gestion Bibliothèque")
fenetre.geometry("600x600")
fenetre.configure(bg="#f0f0f0")

# ========================
# Titre principal
# ========================
titre = tk.Label(fenetre, text="GESTION BIBLIOTHÈQUE",
                 font=("Arial", 18, "bold"),
                 bg="#f0f0f0")
titre.pack(pady=15)

# ========================
# Onglets
# ========================
tab_control = ttk.Notebook(fenetre)

tab_livres = tk.Frame(tab_control, bg="#f0f0f0")
tab_membres = tk.Frame(tab_control, bg="#f0f0f0")
tab_emprunts = tk.Frame(tab_control, bg="#f0f0f0")

tab_control.add(tab_livres, text="Livres")
tab_control.add(tab_membres, text="Membres")
tab_control.add(tab_emprunts, text="Emprunts")

tab_control.pack(expand=1, fill="both")

# =====================================================
# =================== LIVRES ===========================
# =====================================================
cadre_livres = tk.Frame(tab_livres, bg="#f0f0f0")
cadre_livres.pack(pady=20)

tk.Label(cadre_livres, text="Titre :", bg="#f0f0f0").grid(row=0, column=0, pady=5)
entry_titre = tk.Entry(cadre_livres, width=30)
entry_titre.grid(row=0, column=1)

tk.Label(cadre_livres, text="Auteur :", bg="#f0f0f0").grid(row=1, column=0, pady=5)
entry_auteur = tk.Entry(cadre_livres, width=30)
entry_auteur.grid(row=1, column=1)

tk.Label(cadre_livres, text="Genre :", bg="#f0f0f0").grid(row=2, column=0, pady=5)
entry_genre = tk.Entry(cadre_livres, width=30)
entry_genre.grid(row=2, column=1)

tk.Label(cadre_livres, text="ISBN :", bg="#f0f0f0").grid(row=3, column=0, pady=5)
entry_isbn = tk.Entry(cadre_livres, width=30)
entry_isbn.grid(row=3, column=1)

tk.Label(cadre_livres, text="Année :", bg="#f0f0f0").grid(row=4, column=0, pady=5)
entry_annee = tk.Entry(cadre_livres, width=30)
entry_annee.grid(row=4, column=1)

# Boutons Livres
cadre_btn_livres = tk.Frame(tab_livres, bg="#f0f0f0")
cadre_btn_livres.pack(pady=10)

tk.Button(cadre_btn_livres, text="Ajouter", bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_livres, text="Modifier", bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_livres, text="Supprimer", bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_livres, text="Rechercher", bg="#FF9800", fg="white", width=10).pack(side=tk.LEFT, padx=5)

# =====================================================
# =================== MEMBRES ==========================
# =====================================================
cadre_membres = tk.Frame(tab_membres, bg="#f0f0f0")
cadre_membres.pack(pady=20)

tk.Label(cadre_membres, text="Nom :", bg="#f0f0f0").grid(row=0, column=0, pady=5)
entry_nom = tk.Entry(cadre_membres, width=30)
entry_nom.grid(row=0, column=1)

tk.Label(cadre_membres, text="Prénom :", bg="#f0f0f0").grid(row=1, column=0, pady=5)
entry_prenom = tk.Entry(cadre_membres, width=30)
entry_prenom.grid(row=1, column=1)

tk.Label(cadre_membres, text="Email :", bg="#f0f0f0").grid(row=2, column=0, pady=5)
entry_email = tk.Entry(cadre_membres, width=30)
entry_email.grid(row=2, column=1)

tk.Label(cadre_membres, text="Téléphone :", bg="#f0f0f0").grid(row=3, column=0, pady=5)
entry_tel = tk.Entry(cadre_membres, width=30)
entry_tel.grid(row=3, column=1)

# Boutons Membres
cadre_btn_membres = tk.Frame(tab_membres, bg="#f0f0f0")
cadre_btn_membres.pack(pady=10)

tk.Button(cadre_btn_membres, text="Ajouter", bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_membres, text="Modifier", bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_membres, text="Supprimer", bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_membres, text="Rechercher", bg="#FF9800", fg="white", width=10).pack(side=tk.LEFT, padx=5)

# =====================================================
# =================== EMPRUNTS =========================
# =====================================================
cadre_emprunts = tk.Frame(tab_emprunts, bg="#f0f0f0")
cadre_emprunts.pack(pady=20)

tk.Label(cadre_emprunts, text="ID Membre :", bg="#f0f0f0").grid(row=0, column=0, pady=5)
entry_id_membre = tk.Entry(cadre_emprunts, width=30)
entry_id_membre.grid(row=0, column=1)

tk.Label(cadre_emprunts, text="ID Livre :", bg="#f0f0f0").grid(row=1, column=0, pady=5)
entry_id_livre = tk.Entry(cadre_emprunts, width=30)
entry_id_livre.grid(row=1, column=1)

tk.Label(cadre_emprunts, text="Date emprunt :", bg="#f0f0f0").grid(row=2, column=0, pady=5)
entry_date_emprunt = tk.Entry(cadre_emprunts, width=30)
entry_date_emprunt.grid(row=2, column=1)

tk.Label(cadre_emprunts, text="Date retour :", bg="#f0f0f0").grid(row=3, column=0, pady=5)
entry_date_retour = tk.Entry(cadre_emprunts, width=30)
entry_date_retour.grid(row=3, column=1)

# Boutons Emprunts
cadre_btn_emprunts = tk.Frame(tab_emprunts, bg="#f0f0f0")
cadre_btn_emprunts.pack(pady=10)

tk.Button(cadre_btn_emprunts, text="Ajouter", bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_emprunts, text="Modifier", bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_emprunts, text="Supprimer", bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(cadre_btn_emprunts, text="Rechercher", bg="#FF9800", fg="white", width=10).pack(side=tk.LEFT, padx=5)

# ========================
# Lancer
# ========================xcsf
def ajouter_livre():
    titre = entry_titre.get()
    auteur = entry_auteur.get()
    genre = entry_genre.get()
    isbn = entry_isbn.get()
    annee = entry_annee.get()

    sql = "INSERT INTO livres (titre, auteur, genre, isbn, annee) VALUES (%s,%s,%s,%s,%s)"
    valeurs = (titre, auteur, genre, isbn, annee)

    cursor.execute(sql, valeurs)
    conn.commit()

    print("Livre ajouté")

def supprimer_livre():
    titre = entry_titre.get()

    sql = "DELETE FROM livres WHERE titre=%s"
    cursor.execute(sql, (titre,))
    conn.commit()

    print("Livre supprimé")

def modifier_livre():
    titre = entry_titre.get()
    auteur = entry_auteur.get()

    sql = "UPDATE livres SET auteur=%s WHERE titre=%s"
    cursor.execute(sql, (auteur, titre))
    conn.commit()

    print("Livre modifié")
def rechercher_livre():
    titre = entry_titre.get()

    sql = "SELECT * FROM livres WHERE titre=%s"
    cursor.execute(sql, (titre,))

    resultats = cursor.fetchall()

    for ligne in resultats:
        print(ligne)

fenetre.mainloop()