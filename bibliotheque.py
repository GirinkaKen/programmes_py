# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:35:15 2026

@author: PC
"""



import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ========================
# Connexion MySQL
# ========================
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",                    # Change si tu as un mot de passe
        database="Bibliotheques",
        port=3306,
        use_pure=True
    )
    cursor = conn.cursor()
    print("✅ Connexion réussie !")
except Error as err:
    messagebox.showerror("Erreur de connexion", f"Impossible de se connecter :\n{err}")
    conn = None
    cursor = None

# ========================
# Fenêtre principale + Style professionnel
# ========================
root = tk.Tk()
root.title("Gestion de Bibliothèque - Professionnel")
root.geometry("1220x820")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=32)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

# Styles colorés pour les boutons
style.configure("success.TButton", background="#28a745", foreground="white")
style.configure("info.TButton", background="#17a2b8", foreground="white")
style.configure("danger.TButton", background="#dc3545", foreground="white")
style.configure("warning.TButton", background="#ffc107", foreground="black")

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
# Création d'un onglet (Formulaire → Boutons centrés → Tableau)
# ========================
def create_tab(parent, labels, tree_columns, table_name):
    main_frame = ttk.Frame(parent)
    main_frame.pack(expand=True, fill="both", padx=20, pady=15)

    # 1. Formulaire
    form_frame = ttk.LabelFrame(main_frame, text=" Formulaire ", padding=20)
    form_frame.pack(fill="x", pady=(0, 20))

    entries = []
    for i, text in enumerate(labels):
        ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=(0,15), pady=9)
        
        # Combobox pour Livre et Membre dans Emprunts
        if "Livre" in text or "Membre" in text:
            widget = ttk.Combobox(form_frame, width=47, font=("Segoe UI", 11), state="readonly")
        else:
            widget = ttk.Entry(form_frame, width=50, font=("Segoe UI", 11))
        
        widget.grid(row=i, column=1, pady=9, padx=5)
        entries.append(widget)

    # 2. Boutons centrés (au milieu)
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

    # 3. Tableau
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

# --- LIVRES ---
labels_livres = ["Titre :", "Auteur :", "Genre :", "ISBN :", "Année :"]
cols_livres = ("ID", "Titre", "Auteur", "Genre", "ISBN", "Année")
tab_livres_frame = ttk.Frame(tab_control)
entries_livres, tree_livres = create_tab(tab_livres_frame, labels_livres, cols_livres, "livres")
tab_control.add(tab_livres_frame, text="   Livres   ")

# --- MEMBRES ---
labels_membres = ["Nom :", "Prénom :", "Email :", "Téléphone :", "Adresse :", "Date Inscription (AAAA-MM-JJ) :"]
cols_membres = ("ID", "Nom", "Prénom", "Email", "Téléphone", "Adresse", "Date Inscription")
tab_membres_frame = ttk.Frame(tab_control)
entries_membres, tree_membres = create_tab(tab_membres_frame, labels_membres, cols_membres, "membres")
tab_control.add(tab_membres_frame, text="   Membres   ")

# --- EMPRUNTS ---
labels_emprunts = ["Livre :", "Membre :", "Date Emprunt (AAAA-MM-JJ) :", 
                   "Date Retour Prévue :", "Date Retour Effective :", "Statut :"]
cols_emprunts = ("ID", "ID Livre", "ID Membre", "Date Emprunt", "Date Retour Prévue", "Date Retour Effective", "Statut")
tab_emprunts_frame = ttk.Frame(tab_control)
entries_emprunts, tree_emprunts = create_tab(tab_emprunts_frame, labels_emprunts, cols_emprunts, "emprunts")
tab_control.add(tab_emprunts_frame, text="   Emprunts   ")

# ========================
# Fonctions CRUD Livres
# ========================
def ajouter_livres(entries):
    if not check_connexion(): return
    try:
        sql = "INSERT INTO livres (titre, auteur, genre, isbn, annee) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, [e.get() for e in entries])
        conn.commit()
        actualiser("livres", tree_livres)
        messagebox.showinfo("Succès", "Livre ajouté !")
        for e in entries: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_livres(entries, tree):
    if not check_connexion(): return
    try:
        selected = tree.selection()[0]
        livre_id = tree.item(selected)['values'][0]
        sql = "UPDATE livres SET titre=%s, auteur=%s, genre=%s, isbn=%s, annee=%s WHERE id=%s"
        cursor.execute(sql, [e.get() for e in entries] + [livre_id])
        conn.commit()
        actualiser("livres", tree_livres)
        messagebox.showinfo("Succès", "Livre modifié !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un livre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_livres(tree):
    if not check_connexion(): return
    if not confirm_suppression(): return
    try:
        selected = tree.selection()[0]
        livre_id = tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM livres WHERE id=%s", (livre_id,))
        conn.commit()
        actualiser("livres", tree_livres)
        messagebox.showinfo("Succès", "Livre supprimé !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un livre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rechercher_livres(entries, tree):
    if not check_connexion(): return
    query = entries[0].get().strip()
    for row in tree.get_children(): tree.delete(row)
    if query:
        cursor.execute("SELECT * FROM livres WHERE titre LIKE %s", ('%' + query + '%',))
    else:
        cursor.execute("SELECT * FROM livres")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# ========================
# Fonctions CRUD Membres
# ========================
def ajouter_membres(entries):
    if not check_connexion(): return
    try:
        sql = "INSERT INTO membres (nom, prenom, email, telephone, adresse, date_inscription) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, [e.get() or None for e in entries])
        conn.commit()
        actualiser("membres", tree_membres)
        messagebox.showinfo("Succès", "Membre ajouté !")
        for e in entries: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_membres(entries, tree):
    if not check_connexion(): return
    try:
        selected = tree.selection()[0]
        membre_id = tree.item(selected)['values'][0]
        sql = "UPDATE membres SET nom=%s, prenom=%s, email=%s, telephone=%s, adresse=%s, date_inscription=%s WHERE id=%s"
        cursor.execute(sql, [e.get() or None for e in entries] + [membre_id])
        conn.commit()
        actualiser("membres", tree_membres)
        messagebox.showinfo("Succès", "Membre modifié !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un membre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_membres(tree):
    if not check_connexion(): return
    if not confirm_suppression(): return
    try:
        selected = tree.selection()[0]
        membre_id = tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM membres WHERE id=%s", (membre_id,))
        conn.commit()
        actualiser("membres", tree_membres)
        messagebox.showinfo("Succès", "Membre supprimé !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un membre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rechercher_membres(entries, tree):
    if not check_connexion(): return
    query = entries[0].get().strip()
    for row in tree.get_children(): tree.delete(row)
    if query:
        cursor.execute("SELECT * FROM membres WHERE nom LIKE %s OR prenom LIKE %s", ('%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute("SELECT * FROM membres")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# ========================
# Fonctions CRUD Emprunts + Combobox
# ========================
def charger_listes_emprunts():
    if not check_connexion(): return
    try:
        # Livres
        cursor.execute("SELECT id, titre FROM livres ORDER BY titre")
        livres = cursor.fetchall()
        livre_list = [f"{row[0]} - {row[1]}" for row in livres]
        entries_emprunts[0]['values'] = livre_list

        # Membres
        cursor.execute("SELECT id, nom, prenom FROM membres ORDER BY nom")
        membres = cursor.fetchall()
        membre_list = [f"{row[0]} - {row[1]} {row[2]}" for row in membres]
        entries_emprunts[1]['values'] = membre_list
    except Exception as e:
        print("Erreur lors du chargement des listes :", e)

def ajouter_emprunts(entries):
    if not check_connexion(): return
    try:
        livre_str = entries[0].get()
        membre_str = entries[1].get()
        livre_id = livre_str.split(" - ")[0] if livre_str else None
        membre_id = membre_str.split(" - ")[0] if membre_str else None

        sql = """INSERT INTO emprunts (livre_id, membre_id, date_emprunt, date_retour_prevue, 
                 date_retour_effective, statut) VALUES (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (livre_id, membre_id, entries[2].get() or None, 
                             entries[3].get() or None, entries[4].get() or None, entries[5].get()))
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        messagebox.showinfo("Succès", "Emprunt ajouté !")
        for e in entries: 
            if hasattr(e, 'set'): e.set('')
            else: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_emprunts(entries, tree):
    if not check_connexion(): return
    try:
        selected = tree.selection()[0]
        emprunt_id = tree.item(selected)['values'][0]
        livre_str = entries[0].get()
        membre_str = entries[1].get()
        livre_id = livre_str.split(" - ")[0] if livre_str else None
        membre_id = membre_str.split(" - ")[0] if membre_str else None

        sql = """UPDATE emprunts SET livre_id=%s, membre_id=%s, date_emprunt=%s, 
                 date_retour_prevue=%s, date_retour_effective=%s, statut=%s WHERE id=%s"""
        cursor.execute(sql, (livre_id, membre_id, entries[2].get() or None, 
                             entries[3].get() or None, entries[4].get() or None, entries[5].get(), emprunt_id))
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        messagebox.showinfo("Succès", "Emprunt modifié !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un emprunt")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_emprunts(tree):
    if not check_connexion(): return
    if not confirm_suppression(): return
    try:
        selected = tree.selection()[0]
        emprunt_id = tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM emprunts WHERE id=%s", (emprunt_id,))
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        messagebox.showinfo("Succès", "Emprunt supprimé !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un emprunt")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rechercher_emprunts(entries, tree):
    if not check_connexion(): return
    query = entries[0].get().strip()
    for row in tree.get_children(): tree.delete(row)
    if query:
        livre_id = query.split(" - ")[0] if " - " in query else query
        cursor.execute("SELECT * FROM emprunts WHERE livre_id = %s", (livre_id,))
    else:
        cursor.execute("SELECT * FROM emprunts")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# ========================
# Lancement
# ========================
tab_control.pack(expand=True, fill="both", padx=10, pady=10)

if conn is not None:
    actualiser("livres", tree_livres)
    actualiser("membres", tree_membres)
    actualiser("emprunts", tree_emprunts)
    charger_listes_emprunts()   # Chargement des listes déroulantes

root.mainloop()

if conn is not None:
    conn.close()