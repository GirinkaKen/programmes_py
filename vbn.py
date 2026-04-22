import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime, date, timedelta

# ============================================================
# CONFIG
# ============================================================
DB_CONFIG = dict(
    host="localhost", user="root", password="",
    database="Bibliotheques", port=3306, charset="utf8mb4",
    autocommit=False,
    cursorclass=pymysql.cursors.DictCursor,   # retours en dict
)

LOAN_DAYS = 14   # durée par défaut d'un emprunt

# ============================================================
# COULEURS & THÈME
# ============================================================
C = dict(
    bg        = "#f1f5f9",
    sidebar   = "#0f172a",
    sidebar_h = "#1e293b",
    header    = "#0f172a",
    accent    = "#3b82f6",
    accent_d  = "#2563eb",
    success   = "#16a34a",
    danger    = "#dc2626",
    warning   = "#d97706",
    white     = "#ffffff",
    gray50    = "#f8fafc",
    gray100   = "#f1f5f9",
    gray200   = "#e2e8f0",
    gray400   = "#94a3b8",
    gray600   = "#475569",
    gray800   = "#1e293b",
    text      = "#0f172a",
    muted     = "#64748b",
    red_bg    = "#fef2f2",
    red_text  = "#991b1b",
)

FONTS = dict(
    h1  = ("Segoe UI", 22, "bold"),
    h2  = ("Segoe UI", 14, "bold"),
    h3  = ("Segoe UI", 11, "bold"),
    body= ("Segoe UI", 11),
    sm  = ("Segoe UI", 10),
    nav = ("Segoe UI", 11),
)

# ============================================================
# COUCHE BASE DE DONNÉES
# ============================================================
class DB:
    def __init__(self):
        self.conn   = None
        self.cursor = None
        self._connect()

    def _connect(self):
        try:
            self.conn   = pymysql.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connexion", f"Impossible de joindre la base :\n{e}")

    def ok(self):
        """Vérifie la connexion et tente une reconnexion si nécessaire."""
        try:
            self.conn.ping(reconnect=True)
            return True
        except Exception:
            messagebox.showerror("Base de données", "Connexion perdue.")
            return False

    def query(self, sql, params=()):
        if not self.ok(): return []
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Requête", str(e))
            return []

    def execute(self, sql, params=()):
        """Exécute et commit. Lève l'exception pour que l'appelant gère."""
        self.cursor.execute(sql, params)
        self.conn.commit()

    def count(self, sql, params=()):
        rows = self.query(sql, params)
        if rows:
            return list(rows[0].values())[0]
        return 0

    def close(self):
        if self.conn:
            self.conn.close()

db = DB()

# ============================================================
# HELPERS UI
# ============================================================
def flat_button(parent, text, color, command, width=None):
    kw = dict(
        text=text, command=command,
        bg=color, fg=C["white"],
        font=FONTS["body"],
        relief="flat", bd=0,
        padx=14, pady=8,
        cursor="hand2",
        activebackground=color,
        activeforeground=C["white"],
    )
    if width:
        kw["width"] = width
    btn = tk.Button(parent, **kw)
    return btn

def entry_field(parent, row, label, col_offset=0, width=28, readonly=False):
    ttk.Label(parent, text=label).grid(
        row=row, column=col_offset*2, sticky="w", padx=(0,8), pady=4)
    if readonly:
        ent = ttk.Entry(parent, width=width, state="readonly")
    else:
        ent = ttk.Entry(parent, width=width)
    ent.grid(row=row, column=col_offset*2+1, pady=4, sticky="w")
    return ent

def combo_field(parent, row, label, values=(), width=27, col_offset=0):
    ttk.Label(parent, text=label).grid(
        row=row, column=col_offset*2, sticky="w", padx=(0,8), pady=4)
    cb = ttk.Combobox(parent, values=values, width=width, state="readonly")
    ent = cb
    ent.grid(row=row, column=col_offset*2+1, pady=4, sticky="w")
    return ent

def section_label(parent, text):
    tk.Label(parent, text=text, font=FONTS["h2"],
             bg=C["white"], fg=C["gray800"]).pack(
        anchor="w", padx=20, pady=(18, 6))
    tk.Frame(parent, bg=C["gray200"], height=1).pack(fill="x", padx=20)

def toast(root, message, color=C["success"]):
    """Notification non-bloquante en bas de fenêtre."""
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    root.update_idletasks()
    x = root.winfo_x() + root.winfo_width()//2 - 180
    y = root.winfo_y() + root.winfo_height() - 80
    t.geometry(f"360x44+{x}+{y}")
    t.configure(bg=color)
    tk.Label(t, text=message, bg=color, fg=C["white"],
             font=FONTS["body"]).pack(expand=True)
    t.after(2200, t.destroy)

def confirm(message):
    return messagebox.askyesno("Confirmation", message, icon="warning")

def validate_date(s):
    """Renvoie True si la chaîne est une date valide AAAA-MM-JJ."""
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def set_entry(widget, value):
    """Remplit un Entry ou Combobox sans erreur."""
    try:
        state = widget["state"]
        if state == "readonly":
            widget.configure(state="normal")
        widget.delete(0, tk.END)
        widget.insert(0, str(value) if value else "")
        if state == "readonly":
            widget.configure(state="readonly")
    except Exception:
        pass

def clear_entries(widgets):
    for w in widgets:
        set_entry(w, "")

# ============================================================
# TREEVIEW HELPER
# ============================================================
def make_tree(parent, columns, col_widths=None):
    style = ttk.Style()
    style.configure("Treeview",
        rowheight=28, font=FONTS["body"],
        background=C["white"], fieldbackground=C["white"],
        foreground=C["text"])
    style.configure("Treeview.Heading",
        font=FONTS["h3"], background=C["gray100"],
        foreground=C["gray600"])
    style.map("Treeview", background=[("selected", C["accent"])],
              foreground=[("selected", C["white"])])

    frame = tk.Frame(parent, bg=C["white"])
    frame.pack(fill="both", expand=True, padx=14, pady=(8,14))

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.configure(command=tree.yview)
    hsb.configure(command=tree.xview)

    for i, col in enumerate(columns):
        w = (col_widths[i] if col_widths else 130)
        tree.heading(col, text=col.replace("_", " ").capitalize(),
                     command=lambda c=col: sort_tree(tree, c))
        tree.column(col, width=w, anchor="center", minwidth=60)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    tree.tag_configure("overdue", background=C["red_bg"], foreground=C["red_text"])
    tree.tag_configure("even",    background=C["gray50"])
    return tree

_sort_state = {}
def sort_tree(tree, col):
    items = [(tree.set(k, col), k) for k in tree.get_children()]
    desc  = _sort_state.get((id(tree), col), False)
    items.sort(key=lambda x: x[0].lower() if isinstance(x[0], str) else x[0],
               reverse=desc)
    for idx, (_, k) in enumerate(items):
        tree.move(k, "", idx)
    _sort_state[(id(tree), col)] = not desc

def reload_tree(tree, rows, tag_fn=None):
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        values = list(row.values())
        tag = tag_fn(row) if tag_fn else ("even" if i % 2 == 0 else "")
        tree.insert("", tk.END, values=values,
                    tags=(tag,) if tag else ())

# ============================================================
# FENÊTRE PRINCIPALE
# ============================================================
root = tk.Tk()
root.title("Bibliothèque Pro")
root.geometry("1440x860")
root.minsize(1100, 640)
root.configure(bg=C["bg"])

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook",        background=C["bg"],    borderwidth=0)
style.configure("TNotebook.Tab",    font=FONTS["h3"],      padding=[14,7])
style.configure("TLabelframe",      background=C["white"], borderwidth=1)
style.configure("TLabelframe.Label",font=FONTS["h3"],      background=C["white"],
                foreground=C["muted"])
style.configure("TCombobox",        arrowsize=14)
style.configure("TEntry",           padding=4)

# ============================================================
# HEADER
# ============================================================
header = tk.Frame(root, bg=C["header"], height=60)
header.pack(side="top", fill="x")
header.pack_propagate(False)

hbox = tk.Frame(header, bg=C["header"])
hbox.pack(fill="both", expand=True, padx=24)

tk.Label(hbox, text="📚  Gestion Bibliothèque",
         bg=C["header"], fg=C["white"], font=FONTS["h1"]).pack(side="left", pady=12)
tk.Label(hbox, text="Système de gestion intelligent",
         bg=C["header"], fg=C["gray400"], font=FONTS["sm"]).pack(side="left", padx=18)
tk.Label(hbox, text=f"👤 Admin   ·   {datetime.now().strftime('%d %B %Y')}",
         bg=C["header"], fg=C["gray400"], font=FONTS["sm"]).pack(side="right")

# ============================================================
# SIDEBAR
# ============================================================
sidebar = tk.Frame(root, bg=C["sidebar"], width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="NAVIGATION", bg=C["sidebar"], fg=C["gray400"],
         font=("Segoe UI", 9, "bold")).pack(pady=(24,4), padx=16, anchor="w")
tk.Frame(sidebar, bg=C["sidebar_h"], height=1).pack(fill="x", padx=16, pady=6)

menu_btns = []
PAGES = [("🏠  Dashboard", 0), ("📖  Livres", 1), ("👥  Membres", 2), ("🔄  Emprunts", 3)]

notebook = None   # sera créé plus bas

def switch(index):
    notebook.select(index)
    for i, b in enumerate(menu_btns):
        b.configure(bg=C["accent"] if i == index else C["sidebar_h"])

for label, idx in PAGES:
    b = tk.Label(sidebar, text=label, bg=C["sidebar_h"], fg=C["white"],
                 font=FONTS["nav"], anchor="w", padx=16, pady=11, cursor="hand2")
    b.pack(fill="x", padx=12, pady=3)
    b.bind("<Button-1>", lambda e, i=idx: switch(i))
    b.bind("<Enter>",    lambda e: e.widget.configure(bg=C["gray600"]) if e.widget.cget("bg") != C["accent"] else None)
    b.bind("<Leave>",    lambda e: e.widget.configure(bg=C["sidebar_h"]) if e.widget.cget("bg") == C["gray600"] else None)
    menu_btns.append(b)

# ============================================================
# MAIN AREA + NOTEBOOK
# ============================================================
main = tk.Frame(root, bg=C["bg"])
main.pack(side="right", fill="both", expand=True)

wrap = tk.Frame(main, bg=C["white"], bd=0)
wrap.pack(fill="both", expand=True, padx=18, pady=18)

notebook = ttk.Notebook(wrap)
notebook.pack(fill="both", expand=True)
notebook.bind("<<NotebookTabChanged>>",
              lambda e: switch(notebook.index(notebook.select())))

# ============================================================
# PAGE : DASHBOARD
# ============================================================
dash_tab = tk.Frame(notebook, bg=C["gray100"])
notebook.add(dash_tab, text="  🏠 Dashboard  ")

dash_header = tk.Frame(dash_tab, bg=C["gray100"])
dash_header.pack(fill="x", padx=28, pady=(22,8))
tk.Label(dash_header, text="Tableau de bord", font=FONTS["h1"],
         bg=C["gray100"], fg=C["text"]).pack(anchor="w")
tk.Label(dash_header, text="Vue d'ensemble des activités",
         font=FONTS["body"], bg=C["gray100"], fg=C["muted"]).pack(anchor="w", pady=(4,0))
tk.Frame(dash_tab, bg=C["gray200"], height=1).pack(fill="x", padx=28, pady=8)

cards_zone = tk.Frame(dash_tab, bg=C["gray100"])
cards_zone.pack(padx=24, pady=12, fill="x")

STAT_DEFS = [
    ("📚", "Livres",          "#3b82f6"),
    ("👥", "Membres",         "#10b981"),
    ("🔄", "Emprunts actifs", "#f59e0b"),
    ("⚠️",  "En retard",      "#ef4444"),
]
stat_labels = []

def _make_stat_card(parent, icon, title, color):
    card = tk.Frame(parent, bg=C["white"], highlightbackground=C["gray200"],
                    highlightthickness=1)
    card.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    inner = tk.Frame(card, bg=C["white"])
    inner.pack(fill="both", expand=True, padx=20, pady=18)

    top = tk.Frame(inner, bg=C["white"])
    top.pack(fill="x")
    tk.Label(top, text=icon, font=("Segoe UI Emoji", 16), bg=C["white"]).pack(side="left")
    tk.Label(top, text=title, font=FONTS["sm"], fg=C["muted"], bg=C["white"]).pack(side="left", padx=8)

    val = tk.Label(inner, text="—", font=("Segoe UI", 30, "bold"),
                   fg=color, bg=C["white"])
    val.pack(anchor="w", pady=(12,0))
    return val

for icon, title, color in STAT_DEFS:
    stat_labels.append(_make_stat_card(cards_zone, icon, title, color))

def load_dashboard():
    if not db.ok(): return
    today = date.today().strftime("%Y-%m-%d")
    stats = [
        db.count("SELECT COUNT(*) AS n FROM livres"),
        db.count("SELECT COUNT(*) AS n FROM membres"),
        db.count("SELECT COUNT(*) AS n FROM emprunts WHERE retour_effectue='Non'"),
        db.count("""SELECT COUNT(*) AS n FROM emprunts
                    WHERE retour_effectue='Non' AND date_retour < %s""", (today,)),
    ]
    for lbl, val in zip(stat_labels, stats):
        lbl.configure(text=str(val))

flat_button(dash_tab, "↻  Actualiser", C["accent"], load_dashboard).pack(pady=12)

# ============================================================
# COMPOSANT GÉNÉRIQUE : BARRE DE RECHERCHE
# ============================================================
def search_bar(parent, placeholder, on_search, on_reset):
    bar = tk.Frame(parent, bg=C["white"])
    bar.pack(fill="x", padx=14, pady=(10,4))

    sv = tk.StringVar()
    sv.trace_add("write", lambda *_: on_search(sv.get()) if sv.get() else on_reset())

    entry = ttk.Entry(bar, textvariable=sv, width=42)
    entry.insert(0, placeholder)
    entry.configure(foreground=C["muted"])

    def on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground=C["text"])

    def on_focus_out(e):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(foreground=C["muted"])

    entry.bind("<FocusIn>",  on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    entry.pack(side="left", padx=(0,8), ipady=5)

    flat_button(bar, "Rechercher", C["accent"],    lambda: on_search(sv.get() if sv.get() != placeholder else "")).pack(side="left", padx=4)
    flat_button(bar, "↻ Tout",     C["gray400"],   on_reset).pack(side="left")
    return entry

# ============================================================
# PAGE : LIVRES
# ============================================================
livres_tab = tk.Frame(notebook, bg=C["white"])
notebook.add(livres_tab, text="  📖 Livres  ")

cols_livres   = ("id","titre","auteur","genre","isbn","annee","disponible")
widths_livres = (40,  220,    160,     120,    110,   70,     90)

pane_l = tk.Frame(livres_tab, bg=C["white"], width=340)
pane_l.pack(side="left", fill="y", padx=(14,0), pady=14)
pane_l.pack_propagate(False)

pane_r = tk.Frame(livres_tab, bg=C["white"])
pane_r.pack(side="right", fill="both", expand=True, padx=14, pady=14)

section_label(pane_l, "Fiche livre")

form_l = tk.Frame(pane_l, bg=C["white"])
form_l.pack(fill="x", padx=18, pady=8)

labels_l = ["Titre *", "Auteur *", "Genre", "ISBN", "Année"]
entries_livres = [entry_field(form_l, i, lbl) for i, lbl in enumerate(labels_l)]

ttk.Label(form_l, text="Disponible").grid(row=5, column=0, sticky="w", padx=(0,8), pady=4)
cb_dispo = ttk.Combobox(form_l, values=["Oui","Non"], state="readonly", width=27)
cb_dispo.set("Oui")
cb_dispo.grid(row=5, column=1, pady=4, sticky="w")
entries_livres.append(cb_dispo)

# Boutons formulaire
btn_zone_l = tk.Frame(pane_l, bg=C["white"])
btn_zone_l.pack(fill="x", padx=18, pady=8)

def _fill_livre_form(event):
    sel = tree_livres.selection()
    if not sel: return
    vals = tree_livres.item(sel[0])["values"]
    for i, e in enumerate(entries_livres):
        set_entry(e, vals[i+1] if i+1 < len(vals) else "")

def ajouter_livre():
    titre, auteur = entries_livres[0].get().strip(), entries_livres[1].get().strip()
    if not titre or not auteur:
        messagebox.showwarning("Champs requis", "Titre et Auteur sont obligatoires.")
        return
    try:
        db.execute(
            "INSERT INTO livres (titre,auteur,genre,isbn,annee,disponible) VALUES (%s,%s,%s,%s,%s,%s)",
            [e.get().strip() for e in entries_livres])
        _refresh_livres(); load_dashboard()
        toast(root, "✔  Livre ajouté")
        clear_entries(entries_livres); cb_dispo.set("Oui")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_livre():
    sel = tree_livres.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez d'abord un livre dans la liste."); return
    lid = tree_livres.item(sel[0])["values"][0]
    try:
        db.execute(
            "UPDATE livres SET titre=%s,auteur=%s,genre=%s,isbn=%s,annee=%s,disponible=%s WHERE id=%s",
            [e.get().strip() for e in entries_livres] + [lid])
        _refresh_livres(); load_dashboard()
        toast(root, "✔  Livre modifié", C["accent_d"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_livre():
    sel = tree_livres.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez d'abord un livre."); return
    lid = tree_livres.item(sel[0])["values"][0]
    if not confirm("Supprimer ce livre ? Les emprunts liés seront aussi supprimés."):
        return
    try:
        db.execute("DELETE FROM emprunts WHERE id_livre=%s", (lid,))
        db.execute("DELETE FROM livres WHERE id=%s", (lid,))
        _refresh_livres(); _refresh_emprunts(); load_dashboard()
        clear_entries(entries_livres)
        toast(root, "✔  Livre supprimé", C["danger"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def _refresh_livres(query=""):
    if query:
        rows = db.query(
            "SELECT * FROM livres WHERE titre LIKE %s OR auteur LIKE %s OR isbn LIKE %s",
            (f"%{query}%",)*3)
    else:
        rows = db.query("SELECT * FROM livres ORDER BY titre")
    reload_tree(tree_livres, rows)

for text, color, cmd in [
    ("➕  Ajouter",   C["success"], ajouter_livre),
    ("✏️  Modifier",  C["accent"],  modifier_livre),
    ("🗑  Supprimer", C["danger"],  supprimer_livre),
]:
    flat_button(btn_zone_l, text, color, cmd).pack(fill="x", pady=4)

# Barre de recherche livres
search_bar(pane_r, "Rechercher par titre, auteur, ISBN…",
           _refresh_livres, lambda: _refresh_livres())

tree_livres = make_tree(pane_r, cols_livres, widths_livres)
tree_livres.bind("<<TreeviewSelect>>", _fill_livre_form)

# ============================================================
# PAGE : MEMBRES
# ============================================================
membres_tab = tk.Frame(notebook, bg=C["white"])
notebook.add(membres_tab, text="  👥 Membres  ")

cols_membres   = ("id","nom","prenom","email","telephone","date_inscription")
widths_membres = (40, 120,   120,     200,    120,        120)

pane_lm = tk.Frame(membres_tab, bg=C["white"], width=340)
pane_lm.pack(side="left", fill="y", padx=(14,0), pady=14)
pane_lm.pack_propagate(False)

pane_rm = tk.Frame(membres_tab, bg=C["white"])
pane_rm.pack(side="right", fill="both", expand=True, padx=14, pady=14)

section_label(pane_lm, "Fiche membre")

form_m = tk.Frame(pane_lm, bg=C["white"])
form_m.pack(fill="x", padx=18, pady=8)

labels_m = ["Nom *", "Prénom *", "Email", "Téléphone", "Date inscription\n(AAAA-MM-JJ)"]
entries_membres = [entry_field(form_m, i, lbl) for i, lbl in enumerate(labels_m)]

btn_zone_m = tk.Frame(pane_lm, bg=C["white"])
btn_zone_m.pack(fill="x", padx=18, pady=8)

def _fill_membre_form(event):
    sel = tree_membres.selection()
    if not sel: return
    vals = tree_membres.item(sel[0])["values"]
    for i, e in enumerate(entries_membres):
        set_entry(e, vals[i+1] if i+1 < len(vals) else "")

def ajouter_membre():
    nom, prenom = entries_membres[0].get().strip(), entries_membres[1].get().strip()
    if not nom or not prenom:
        messagebox.showwarning("Champs requis", "Nom et Prénom sont obligatoires."); return
    date_ins = entries_membres[4].get().strip() or date.today().strftime("%Y-%m-%d")
    if not validate_date(date_ins):
        messagebox.showwarning("Date", "Format de date invalide. Utilisez AAAA-MM-JJ."); return
    try:
        db.execute(
            "INSERT INTO membres (nom,prenom,email,telephone,date_inscription) VALUES (%s,%s,%s,%s,%s)",
            [nom, prenom,
             entries_membres[2].get().strip() or None,
             entries_membres[3].get().strip() or None,
             date_ins])
        _refresh_membres(); load_dashboard()
        toast(root, "✔  Membre ajouté")
        clear_entries(entries_membres)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_membre():
    sel = tree_membres.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un membre."); return
    mid = tree_membres.item(sel[0])["values"][0]
    date_ins = entries_membres[4].get().strip()
    if date_ins and not validate_date(date_ins):
        messagebox.showwarning("Date", "Format de date invalide. Utilisez AAAA-MM-JJ."); return
    try:
        db.execute(
            "UPDATE membres SET nom=%s,prenom=%s,email=%s,telephone=%s,date_inscription=%s WHERE id=%s",
            [e.get().strip() for e in entries_membres] + [mid])
        _refresh_membres(); load_dashboard()
        toast(root, "✔  Membre modifié", C["accent_d"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_membre():
    sel = tree_membres.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un membre."); return
    mid = tree_membres.item(sel[0])["values"][0]
    if not confirm("Supprimer ce membre ? Ses emprunts seront aussi supprimés."):
        return
    try:
        # Libérer les livres empruntés avant suppression
        emprunts = db.query("SELECT id_livre FROM emprunts WHERE id_membre=%s AND retour_effectue='Non'", (mid,))
        for e in emprunts:
            db.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (e["id_livre"],))
        db.execute("DELETE FROM emprunts WHERE id_membre=%s", (mid,))
        db.execute("DELETE FROM membres WHERE id=%s", (mid,))
        _refresh_membres(); _refresh_livres(); _refresh_emprunts(); load_dashboard()
        clear_entries(entries_membres)
        toast(root, "✔  Membre supprimé", C["danger"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def _refresh_membres(query=""):
    if query:
        rows = db.query(
            "SELECT * FROM membres WHERE nom LIKE %s OR prenom LIKE %s OR email LIKE %s",
            (f"%{query}%",)*3)
    else:
        rows = db.query("SELECT * FROM membres ORDER BY nom, prenom")
    reload_tree(tree_membres, rows)

for text, color, cmd in [
    ("➕  Ajouter",   C["success"], ajouter_membre),
    ("✏️  Modifier",  C["accent"],  modifier_membre),
    ("🗑  Supprimer", C["danger"],  supprimer_membre),
]:
    flat_button(btn_zone_m, text, color, cmd).pack(fill="x", pady=4)

search_bar(pane_rm, "Rechercher par nom, prénom, email…",
           _refresh_membres, lambda: _refresh_membres())

tree_membres = make_tree(pane_rm, cols_membres, widths_membres)
tree_membres.bind("<<TreeviewSelect>>", _fill_membre_form)

# ============================================================
# PAGE : EMPRUNTS
# ============================================================
emprunts_tab = tk.Frame(notebook, bg=C["white"])
notebook.add(emprunts_tab, text="  🔄 Emprunts  ")

cols_emprunts   = ("id","id_membre","id_livre","date_emprunt","date_retour","retour_effectue")
widths_emprunts = (40,  100,        90,         120,           120,          120)

pane_le = tk.Frame(emprunts_tab, bg=C["white"], width=340)
pane_le.pack(side="left", fill="y", padx=(14,0), pady=14)
pane_le.pack_propagate(False)

pane_re = tk.Frame(emprunts_tab, bg=C["white"])
pane_re.pack(side="right", fill="both", expand=True, padx=14, pady=14)

section_label(pane_le, "Fiche emprunt")

form_e = tk.Frame(pane_le, bg=C["white"])
form_e.pack(fill="x", padx=18, pady=8)

ttk.Label(form_e, text="Membre *").grid(row=0, column=0, sticky="w", padx=(0,8), pady=4)
cb_membre = ttk.Combobox(form_e, width=27, state="readonly")
cb_membre.grid(row=0, column=1, pady=4, sticky="w")

ttk.Label(form_e, text="Livre *").grid(row=1, column=0, sticky="w", padx=(0,8), pady=4)
cb_livre = ttk.Combobox(form_e, width=27, state="readonly")
cb_livre.grid(row=1, column=1, pady=4, sticky="w")

ttk.Label(form_e, text="Retour effectué").grid(row=2, column=0, sticky="w", padx=(0,8), pady=4)
cb_retour = ttk.Combobox(form_e, values=["Oui","Non"], state="readonly", width=27)
cb_retour.set("Non")
cb_retour.grid(row=2, column=1, pady=4, sticky="w")

# Dates auto (affichage lecture seule)
e_date_emprunt = entry_field(form_e, 3, "Date emprunt", readonly=True)
e_date_retour  = entry_field(form_e, 4, "Date retour prévu", readonly=True)

def _refresh_combo_emprunts():
    membres = db.query("SELECT id,nom,prenom FROM membres ORDER BY nom")
    cb_membre["values"] = [f"{r['id']} — {r['nom']} {r['prenom']}" for r in membres]
    livres = db.query("SELECT id,titre FROM livres WHERE disponible='Oui' ORDER BY titre")
    cb_livre["values"] = [f"{r['id']} — {r['titre']}" for r in livres]

def _id_from_cb(cb):
    v = cb.get()
    return v.split(" — ")[0] if " — " in v else None

def _fill_emprunt_form(event):
    sel = tree_emprunts.selection()
    if not sel: return
    vals = tree_emprunts.item(sel[0])["values"]
    # vals: id, id_membre, id_livre, date_emprunt, date_retour, retour_effectue
    # Recompose les labels combobox
    rows_m = db.query("SELECT nom,prenom FROM membres WHERE id=%s", (vals[1],))
    rows_l = db.query("SELECT titre FROM livres WHERE id=%s", (vals[2],))
    nm = f"{vals[1]} — {rows_m[0]['nom']} {rows_m[0]['prenom']}" if rows_m else str(vals[1])
    nl = f"{vals[2]} — {rows_l[0]['titre']}" if rows_l else str(vals[2])
    cb_membre.set(nm); cb_livre.set(nl)
    cb_retour.set(vals[5] if vals[5] else "Non")
    set_entry(e_date_emprunt, vals[3])
    set_entry(e_date_retour,  vals[4])

def ajouter_emprunt():
    id_m = _id_from_cb(cb_membre)
    id_l = _id_from_cb(cb_livre)
    if not id_m or not id_l:
        messagebox.showwarning("Champs requis", "Sélectionnez un membre et un livre."); return
    today      = date.today().strftime("%Y-%m-%d")
    due        = (date.today() + timedelta(days=LOAN_DAYS)).strftime("%Y-%m-%d")
    try:
        db.execute(
            "INSERT INTO emprunts (id_membre,id_livre,date_emprunt,date_retour,retour_effectue) VALUES (%s,%s,%s,%s,'Non')",
            (id_m, id_l, today, due))
        db.execute("UPDATE livres SET disponible='Non' WHERE id=%s", (id_l,))
        _refresh_emprunts(); _refresh_livres(); _refresh_combo_emprunts(); load_dashboard()
        set_entry(e_date_emprunt, today); set_entry(e_date_retour, due)
        toast(root, f"✔  Emprunt enregistré — retour le {due}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def retourner_livre():
    sel = tree_emprunts.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un emprunt."); return
    vals = tree_emprunts.item(sel[0])["values"]
    eid, id_l, statut = vals[0], vals[2], vals[5]
    if statut == "Oui":
        messagebox.showinfo("Info", "Ce livre a déjà été retourné."); return
    today = date.today().strftime("%Y-%m-%d")
    try:
        db.execute("UPDATE emprunts SET retour_effectue='Oui', date_retour=%s WHERE id=%s", (today, eid))
        db.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (id_l,))
        _refresh_emprunts(); _refresh_livres(); _refresh_combo_emprunts(); load_dashboard()
        toast(root, "✔  Livre retourné", C["success"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def modifier_emprunt():
    sel = tree_emprunts.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un emprunt."); return
    eid = tree_emprunts.item(sel[0])["values"][0]
    id_m = _id_from_cb(cb_membre)
    id_l = _id_from_cb(cb_livre)
    if not id_m or not id_l:
        messagebox.showwarning("Champs requis", "Membre et livre sont requis."); return
    de = e_date_emprunt.get().strip()
    dr = e_date_retour.get().strip()
    if de and not validate_date(de):
        messagebox.showwarning("Date", "Date emprunt invalide (AAAA-MM-JJ)."); return
    if dr and not validate_date(dr):
        messagebox.showwarning("Date", "Date retour invalide (AAAA-MM-JJ)."); return
    try:
        db.execute(
            "UPDATE emprunts SET id_membre=%s,id_livre=%s,date_emprunt=%s,date_retour=%s,retour_effectue=%s WHERE id=%s",
            (id_m, id_l,
             de or date.today().strftime("%Y-%m-%d"),
             dr or (date.today()+timedelta(LOAN_DAYS)).strftime("%Y-%m-%d"),
             cb_retour.get(), eid))
        _refresh_emprunts(); load_dashboard()
        toast(root, "✔  Emprunt modifié", C["accent_d"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_emprunt():
    sel = tree_emprunts.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un emprunt."); return
    vals = tree_emprunts.item(sel[0])["values"]
    eid, id_l, statut = vals[0], vals[2], vals[5]
    if not confirm("Supprimer cet emprunt ?"):
        return
    try:
        if statut == "Non":
            db.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (id_l,))
        db.execute("DELETE FROM emprunts WHERE id=%s", (eid,))
        _refresh_emprunts(); _refresh_livres(); _refresh_combo_emprunts(); load_dashboard()
        toast(root, "✔  Emprunt supprimé", C["danger"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def _retard_tag(row):
    if row.get("retour_effectue") == "Non":
        dr = str(row.get("date_retour",""))
        if dr and dr < date.today().strftime("%Y-%m-%d"):
            return "overdue"
    return ""

def _refresh_emprunts(query=""):
    if query:
        rows = db.query(
            """SELECT e.* FROM emprunts e
               JOIN membres m ON e.id_membre=m.id
               WHERE m.nom LIKE %s OR m.prenom LIKE %s""",
            (f"%{query}%",)*2)
    else:
        rows = db.query("SELECT * FROM emprunts ORDER BY date_retour")
    reload_tree(tree_emprunts, rows, tag_fn=_retard_tag)

btn_zone_e = tk.Frame(pane_le, bg=C["white"])
btn_zone_e.pack(fill="x", padx=18, pady=8)

for text, color, cmd in [
    ("➕  Emprunter",  C["success"],  ajouter_emprunt),
    ("📥  Retourner",  "#7c3aed",     retourner_livre),
    ("✏️  Modifier",   C["accent"],   modifier_emprunt),
    ("🗑  Supprimer",  C["danger"],   supprimer_emprunt),
]:
    flat_button(btn_zone_e, text, color, cmd).pack(fill="x", pady=4)

# Légende retard
leg = tk.Frame(pane_le, bg=C["white"])
leg.pack(fill="x", padx=18, pady=(4,0))
tk.Frame(leg, bg=C["red_bg"], width=14, height=14,
         highlightbackground=C["red_text"], highlightthickness=1).pack(side="left")
tk.Label(leg, text="  Emprunt en retard", font=FONTS["sm"],
         fg=C["muted"], bg=C["white"]).pack(side="left")

search_bar(pane_re, "Rechercher par nom du membre…",
           _refresh_emprunts, lambda: _refresh_emprunts())

tree_emprunts = make_tree(pane_re, cols_emprunts, widths_emprunts)
tree_emprunts.bind("<<TreeviewSelect>>", _fill_emprunt_form)

# ============================================================
# CHARGEMENT INITIAL
# ============================================================
_refresh_livres()
_refresh_membres()
_refresh_emprunts()
_refresh_combo_emprunts()
load_dashboard()
switch(0)

# ============================================================
# LANCEMENT
# ============================================================
root.mainloop()
db.close()