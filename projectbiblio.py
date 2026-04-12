import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime, date, timedelta

# ========================
# Connexion MySQL
# ========================
try:
    conn = pymysql.connect(
        host="localhost", user="root", password="", 
        database="Bibliotheques", port=3306, charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("✅ Connexion réussie !")
except Exception as err:
    messagebox.showerror("Erreur", f"Connexion échouée :\n{err}")
    conn = None
    cursor = None

# ========================
# Fenêtre principale
# ========================
root = tk.Tk()
root.title("Gestion de la Bibliotheque")
root.geometry("1550x950")
root.configure(bg="#f1f5f9")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=34)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

style.configure("Success.TButton", background="#16a34a", foreground="white")
style.configure("Accent.TButton", background="#2563eb", foreground="white")
style.configure("Danger.TButton", background="#ef4444", foreground="white")
style.configure("Info.TButton", background="#64748b", foreground="white")

# ========================
# En-tête (Header)
# ========================
header = tk.Frame(root, bg="#1e2937", height=80)
header.pack(side=tk.TOP, fill="x")
tk.Label(header, text="Gestion de la Bibliotheque", bg="#1e2937", fg="white", 
         font=("Segoe UI", 20, "bold")).pack(side=tk.LEFT, padx=30, pady=20)

# ========================
# Sidebar (Menu Principal) - Même couleur que l'en-tête
# ========================
sidebar = tk.Frame(root, bg="#1e2937", width=280)
sidebar.pack(side=tk.LEFT, fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="Menu Principal", bg="#1e2937", fg="#e2e8f0", 
         font=("Segoe UI", 14, "bold")).pack(pady=30, padx=20, anchor="w")

def switch_tab(index):
    notebook.select(index)

menu_items = [
    ("🏠 Dashboard", 0),
    ("📖 Livres", 1),
    ("👥 Membres", 2),
    ("🔄 Emprunts", 3)
]

for text, idx in menu_items:
    btn = tk.Button(sidebar, text=text, bg="#334155", fg="white", 
                    font=("Segoe UI", 12), relief="flat", anchor="w", padx=25, pady=14,
                    command=lambda i=idx: switch_tab(i))
    btn.pack(fill="x", padx=15, pady=6)

# ========================
# Zone principale 
# ========================
# ========================
# Zone principale 
# ========================
main_area = tk.Frame(root, bg="#e5e7eb")  # gris visible
main_area.pack(side=tk.RIGHT, expand=True, fill="both")

container = tk.Frame(main_area, bg="white")
container.pack(expand=True, fill="both", padx=20, pady=20)

notebook = ttk.Notebook(container)
notebook.pack(expand=True, fill="both")

# ========================
# DASHBOARD
# ========================
dash_tab = ttk.Frame(notebook)
notebook.add(dash_tab, text="  🏠 Dashboard  ")

# Titre principal
title_frame = tk.Frame(dash_tab, bg="#f1f5f9")
title_frame.pack(fill="x", pady=(30, 10))
tk.Label(title_frame, text="Tableau de Bord", font=("Segoe UI", 28, "bold"), 
         bg="#f1f5f9", fg="#1e2937").pack()

tk.Label(title_frame, text="Aperçu général de votre bibliothèque", 
         font=("Segoe UI", 12), bg="#f1f5f9", fg="#64748b").pack()

# Frame des cartes
cards_frame = tk.Frame(dash_tab, bg="#f1f5f9")
cards_frame.pack(pady=30)

def create_stat_card(title, value, color, icon="📊"):
    # Carte avec effet moderne
    card = tk.Frame(cards_frame, bg="white", relief="flat", bd=0)
    card.pack(side=tk.LEFT, padx=18, pady=10, ipadx=30, ipady=25)
    
    # Ombre légère (effet relief)
    card.configure(highlightbackground="#e2e8f0", highlightthickness=1)
    
    # Icône
    tk.Label(card, text=icon, font=("Segoe UI", 28), bg="white").pack(pady=(10,5))
    
    # Valeur principale
    tk.Label(card, text=value, font=("Segoe UI", 42, "bold"), fg=color).pack()
    
    # Titre
    tk.Label(card, text=title, font=("Segoe UI", 12), fg="#475569", bg="white").pack(pady=5)

# Chargement des statistiques
def load_dashboard():
    if not conn: return
    try:
        cursor.execute("SELECT COUNT(*) FROM livres")
        total_livres = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM membres")
        total_membres = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM emprunts WHERE retour_effectue = 'Non' OR retour_effectue IS NULL")
        en_cours = cursor.fetchone()[0]

        today = date.today().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COUNT(*) FROM emprunts 
            WHERE (retour_effectue = 'Non' OR retour_effectue IS NULL) 
            AND date_retour < %s
        """, (today,))
        en_retard = cursor.fetchone()[0]

        # Nettoyer les anciennes cartes
        for widget in cards_frame.winfo_children():
            widget.destroy()

        # Créer les nouvelles cartes
        create_stat_card("Total Livres", str(total_livres), "#3b82f6", "📚")
        create_stat_card("Membres Inscrits", str(total_membres), "#10b981", "👥")
        create_stat_card("Emprunts en Cours", str(en_cours), "#f59e0b", "🔄")
        create_stat_card("Emprunts en Retard", str(en_retard), "#ef4444", "⚠️")

    except Exception as e:
        print("Erreur lors du chargement du dashboard:", e)

load_dashboard()

# Bouton Actualiser stylé
refresh_btn = ttk.Button(dash_tab, text="🔄 Actualiser les statistiques", 
                        style="Accent.TButton", command=load_dashboard)
refresh_btn.pack(pady=30, ipadx=20, ipady=8)

# ========================
# Fin du Dashboard
# ========================

# ========================
# Utilitaires
# ========================
def check_connexion():
    if conn is None or cursor is None:
        messagebox.showerror("Erreur", "Pas de connexion à la base de données")
        return False
    return True

def valider_champs(entries, obligatoires):
    for i, obligatoire in enumerate(obligatoires):
        if obligatoire and not entries[i].get().strip():
            messagebox.showwarning("Obligatoire", f"Le champ '{labels[i]}' est obligatoire !")
            entries[i].focus()
            return False
    return True

def actualiser(table_name, tree):
    if not check_connexion(): return
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute(f"SELECT * FROM {table_name}")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# ========================
# Fonctions Modifier et Supprimer
# ========================
def modifier_item(table_name, tree, entries, update_sql):
    if not check_connexion(): return
    try:
        selected = tree.selection()[0]
        item_id = tree.item(selected)['values'][0]
        values = [e.get().strip() for e in entries]
        cursor.execute(update_sql, values + [item_id])
        conn.commit()
        actualiser(table_name, tree)
        load_dashboard()
        messagebox.showinfo("Succès", "Modification effectuée !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_item(table_name, tree):
    if not check_connexion(): return
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élément ?", icon="warning"):
        return
    try:
        selected = tree.selection()[0]
        item_id = tree.item(selected)['values'][0]
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (item_id,))
        conn.commit()
        actualiser(table_name, tree)
        load_dashboard()
        messagebox.showinfo("Succès", "Suppression effectuée !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# ========================
# ONGLET LIVRES
# ========================
livres_tab = ttk.Frame(notebook)
notebook.add(livres_tab, text="  📖 Livres  ")

labels_livres = ["Titre :", "Auteur :", "Genre :", "ISBN :", "Année :", "Disponible :"]
cols_livres = ("id", "titre", "auteur", "genre", "isbn", "annee", "disponible")

livres_form = ttk.LabelFrame(livres_tab, text=" Formulaire Livres ", padding=15)
livres_form.pack(fill="x", pady=10, padx=10)

entries_livres = []
for i, text in enumerate(labels_livres):
    ttk.Label(livres_form, text=text).grid(row=i, column=0, sticky="e", padx=10, pady=8)
    if "Disponible" in text:
        ent = ttk.Combobox(livres_form, values=["Oui", "Non"], width=47, state="readonly")
        ent.set("Oui")
    else:
        ent = ttk.Entry(livres_form, width=50)
    ent.grid(row=i, column=1, padx=10, pady=8)
    entries_livres.append(ent)

btn_frame_l = ttk.Frame(livres_tab)
btn_frame_l.pack(pady=10)

ttk.Button(btn_frame_l, text="Ajouter", style="Success.TButton", command=lambda: ajouter_livre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_l, text="Modifier", style="Accent.TButton", command=lambda: modifier_livre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_l, text="Supprimer", style="Danger.TButton", command=lambda: supprimer_livre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_l, text="Rechercher", style="Info.TButton", command=lambda: rechercher_livre()).pack(side=tk.LEFT, padx=6)

tree_livres = ttk.Treeview(livres_tab, columns=cols_livres, show="headings")
for col in cols_livres:
    tree_livres.heading(col, text=col.capitalize())
    tree_livres.column(col, width=130)
tree_livres.pack(fill="both", expand=True, padx=10, pady=10)

def ajouter_livre():
    if not check_connexion(): return
    if not valider_champs(entries_livres, [True, True, False, False, False, False]): return
    try:
        sql = "INSERT INTO livres (titre, auteur, genre, isbn, annee, disponible) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, [e.get().strip() for e in entries_livres])
        conn.commit()
        actualiser("livres", tree_livres)
        load_dashboard()
        messagebox.showinfo("Succès", "Livre ajouté avec succès !")
        for e in entries_livres: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_livre():
    if not check_connexion(): return
    try:
        selected = tree_livres.selection()[0]
        livre_id = tree_livres.item(selected)['values'][0]
        sql = "UPDATE livres SET titre=%s, auteur=%s, genre=%s, isbn=%s, annee=%s, disponible=%s WHERE id=%s"
        cursor.execute(sql, [e.get().strip() for e in entries_livres] + [livre_id])
        conn.commit()
        actualiser("livres", tree_livres)
        load_dashboard()
        messagebox.showinfo("Succès", "Livre modifié !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un livre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_livre():
    if not check_connexion(): return
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce livre ?", icon="warning"):
        return
    try:
        selected = tree_livres.selection()[0]
        livre_id = tree_livres.item(selected)['values'][0]
        cursor.execute("SELECT COUNT(*) FROM emprunts WHERE id_livre = %s AND retour_effectue = 'Non'", (livre_id,))
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Impossible", "Ce livre est actuellement emprunté. Impossible de le supprimer.")
            return
        cursor.execute("DELETE FROM livres WHERE id = %s", (livre_id,))
        conn.commit()
        actualiser("livres", tree_livres)
        load_dashboard()
        messagebox.showinfo("Succès", "Livre supprimé !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un livre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rechercher_livre():
    query = entries_livres[0].get().strip()
    for row in tree_livres.get_children():
        tree_livres.delete(row)
    if query:
        cursor.execute("SELECT * FROM livres WHERE titre LIKE %s OR auteur LIKE %s", 
                      ('%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute("SELECT * FROM livres")
    for row in cursor.fetchall():
        tree_livres.insert("", tk.END, values=row)

# ========================
# ONGLET MEMBRES
# ========================
membres_tab = ttk.Frame(notebook)
notebook.add(membres_tab, text="  👥 Membres  ")

labels_membres = ["Nom :", "Prénom :", "Email :", "Téléphone :", "Date Inscription (AAAA-MM-JJ) :"]
cols_membres = ("id", "nom", "prenom", "email", "telephone", "date_inscription")

membres_form = ttk.LabelFrame(membres_tab, text=" Formulaire Membres ", padding=15)
membres_form.pack(fill="x", pady=10, padx=10)

entries_membres = []
for i, text in enumerate(labels_membres):
    ttk.Label(membres_form, text=text).grid(row=i, column=0, sticky="e", padx=10, pady=8)
    ent = ttk.Entry(membres_form, width=50)
    ent.grid(row=i, column=1, padx=10, pady=8)
    entries_membres.append(ent)

btn_frame_m = ttk.Frame(membres_tab)
btn_frame_m.pack(pady=10)

ttk.Button(btn_frame_m, text="Ajouter", style="Success.TButton", command=lambda: ajouter_membre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_m, text="Modifier", style="Accent.TButton", command=lambda: modifier_membre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_m, text="Supprimer", style="Danger.TButton", command=lambda: supprimer_membre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_m, text="Rechercher", style="Info.TButton", command=lambda: rechercher_membre()).pack(side=tk.LEFT, padx=6)

tree_membres = ttk.Treeview(membres_tab, columns=cols_membres, show="headings")
for col in cols_membres:
    tree_membres.heading(col, text=col.capitalize())
    tree_membres.column(col, width=140)
tree_membres.pack(fill="both", expand=True, padx=10, pady=10)

def ajouter_membre():
    if not check_connexion(): return
    if not valider_champs(entries_membres, [True, True, False, False, False]): return
    try:
        sql = "INSERT INTO membres (nom, prenom, email, telephone, date_inscription) VALUES (%s,%s,%s,%s,%s)"
        date_ins = entries_membres[4].get() or datetime.today().strftime('%Y-%m-%d')
        cursor.execute(sql, [entries_membres[0].get().strip(), entries_membres[1].get().strip(), 
                             entries_membres[2].get().strip() or None, 
                             entries_membres[3].get().strip() or None, date_ins])
        conn.commit()
        actualiser("membres", tree_membres)
        load_dashboard()
        messagebox.showinfo("Succès", "Membre ajouté !")
        for e in entries_membres: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_membre():
    if not check_connexion(): return
    try:
        selected = tree_membres.selection()[0]
        membre_id = tree_membres.item(selected)['values'][0]
        sql = "UPDATE membres SET nom=%s, prenom=%s, email=%s, telephone=%s, date_inscription=%s WHERE id=%s"
        cursor.execute(sql, [e.get().strip() for e in entries_membres] + [membre_id])
        conn.commit()
        actualiser("membres", tree_membres)
        load_dashboard()
        messagebox.showinfo("Succès", "Membre modifié !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un membre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_membre():
    if not check_connexion(): return
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce membre ?", icon="warning"):
        return
    try:
        selected = tree_membres.selection()[0]
        membre_id = tree_membres.item(selected)['values'][0]
        cursor.execute("DELETE FROM membres WHERE id = %s", (membre_id,))
        conn.commit()
        actualiser("membres", tree_membres)
        load_dashboard()
        messagebox.showinfo("Succès", "Membre supprimé !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un membre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rechercher_membre():
    query = entries_membres[0].get().strip()
    for row in tree_membres.get_children():
        tree_membres.delete(row)
    if query:
        cursor.execute("SELECT * FROM membres WHERE nom LIKE %s OR prenom LIKE %s", 
                      ('%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute("SELECT * FROM membres")
    for row in cursor.fetchall():
        tree_membres.insert("", tk.END, values=row)

# ========================
# ONGLET EMPRUNTS
# ========================
emprunts_tab = ttk.Frame(notebook)
notebook.add(emprunts_tab, text="  🔄 Emprunts  ")

labels_emprunts = ["Membre :", "Livre :", "Date Emprunt :", "Date Retour Prévue :", "Retour Effectué :"]
cols_emprunts = ("id", "id_membre", "id_livre", "date_emprunt", "date_retour", "retour_effectue")

emprunts_form = ttk.LabelFrame(emprunts_tab, text=" Formulaire Emprunts ", padding=15)
emprunts_form.pack(fill="x", pady=10, padx=10)

entries_emprunts = []
for i, text in enumerate(labels_emprunts):
    ttk.Label(emprunts_form, text=text).grid(row=i, column=0, sticky="e", padx=10, pady=8)
    if "Membre" in text or "Livre" in text:
        ent = ttk.Combobox(emprunts_form, width=47, state="readonly")
    elif "Retour Effectué" in text:
        ent = ttk.Combobox(emprunts_form, values=["Oui", "Non"], width=47, state="readonly")
        ent.set("Non")
    else:
        ent = ttk.Entry(emprunts_form, width=50)
    ent.grid(row=i, column=1, padx=10, pady=8)
    entries_emprunts.append(ent)

btn_frame_e = ttk.Frame(emprunts_tab)
btn_frame_e.pack(pady=10)

ttk.Button(btn_frame_e, text="Ajouter Emprunt", style="Success.TButton", 
           command=lambda: ajouter_emprunt()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="Retourner le Livre", style="Accent.TButton", 
           command=lambda: retourner_livre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="Modifier", style="Accent.TButton", 
           command=lambda: modifier_emprunt()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="Supprimer", style="Danger.TButton", 
           command=lambda: supprimer_emprunt()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="Rechercher", style="Info.TButton", 
           command=lambda: rechercher_emprunt()).pack(side=tk.LEFT, padx=6)

tree_emprunts = ttk.Treeview(emprunts_tab, columns=cols_emprunts, show="headings")
for col in cols_emprunts:
    tree_emprunts.heading(col, text=col.capitalize())
    tree_emprunts.column(col, width=130)
tree_emprunts.pack(fill="both", expand=True, padx=10, pady=10)

def charger_listes_emprunts():
    if not check_connexion(): return
    try:
        cursor.execute("SELECT id, nom, prenom FROM membres ORDER BY nom")
        entries_emprunts[0]['values'] = [f"{row[0]} - {row[1]} {row[2]}" for row in cursor.fetchall()]
        cursor.execute("SELECT id, titre FROM livres WHERE disponible = 'Oui' ORDER BY titre")
        entries_emprunts[1]['values'] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    except:
        pass

def ajouter_emprunt():
    if not check_connexion(): return
    if not valider_champs(entries_emprunts, [True, True, False, True, False]): return
    try:
        membre_str = entries_emprunts[0].get()
        livre_str = entries_emprunts[1].get()
        id_membre = membre_str.split(" - ")[0] if membre_str else None
        id_livre = livre_str.split(" - ")[0] if livre_str else None

        date_retour_prevue = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')

        sql = """INSERT INTO emprunts (id_membre, id_livre, date_emprunt, date_retour, retour_effectue) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_membre, id_livre, datetime.today().strftime('%Y-%m-%d'), 
                             date_retour_prevue, "Non"))
        
        cursor.execute("UPDATE livres SET disponible = 'Non' WHERE id = %s", (id_livre,))
        
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        actualiser("livres", tree_livres)
        load_dashboard()
        messagebox.showinfo("Succès", "Emprunt enregistré ! Le livre est maintenant indisponible.")
        for e in entries_emprunts: 
            if hasattr(e, 'set'): e.set('')
            else: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def retourner_livre():
    if not check_connexion(): return
    try:
        selected = tree_emprunts.selection()[0]
        emprunt_id = tree_emprunts.item(selected)['values'][0]
        id_livre = tree_emprunts.item(selected)['values'][2]

        today = datetime.today().strftime('%Y-%m-%d')
        
        cursor.execute("UPDATE emprunts SET retour_effectue = 'Oui', date_retour = %s WHERE id = %s", (today, emprunt_id))
        cursor.execute("UPDATE livres SET disponible = 'Oui' WHERE id = %s", (id_livre,))
        
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        actualiser("livres", tree_livres)
        load_dashboard()
        messagebox.showinfo("Succès", "Livre retourné avec succès !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un emprunt")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_emprunt():
    if not check_connexion(): return
    try:
        selected = tree_emprunts.selection()[0]
        emprunt_id = tree_emprunts.item(selected)['values'][0]
        sql = "UPDATE emprunts SET id_membre=%s, id_livre=%s, date_emprunt=%s, date_retour=%s, retour_effectue=%s WHERE id=%s"
        cursor.execute(sql, [e.get().strip() for e in entries_emprunts] + [emprunt_id])
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        load_dashboard()
        messagebox.showinfo("Succès", "Emprunt modifié !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un emprunt")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_emprunt():
    if not check_connexion(): return
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet emprunt ?", icon="warning"):
        return
    try:
        selected = tree_emprunts.selection()[0]
        emprunt_id = tree_emprunts.item(selected)['values'][0]
        cursor.execute("DELETE FROM emprunts WHERE id = %s", (emprunt_id,))
        conn.commit()
        actualiser("emprunts", tree_emprunts)
        load_dashboard()
        messagebox.showinfo("Succès", "Emprunt supprimé !")
    except IndexError:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un emprunt")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rechercher_emprunt():
    query = entries_emprunts[0].get().strip()
    for row in tree_emprunts.get_children():
        tree_emprunts.delete(row)
    if query:
        id_membre = query.split(" - ")[0] if " - " in query else query
        cursor.execute("SELECT * FROM emprunts WHERE id_membre = %s", (id_membre,))
    else:
        cursor.execute("SELECT * FROM emprunts")
    for row in cursor.fetchall():
        tree_emprunts.insert("", tk.END, values=row)

# ========================
# Chargement initial
# ========================
charger_listes_emprunts()
actualiser("livres", tree_livres)
actualiser("membres", tree_membres)
actualiser("emprunts", tree_emprunts)

# ========================
# Lancement
# ========================
root.mainloop()

if conn is not None:
    conn.close()