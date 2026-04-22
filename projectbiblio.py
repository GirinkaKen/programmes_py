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

def show_login():
    login_win = tk.Tk()
    login_win.title("Connexion")
    login_win.geometry("400x300")
    login_win.configure(bg="#111827")
    login_win.resizable(False, False)

    tk.Label(login_win, text="🔐 Connexion",
             font=("Segoe UI", 20, "bold"),
             bg="#111827", fg="white").pack(pady=20)

    frame = tk.Frame(login_win, bg="#111827")
    frame.pack(pady=10)

    tk.Label(frame, text="Username", bg="#111827", fg="white").grid(row=0, column=0, sticky="w")
    entry_user = ttk.Entry(frame, width=30)
    entry_user.grid(row=1, column=0, pady=5)

    tk.Label(frame, text="Password", bg="#111827", fg="white").grid(row=2, column=0, sticky="w")
    entry_pass = ttk.Entry(frame, width=30, show="*")
    entry_pass.grid(row=3, column=0, pady=5)

    def login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires")
            return

        cursor.execute("""
            SELECT * FROM utilisateurs
            WHERE username=%s AND password=SHA2(%s,256)
        """, (username, password))

        if cursor.fetchone():
            login_win.destroy()
            open_main_app()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    tk.Button(login_win, text="Se connecter",
              command=login,
              bg="#2563eb", fg="white",
              font=("Segoe UI", 11, "bold"),
              relief="flat").pack(pady=20)

    login_win.mainloop()

# ========================
# Fenêtre principale
# ========================
root = tk.Tk()
root.title("📚 Gestion de Bibliothèque")
root.geometry("1500x900")
root.minsize(1200, 700)
root.configure(bg="#e5e7eb")  # gris moderne (fond global)

# ========================
# STYLE GLOBAL
# ========================
style = ttk.Style()
style.theme_use("clam")

# Couleurs globales
PRIMARY = "#2563eb"   # bleu
SUCCESS = "#16a34a"   # vert
DANGER  = "#dc2626"   # rouge
GRAY    = "#6b7280"   # gris texte
BG      = "#f9fafb"   # fond clair
WHITE   = "#ffffff"

# ========================
# STYLE BOUTONS PRO MAX
# ========================

PRIMARY = "#2563eb"   # Bleu
SUCCESS = "#16a34a"   # Vert
DANGER  = "#dc2626"   # Rouge
WARNING = "#f59e0b"   # Orange
INFO    = "#6b7280"   # Gris
PURPLE  = "#7c3aed"   # Violet
WHITE   = "#ffffff"

style.configure("TButton",
                font=("Segoe UI", 10, "bold"),
                padding=10,
                borderwidth=0,
                focusthickness=0)

# ===== Ajouter (VERT)
style.configure("Success.TButton",
                background=SUCCESS,
                foreground=WHITE)
style.map("Success.TButton",
          background=[("active", "#15803d")])

# ===== Modifier (BLEU)
style.configure("Primary.TButton",
                background=PRIMARY,
                foreground=WHITE)
style.map("Primary.TButton",
          background=[("active", "#1d4ed8")])

# ===== Supprimer (ROUGE)
style.configure("Danger.TButton",
                background=DANGER,
                foreground=WHITE)
style.map("Danger.TButton",
          background=[("active", "#b91c1c")])

# ===== Rechercher (GRIS)
style.configure("Info.TButton",
                background=INFO,
                foreground=WHITE)
style.map("Info.TButton",
          background=[("active", "#4b5563")])

# ===== Retour (VIOLET)
style.configure("Purple.TButton",
                background=PURPLE,
                foreground=WHITE)
style.map("Purple.TButton",
          background=[("active", "#6d28d9")])

# ========================
# NOTEBOOK (ONGLETS)
# ========================
style.configure("TNotebook",
                background=BG,
                borderwidth=0)

style.configure("TNotebook.Tab",
                font=("Segoe UI", 10, "bold"),
                padding=[15, 8],
                background="#e2e8f0")

style.map("TNotebook.Tab",
          background=[("selected", WHITE)],
          foreground=[("selected", PRIMARY)])
# ========================
# HEADER PRO
# ========================
header = tk.Frame(root, bg="#111827", height=70)  # gris très foncé premium
header.pack(side=tk.TOP, fill="x")

header_container = tk.Frame(header, bg="#111827")
header_container.pack(fill="both", expand=True, padx=25)

# Logo + titre
logo_frame = tk.Frame(header_container, bg="#111827")
logo_frame.pack(side=tk.LEFT)

tk.Label(logo_frame, text="📚", bg="#111827", fg="#3b82f6",
         font=("Segoe UI Emoji", 20)).pack(side=tk.LEFT, padx=(0,10))

tk.Label(logo_frame, text="GESTION BIBLIOTHÈQUE",
         bg="#111827", fg="white",
         font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)

# Sous-titre
tk.Label(header_container, text="Système de gestion intelligent",
         bg="#111827", fg="#9ca3af",
         font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=20)

# Partie droite (profil / date)
right_frame = tk.Frame(header_container, bg="#111827")
right_frame.pack(side=tk.RIGHT)

from datetime import datetime
tk.Label(right_frame,
         text=datetime.now().strftime("%d %B %Y"),
         bg="#111827", fg="#9ca3af",
         font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=10)

tk.Label(right_frame,
         text="👤 Admin",
         bg="#111827", fg="white",
         font=("Segoe UI", 10, "bold")).pack(side=tk.RIGHT, padx=10)

# ========================
# SIDEBAR PRO
# ========================
sidebar = tk.Frame(root, bg="#1f2937", width=260)  # gris pro
sidebar.pack(side=tk.LEFT, fill="y")
sidebar.pack_propagate(False)

# Titre menu
tk.Label(sidebar, text="NAVIGATION",
         bg="#1f2937", fg="#9ca3af",
         font=("Segoe UI", 10, "bold")).pack(pady=(25,10), padx=20, anchor="w")

# Ligne séparation
tk.Frame(sidebar, bg="#374151", height=1).pack(fill="x", padx=20, pady=10)

# Fonction switch
def switch_tab(index):
    notebook.select(index)
    highlight_button(index)

# Gestion sélection active
active_btn = None
def highlight_button(index):
    global active_btn
    for i, btn in enumerate(menu_buttons):
        if i == index:
            btn.configure(bg="#2563eb")  # bleu actif
        else:
            btn.configure(bg="#374151")

# Hover effect
def on_enter(e):
    e.widget['bg'] = "#4b5563"

def on_leave(e):
    if e.widget != active_btn:
        e.widget['bg'] = "#374151"

# Menu items
menu_items = [
    ("🏠  Dashboard", 0),
    ("📖  Livres", 1),
    ("👥  Membres", 2),
    ("🔄  Emprunts", 3)
]

menu_buttons = []

for text, idx in menu_items:
    btn = tk.Label(sidebar,
                   text=text,
                   bg="#374151",
                   fg="white",
                   font=("Segoe UI", 11),
                   anchor="w",
                   padx=20,
                   pady=12,
                   cursor="hand2")
    
    btn.pack(fill="x", padx=15, pady=5)

    btn.bind("<Button-1>", lambda e, i=idx: switch_tab(i))
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    menu_buttons.append(btn)

# Activer premier bouton
highlight_button(0)
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
# DASHBOARD PREMIUM
# ========================
dash_tab = tk.Frame(notebook, bg="#f3f4f6")
notebook.add(dash_tab, text="  🏠 Dashboard  ")

# ========================
# HEADER DASHBOARD
# ========================
top_section = tk.Frame(dash_tab, bg="#f3f4f6")
top_section.pack(fill="x", padx=30, pady=(25, 10))

tk.Label(top_section,
         text="Tableau de bord",
         font=("Segoe UI", 26, "bold"),
         bg="#f3f4f6",
         fg="#111827").pack(anchor="w")

tk.Label(top_section,
         text="Suivi global des activités de la bibliothèque",
         font=("Segoe UI", 11),
         bg="#f3f4f6",
         fg="#6b7280").pack(anchor="w", pady=(5, 0))

# ========================
# LIGNE SEPARATION
# ========================
tk.Frame(dash_tab, bg="#e5e7eb", height=1).pack(fill="x", padx=30, pady=10)

# ========================
# CARDS CONTAINER
# ========================
cards_container = tk.Frame(dash_tab, bg="#f3f4f6")
cards_container.pack(padx=20, pady=20, fill="x")

# ========================
# CARD COMPONENT
# ========================
def create_stat_card(parent, title, value, color, icon):
    card = tk.Frame(parent, bg="white", bd=0)
    card.pack(side=tk.LEFT, expand=True, fill="both", padx=10, pady=10)

    # effet bordure légère
    card.configure(highlightbackground="#e5e7eb", highlightthickness=1)

    inner = tk.Frame(card, bg="white")
    inner.pack(padx=20, pady=20, fill="both", expand=True)

    # ligne top (icone + titre)
    top = tk.Frame(inner, bg="white")
    top.pack(fill="x")

    tk.Label(top, text=icon,
             font=("Segoe UI Emoji", 20),
             bg="white").pack(side=tk.LEFT)

    tk.Label(top, text=title,
             font=("Segoe UI", 11),
             fg="#6b7280",
             bg="white").pack(side=tk.LEFT, padx=10)

    # valeur principale
    tk.Label(inner,
             text=value,
             font=("Segoe UI", 32, "bold"),
             fg=color,
             bg="white").pack(anchor="w", pady=(15, 5))

# ========================
# CHARGEMENT DATA
# ========================
def load_dashboard():
    if not conn:
        return
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

        # clear cards
        for widget in cards_container.winfo_children():
            widget.destroy()

        # GRID propre (2 lignes)
        row1 = tk.Frame(cards_container, bg="#f3f4f6")
        row1.pack(fill="x")

        row2 = tk.Frame(cards_container, bg="#f3f4f6")
        row2.pack(fill="x")

        create_stat_card(row1, "Livres", total_livres, "#3b82f6", "📚")
        create_stat_card(row1, "Membres", total_membres, "#10b981", "👥")

        create_stat_card(row2, "Emprunts actifs", en_cours, "#f59e0b", "🔄")
        create_stat_card(row2, "Retards", en_retard, "#ef4444", "⚠️")

    except Exception as e:
        print("Erreur dashboard:", e)

load_dashboard()

# ========================
# ACTIONS DASHBOARD
# ========================
actions_frame = tk.Frame(dash_tab, bg="#f3f4f6")
actions_frame.pack(pady=20)

ttk.Button(actions_frame,
           text="🔄 Actualiser",
           style="Primary.TButton",
           command=load_dashboard).pack(ipadx=20, ipady=8)

# ========================
# Utilitaires
# ========================
def check_connexion():
    if conn is None or cursor is None:
        messagebox.showerror("Erreur", "Pas de connexion à la base de données")
        return False
    return True

def valider_champs(entries, obligatoires, labels):
    for i, obligatoire in enumerate(obligatoires):
        valeur = entries[i].get().strip()

        if obligatoire and valeur == "":
            messagebox.showwarning(
                "Champ obligatoire",
                f"Le champ '{labels[i]}' est obligatoire !"
            )
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
# FONCTIONS LIVRES (OBLIGATOIRE AVANT UI)
# ========================

def ajouter_livre():
    if not check_connexion():
        return

    if not valider_champs(
        entries_livres,
        [True, True, True, True, True, True],
        labels_livres
    ):
        return

    try:
        titre = entries_livres[0].get().strip()
        auteur = entries_livres[1].get().strip()
        isbn = entries_livres[3].get().strip()

        # 🔍 Vérifier doublon
        cursor.execute("""
            SELECT COUNT(*) FROM livres
            WHERE (titre=%s AND auteur=%s) OR isbn=%s
        """, (titre, auteur, isbn if isbn else None))

        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Doublon", "Ce livre existe déjà !")
            return

        sql = """INSERT INTO livres
                 (titre, auteur, genre, isbn, annee, disponible)
                 VALUES (%s,%s,%s,%s,%s,%s)"""

        valeurs = [e.get().strip() if e.get().strip() != "" else None for e in entries_livres]

        cursor.execute(sql, valeurs)
        conn.commit()

        actualiser("livres", tree_livres)
        load_dashboard()

        messagebox.showinfo("Succès", "Livre ajouté avec succès !")

        for e in entries_livres:
            if hasattr(e, "set"):
                e.set("")
            else:
                e.delete(0, tk.END)

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
        messagebox.showwarning("Sélection", "Sélectionnez un livre")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


def supprimer_livre():
    if not check_connexion(): return
    if not messagebox.askyesno("Confirmation", "Supprimer ce livre ?"):
        return
    try:
        selected = tree_livres.selection()[0]
        livre_id = tree_livres.item(selected)['values'][0]
        cursor.execute("DELETE FROM livres WHERE id=%s", (livre_id,))
        conn.commit()
        actualiser("livres", tree_livres)
        load_dashboard()
        messagebox.showinfo("Succès", "Livre supprimé !")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


def rechercher_livre():
    query = entries_livres[0].get().strip()
    tree_livres.delete(*tree_livres.get_children())

    if query:
        cursor.execute("SELECT * FROM livres WHERE titre LIKE %s OR auteur LIKE %s",
                      ('%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute("SELECT * FROM livres")

    for row in cursor.fetchall():
        tree_livres.insert("", tk.END, values=row)
# ========================
# ONGLET LIVRES (PRO UX CLEAN)
# ========================
livres_tab = ttk.Frame(notebook)
notebook.add(livres_tab, text="📖 Livres")

# ========================
# CONTAINER PRINCIPAL
# ========================
main_livres = tk.Frame(livres_tab, bg="#f8fafc")
main_livres.pack(fill="both", expand=True)

# ========================
# LEFT PANEL (FORM + ACTIONS)
# ========================
left_panel = tk.Frame(main_livres, bg="#ffffff", width=380)
left_panel.pack(side="left", fill="y", padx=10, pady=10)
left_panel.pack_propagate(False)

tk.Label(
    left_panel,
    text="Gestion des Livres",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    fg="#111827"
).pack(pady=15)

# ========================
# FORMULAIRE
# ========================
form = ttk.LabelFrame(left_panel, text=" Nouveau Livre ", padding=15)
form.pack(fill="x", padx=10, pady=10)

labels_livres = ["Titre", "Auteur", "Genre", "ISBN", "Année", "Disponible"]
entries_livres = []

for i, label in enumerate(labels_livres):
    ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=5)

    if label == "Disponible":
        ent = ttk.Combobox(form, values=["Oui", "Non"], state="readonly", width=25)
        ent.set("Oui")
    else:
        ent = ttk.Entry(form, width=28)

    ent.grid(row=i, column=1, pady=5, padx=5)
    entries_livres.append(ent)

# ========================
# ACTIONS BUTTONS (PRO SIZE)
# ========================
btn_frame = tk.Frame(left_panel, bg="white")
btn_frame.pack(fill="x", pady=15)

def style_btn(parent, text, color, cmd):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        height=2,
        cursor="hand2"
    )

style_btn(btn_frame, "➕ Ajouter", "#16a34a", ajouter_livre).pack(fill="x", pady=5)
style_btn(btn_frame, "✏️ Modifier", "#2563eb", modifier_livre).pack(fill="x", pady=5)
style_btn(btn_frame, "🗑 Supprimer", "#dc2626", supprimer_livre).pack(fill="x", pady=5)

# ========================
# RIGHT PANEL (SEARCH + TABLE)
# ========================
right_panel = tk.Frame(main_livres, bg="#f8fafc")
right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ========================
# SEARCH BAR (TOP)
# ========================
top_bar = tk.Frame(right_panel, bg="white")
top_bar.pack(fill="x", pady=10)

search_entry = ttk.Entry(top_bar, width=40)
search_entry.pack(side="left", padx=10, pady=10)

def rechercher_livre():
    query = search_entry.get().strip()
    tree_livres.delete(*tree_livres.get_children())

    if query:
        cursor.execute("""
            SELECT * FROM livres 
            WHERE titre LIKE %s OR auteur LIKE %s
        """, ('%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute("SELECT * FROM livres")

    for row in cursor.fetchall():
        tree_livres.insert("", "end", values=row)

tk.Button(
    top_bar,
    text="🔍 Rechercher",
    command=rechercher_livre,
    bg="#2563eb",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
).pack(side="left", padx=5)

tk.Button(
    top_bar,
    text="↻ Refresh",
    command=lambda: actualiser("livres", tree_livres),
    bg="#6b7280",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
).pack(side="left")

# ========================
# TABLE (PRO STYLE)
# ========================
table_frame = tk.Frame(right_panel, bg="white")
table_frame.pack(fill="both", expand=True)

cols_livres = ("id", "titre", "auteur", "genre", "isbn", "annee", "disponible")

tree_livres = ttk.Treeview(table_frame, columns=cols_livres, show="headings", height=18)

for col in cols_livres:
    tree_livres.heading(col, text=col.capitalize())
    tree_livres.column(col, width=120, anchor="center")

tree_livres.pack(fill="both", expand=True, padx=10, pady=10)

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

ttk.Button(btn_frame_m, text="➕ Ajouter", style="Success.TButton", command =lambda: ajouter_membre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_m, text="✏️ Modifier", style="Primary.TButton", command =lambda: modifier_membre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_m, text="🗑 Supprimer", style="Danger.TButton", command =lambda: supprimer_membre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_m, text="🔍 Rechercher", style="Info.TButton", command =lambda: rechercher_membre()).pack(side=tk.LEFT, padx=6)
for btn in btn_frame_m.winfo_children():
    btn.configure(cursor="hand2")

tree_membres = ttk.Treeview(membres_tab, columns=cols_membres, show="headings")
for col in cols_membres:
    tree_membres.heading(col, text=col.capitalize())
    tree_membres.column(col, width=140)
tree_membres.pack(fill="both", expand=True, padx=10, pady=10)

def ajouter_membre():
    if not check_connexion():
        return

    if not valider_champs(
        entries_membres,
        [True, True, True, True, True],
        labels_membres
    ):
        return

    try:
        nom = entries_membres[0].get().strip()
        prenom = entries_membres[1].get().strip()
        email = entries_membres[2].get().strip()
        telephone = entries_membres[3].get().strip()
        date_ins = entries_membres[4].get().strip()

        # 🔍 Vérifier doublon email
        cursor.execute(
            "SELECT COUNT(*) FROM membres WHERE email=%s",
            (email,)
        )
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Doublon", "Email déjà utilisé !")
            return

        # ✅ INSERT SANS AUCUN None
        sql = """INSERT INTO membres
                 (nom, prenom, email, telephone, date_inscription)
                 VALUES (%s,%s,%s,%s,%s)"""

        cursor.execute(sql, (nom, prenom, email, telephone, date_ins))

        conn.commit()

        actualiser("membres", tree_membres)
        load_dashboard()

        messagebox.showinfo("Succès", "Membre ajouté avec succès !")

        # ✅ Nettoyage propre
        for e in entries_membres:
            e.delete(0, tk.END)

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

ttk.Button(btn_frame_e, text="➕ Emprunter", style="Success.TButton", command =lambda: ajouter_emprunt()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="📥 Retourner", style="Purple.TButton", command =lambda: retourner_livre()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="✏️ Modifier", style="Primary.TButton", command =lambda: modifier_emprunt()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="🗑 Supprimer", style="Danger.TButton", command =lambda: supprimer_emprunt()).pack(side=tk.LEFT, padx=6)
ttk.Button(btn_frame_e, text="🔍 Rechercher", style="Info.TButton", command =lambda: rechercher_emprunt()).pack(side=tk.LEFT, padx=6)
for btn in btn_frame_e.winfo_children():
    btn.configure(cursor="hand2")

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
    if not check_connexion():
        return

    # ✅ Tous les champs obligatoires
    if not valider_champs(
        entries_emprunts,
        [True, True, True, True, True],
        labels_emprunts
    ):
        return

    try:
        membre_str = entries_emprunts[0].get().strip()
        livre_str = entries_emprunts[1].get().strip()
        date_emprunt = entries_emprunts[2].get().strip()
        date_retour = entries_emprunts[3].get().strip()
        retour = entries_emprunts[4].get().strip()

        # 🔍 Extraction IDs
        id_membre = membre_str.split(" - ")[0]
        id_livre = livre_str.split(" - ")[0]

        # 🔍 Vérifier si déjà emprunté
        cursor.execute("""
            SELECT COUNT(*) FROM emprunts
            WHERE id_livre=%s AND retour_effectue='Non'
        """, (id_livre,))

        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Indisponible", "Ce livre est déjà emprunté !")
            return

        # ❌ Vérifier cohérence dates
        if date_retour < date_emprunt:
            messagebox.showwarning("Erreur", "Date retour invalide !")
            return

        # ✅ INSERT propre
        sql = """INSERT INTO emprunts
                 (id_membre, id_livre, date_emprunt, date_retour, retour_effectue)
                 VALUES (%s,%s,%s,%s,%s)"""

        cursor.execute(sql, (
            id_membre,
            id_livre,
            date_emprunt,
            date_retour,
            retour
        ))

        # 🔄 Mise à jour disponibilité
        if retour == "Non":
            cursor.execute("UPDATE livres SET disponible='Non' WHERE id=%s", (id_livre,))
        else:
            cursor.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (id_livre,))

        conn.commit()

        actualiser("emprunts", tree_emprunts)
        actualiser("livres", tree_livres)
        load_dashboard()

        messagebox.showinfo("Succès", "Emprunt enregistré avec succès !")

        # nettoyage
        for e in entries_emprunts:
            if hasattr(e, "set"):
                e.set("")
            else:
                e.delete(0, tk.END)

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