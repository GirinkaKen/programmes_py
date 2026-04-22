import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime, date, timedelta
import re

# ============================================================
# CONNEXION BASE DE DONNÉES
# ============================================================
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

# ============================================================
# PALETTE & CONSTANTES
# ============================================================
C = {
    "bg_dark":    "#0d1117",
    "bg_card":    "#161b22",
    "bg_input":   "#21262d",
    "border":     "#30363d",
    "blue":       "#2563eb",
    "blue_hover": "#1d4ed8",
    "green":      "#16a34a",
    "green_h":    "#15803d",
    "red":        "#dc2626",
    "red_h":      "#b91c1c",
    "amber":      "#d97706",
    "purple":     "#7c3aed",
    "text":       "#e6edf3",
    "muted":      "#8b949e",
    "white":      "#ffffff",
    "sidebar":    "#0d1117",
    "header":     "#161b22",
    "accent":     "#58a6ff",
    "row_even":   "#161b22",
    "row_odd":    "#1c2128",
    "row_sel":    "#1f4068",
}

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_HEADER = ("Segoe UI", 12, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Consolas", 10)

# ============================================================
# WIDGETS PERSONNALISÉS
# ============================================================
class DarkEntry(tk.Entry):
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent,
            bg=C["bg_input"], fg=C["text"],
            insertbackground=C["accent"],
            relief="flat", bd=0,
            font=FONT_LABEL,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["blue"],
            **kwargs)
        self.placeholder = placeholder
        self._has_placeholder = False
        if placeholder:
            self._show_placeholder()
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._restore_placeholder)

    def _show_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg=C["muted"])
        self._has_placeholder = True

    def _clear_placeholder(self, e=None):
        if self._has_placeholder:
            self.delete(0, tk.END)
            self.config(fg=C["text"])
            self._has_placeholder = False

    def _restore_placeholder(self, e=None):
        if not self.get() and self.placeholder:
            self._show_placeholder()

    def get_value(self):
        return "" if self._has_placeholder else self.get().strip()


class DarkCombo(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


class IconButton(tk.Button):
    def __init__(self, parent, text, color, hover_color, command=None, **kwargs):
        super().__init__(parent,
            text=text, command=command,
            bg=color, fg=C["white"],
            activebackground=hover_color,
            activeforeground=C["white"],
            font=FONT_BTN, relief="flat",
            bd=0, cursor="hand2",
            padx=14, pady=8,
            **kwargs)
        self._color = color
        self._hover = hover_color
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._color))


class StatCard(tk.Frame):
    def __init__(self, parent, title, value, color, icon, subtitle=""):
        super().__init__(parent, bg=C["bg_card"],
                         highlightbackground=C["border"],
                         highlightthickness=1)
        self.config(width=200, height=120)
        self.pack_propagate(False)

        inner = tk.Frame(self, bg=C["bg_card"])
        inner.pack(fill="both", expand=True, padx=18, pady=14)

        top = tk.Frame(inner, bg=C["bg_card"])
        top.pack(fill="x")

        tk.Label(top, text=icon, font=("Segoe UI Emoji", 18),
                 bg=C["bg_card"], fg=color).pack(side="left")
        tk.Label(top, text=title, font=FONT_SMALL,
                 bg=C["bg_card"], fg=C["muted"]).pack(side="left", padx=8)

        self.value_label = tk.Label(inner, text=str(value),
                                    font=("Segoe UI", 28, "bold"),
                                    bg=C["bg_card"], fg=color)
        self.value_label.pack(anchor="w", pady=(8, 0))

        if subtitle:
            tk.Label(inner, text=subtitle, font=FONT_SMALL,
                     bg=C["bg_card"], fg=C["muted"]).pack(anchor="w")

    def update_value(self, val):
        self.value_label.config(text=str(val))


# ============================================================
# ÉCRAN DE CONNEXION DB
# ============================================================


# ============================================================
# ÉCRAN DE LOGIN
# ============================================================
def show_login(on_success):
    win = tk.Toplevel() if False else tk.Tk()
    win.title("Connexion — Bibliothèque")
    win.state("zoomed")
    win.configure(bg=C["bg_dark"])

    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)

    # ── GAUCHE ──
    left = tk.Frame(win, bg="#0f1a2e")
    left.grid(row=0, column=0, sticky="nsew")
    left.grid_rowconfigure(0, weight=1)
    left.grid_columnconfigure(0, weight=1)

    brand = tk.Frame(left, bg="#0f1a2e")
    brand.grid(row=0, column=0)

    tk.Label(brand, text="📚", font=("Segoe UI Emoji", 64),
             bg="#0f1a2e", fg=C["accent"]).pack(pady=(0, 10))
    tk.Label(brand, text="BIBLIOTHÈQUE",
             font=("Segoe UI", 28, "bold"), bg="#0f1a2e", fg=C["white"]).pack()
    tk.Label(brand, text="Système de gestion intelligent",
             font=("Segoe UI", 12), bg="#0f1a2e", fg=C["muted"]).pack(pady=8)

    # séparateur décoratif
    sep = tk.Frame(brand, bg=C["blue"], height=3, width=60)
    sep.pack(pady=15)

    features = ["✅  Gestion des livres & stocks",
                "✅  Suivi des membres",
                "✅  Emprunts & retours",
                "✅  Alertes de retard"]
    for f in features:
        tk.Label(brand, text=f, font=FONT_LABEL, bg="#0f1a2e", fg="#93c5fd").pack(anchor="w", pady=2)

    # ── DROITE ──
    right = tk.Frame(win, bg=C["bg_dark"])
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_rowconfigure(0, weight=1)
    right.grid_columnconfigure(0, weight=1)

    form_outer = tk.Frame(right, bg=C["bg_dark"])
    form_outer.grid(row=0, column=0)

    tk.Label(form_outer, text="Connexion",
             font=FONT_TITLE, bg=C["bg_dark"], fg=C["white"]).pack(anchor="w", pady=(0, 6))
    tk.Label(form_outer, text="Entrez vos identifiants pour accéder au système",
             font=FONT_SMALL, bg=C["bg_dark"], fg=C["muted"]).pack(anchor="w", pady=(0, 25))

    def make_field(label, placeholder, show=None):
        tk.Label(form_outer, text=label, font=FONT_SMALL,
                 bg=C["bg_dark"], fg=C["muted"]).pack(anchor="w")
        e = DarkEntry(form_outer, width=38, placeholder=placeholder)
        if show:
            e.config(show=show)
        e.pack(fill="x", pady=(4, 14), ipady=8)
        return e

    entry_user = make_field("Nom d'utilisateur", "ex: admin")
    entry_pass = make_field("Mot de passe", "••••••••", show="*")

    err_var = tk.StringVar()
    tk.Label(form_outer, textvariable=err_var, font=FONT_SMALL,
             bg=C["bg_dark"], fg=C["red"]).pack(anchor="w")

    def do_login(event=None):
        username = entry_user.get_value()
        password = entry_pass.get_value()
        if not username or not password:
            err_var.set("⚠  Tous les champs sont requis")
            return
        try:
            cursor.execute(
                "SELECT id, username FROM utilisateurs WHERE username=%s AND password=SHA2(%s,256)",
                (username, password)
            )
            row = cursor.fetchone()
            if row:
                win.destroy()
                on_success(row[1])  # passe le nom d'utilisateur
            else:
                err_var.set("❌  Identifiants incorrects")
        except Exception as e:
            err_var.set(f"Erreur DB: {e}")

    btn = IconButton(form_outer, "  Se connecter →  ", C["blue"], C["blue_hover"],
                     command=do_login)
    btn.pack(fill="x", pady=10, ipady=4)
    win.bind("<Return>", do_login)

    tk.Label(form_outer, text="Appuyez sur Entrée pour vous connecter",
             font=FONT_SMALL, bg=C["bg_dark"], fg=C["muted"]).pack(pady=5)

    win.mainloop()


# ============================================================
# APPLICATION PRINCIPALE
# ============================================================
def open_main_app(username="Admin"):
    root = tk.Tk()
    root.title("📚 Gestion de Bibliothèque")
    root.state("zoomed")
    root.configure(bg=C["bg_dark"])
    root.minsize(1100, 650)

    # ── STYLE ttk ──
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=C["bg_card"], fieldbackground=C["bg_card"],
                    foreground=C["text"], rowheight=32,
                    font=FONT_LABEL, borderwidth=0)
    style.configure("Treeview.Heading",
                    background=C["bg_dark"], foreground=C["accent"],
                    font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat")
    style.map("Treeview", background=[("selected", C["row_sel"])],
              foreground=[("selected", C["white"])])
    style.configure("TCombobox",
                    fieldbackground=C["bg_input"], background=C["bg_input"],
                    foreground=C["text"], arrowcolor=C["accent"], borderwidth=0)
    style.map("TCombobox", fieldbackground=[("readonly", C["bg_input"])],
              foreground=[("readonly", C["text"])])
    style.configure("TLabelframe",
                    background=C["bg_card"], bordercolor=C["border"],
                    labelanchor="nw")
    style.configure("TLabelframe.Label",
                    background=C["bg_card"], foreground=C["accent"],
                    font=FONT_HEADER)
    style.configure("TScrollbar", background=C["border"],
                    troughcolor=C["bg_dark"], arrowcolor=C["muted"])

    # ── LAYOUT PRINCIPAL ──
    # Header
    header = tk.Frame(root, bg=C["header"], height=60)
    header.pack(fill="x")
    header.pack_propagate(False)

    h_inner = tk.Frame(header, bg=C["header"])
    h_inner.pack(fill="both", expand=True, padx=20, pady=10)

    logo_f = tk.Frame(h_inner, bg=C["header"])
    logo_f.pack(side="left")
    tk.Label(logo_f, text="📚", font=("Segoe UI Emoji", 18),
             bg=C["header"], fg=C["accent"]).pack(side="left", padx=(0, 8))
    tk.Label(logo_f, text="BIBLIOTHÈQUE",
             font=("Segoe UI", 14, "bold"), bg=C["header"], fg=C["white"]).pack(side="left")
    tk.Label(logo_f, text=" — Système de gestion",
             font=FONT_LABEL, bg=C["header"], fg=C["muted"]).pack(side="left")

    h_right = tk.Frame(h_inner, bg=C["header"])
    h_right.pack(side="right")

    clock_label = tk.Label(h_right, font=FONT_SMALL, bg=C["header"], fg=C["muted"])
    clock_label.pack(side="right", padx=15)

    def update_clock():
        clock_label.config(text=datetime.now().strftime("🕐  %d %B %Y  |  %H:%M:%S"))
        root.after(1000, update_clock)
    update_clock()

    tk.Label(h_right, text=f"👤 {username}",
             font=FONT_LABEL, bg=C["header"], fg=C["accent"]).pack(side="right", padx=10)

    def logout():
        if messagebox.askyesno("Déconnexion", "Voulez-vous vous déconnecter ?"):
            root.destroy()
            show_login(open_main_app)

    IconButton(h_right, "Déconnexion", C["bg_input"], C["border"],
               command=logout).pack(side="right", padx=5)

    # Body
    body = tk.Frame(root, bg=C["bg_dark"])
    body.pack(fill="both", expand=True)

    # Sidebar
    sidebar = tk.Frame(body, bg=C["sidebar"], width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="NAVIGATION", font=("Segoe UI", 9, "bold"),
             bg=C["sidebar"], fg=C["muted"]).pack(pady=(20, 5), padx=20, anchor="w")
    tk.Frame(sidebar, bg=C["border"], height=1).pack(fill="x", padx=15, pady=5)

    # Zone principale
    main_zone = tk.Frame(body, bg=C["bg_dark"])
    main_zone.pack(side="right", fill="both", expand=True)

    # Notebook caché (contrôlé via sidebar)
    notebook = ttk.Notebook(main_zone)
    notebook.pack(fill="both", expand=True, padx=15, pady=15)
    # Cacher les onglets visuels (on utilise la sidebar)
    style.configure("TNotebook", background=C["bg_dark"], borderwidth=0,
                    tabmargins=0)
    style.layout("TNotebook.Tab", [])  # Supprime visuellement les onglets

    # ── SIDEBAR BUTTONS ──
    current_tab = [0]
    sidebar_btns = []

    menu_items = [
        ("🏠", "Dashboard", 0),
        ("📖", "Livres", 1),
        ("👥", "Membres", 2),
        ("🔄", "Emprunts", 3),
        ("⚠️", "Retards", 4),
        ("📊", "Statistiques", 5),
    ]

    def switch_tab(i):
        notebook.select(i)
        current_tab[0] = i
        for j, btn in enumerate(sidebar_btns):
            if j == i:
                btn.config(bg=C["blue"], fg=C["white"])
            else:
                btn.config(bg=C["sidebar"], fg=C["muted"])

    for icon, label, idx in menu_items:
        f = tk.Frame(sidebar, bg=C["sidebar"], cursor="hand2")
        f.pack(fill="x", pady=2, padx=10)
        btn = tk.Label(f, text=f"  {icon}  {label}",
                       font=FONT_LABEL, bg=C["sidebar"], fg=C["muted"],
                       anchor="w", padx=8, pady=10, cursor="hand2")
        btn.pack(fill="x")

        def on_click(e, i=idx):
            switch_tab(i)
        def on_enter(e):
            if e.widget.cget("bg") != C["blue"]:
                e.widget.config(bg=C["bg_input"])
        def on_leave(e):
            if e.widget.cget("bg") != C["blue"]:
                e.widget.config(bg=C["sidebar"])

        btn.bind("<Button-1>", on_click)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        sidebar_btns.append(btn)

    tk.Frame(sidebar, bg=C["border"], height=1).pack(fill="x", padx=15, pady=10)

    # Version en bas
    tk.Label(sidebar, text="v2.0 — 2025",
             font=FONT_SMALL, bg=C["sidebar"], fg=C["muted"]).pack(side="bottom", pady=15)

    # ============================================================
    # UTILITAIRES COMMUNS
    # ============================================================
    def check_conn():
        if conn is None:
            messagebox.showerror("Erreur", "Pas de connexion à la base de données")
            return False
        return True

    def refresh_tree(tree, query, params=()):
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        tree.tag_configure("even", background=C["row_even"])
        tree.tag_configure("odd", background=C["row_odd"])

    def add_scrollbars(parent, tree):
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

    def section_header(parent, title, subtitle=""):
        f = tk.Frame(parent, bg=C["bg_dark"])
        f.pack(fill="x", padx=5, pady=(10, 5))
        tk.Label(f, text=title, font=("Segoe UI", 18, "bold"),
                 bg=C["bg_dark"], fg=C["white"]).pack(anchor="w")
        if subtitle:
            tk.Label(f, text=subtitle, font=FONT_SMALL,
                     bg=C["bg_dark"], fg=C["muted"]).pack(anchor="w", pady=(2, 0))
        tk.Frame(f, bg=C["border"], height=1).pack(fill="x", pady=8)

    def validate_date(d):
        try:
            datetime.strptime(d, "%Y-%m-%d")
            return True
        except:
            return False

    def validate_email(e):
        return re.match(r"[^@]+@[^@]+\.[^@]+", e) is not None

    # ============================================================
    # TAB 0 — DASHBOARD
    # ============================================================
    dash = tk.Frame(notebook, bg=C["bg_dark"])
    notebook.add(dash)

    section_header(dash, "Tableau de bord", "Vue globale de l'activité")

    stat_cards = {}
    cards_frame = tk.Frame(dash, bg=C["bg_dark"])
    cards_frame.pack(fill="x", padx=5, pady=5)

    card_defs = [
        ("livres",   "📚", "Livres", C["accent"],   "Total dans le catalogue"),
        ("membres",  "👥", "Membres", C["green"],   "Membres enregistrés"),
        ("emprunts", "🔄", "Emprunts actifs", C["amber"], "En cours actuellement"),
        ("retards",  "⚠️", "En retard", C["red"],  "À relancer"),
    ]
    for key, icon, title, color, sub in card_defs:
        card = StatCard(cards_frame, title, "—", color, icon, sub)
        card.pack(side="left", expand=True, fill="both", padx=8, pady=8)
        stat_cards[key] = card

    # Tableau des emprunts récents
    recent_frame = tk.Frame(dash, bg=C["bg_card"],
                            highlightbackground=C["border"], highlightthickness=1)
    recent_frame.pack(fill="both", expand=True, padx=5, pady=10)

    tk.Label(recent_frame, text="Emprunts récents",
             font=FONT_HEADER, bg=C["bg_card"], fg=C["accent"]).pack(anchor="w", padx=15, pady=10)

    cols_recent = ("Membre", "Livre", "Emprunté le", "Retour prévu", "Statut")
    tree_recent = ttk.Treeview(recent_frame, columns=cols_recent, show="headings", height=8)
    for col in cols_recent:
        tree_recent.heading(col, text=col)
        tree_recent.column(col, width=160, anchor="center")
    add_scrollbars(recent_frame, tree_recent)
    tree_recent.tag_configure("retard", foreground=C["red"])
    tree_recent.tag_configure("ok", foreground=C["green"])

    def load_dashboard():
        if not check_conn(): return
        try:
            cursor.execute("SELECT COUNT(*) FROM livres")
            stat_cards["livres"].update_value(cursor.fetchone()[0])
            cursor.execute("SELECT COUNT(*) FROM membres")
            stat_cards["membres"].update_value(cursor.fetchone()[0])
            cursor.execute("SELECT COUNT(*) FROM emprunts WHERE retour_effectue='Non'")
            stat_cards["emprunts"].update_value(cursor.fetchone()[0])
            today = date.today().strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT COUNT(*) FROM emprunts
                WHERE retour_effectue='Non' AND date_retour < %s
            """, (today,))
            stat_cards["retards"].update_value(cursor.fetchone()[0])

            # Emprunts récents
            for row in tree_recent.get_children():
                tree_recent.delete(row)
            cursor.execute("""
                SELECT m.nom, m.prenom, l.titre,
                       e.date_emprunt, e.date_retour, e.retour_effectue
                FROM emprunts e
                JOIN membres m ON e.id_membre = m.id
                JOIN livres l ON e.id_livre = l.id
                ORDER BY e.id DESC LIMIT 12
            """)
            for row in cursor.fetchall():
                nom_complet = f"{row[0]} {row[1]}"
                retour = row[4]
                statut = "✅ Rendu" if row[5] == "Oui" else (
                    "🔴 En retard" if str(retour) < today else "🟡 En cours"
                )
                tag = "retard" if "retard" in statut else "ok" if "Rendu" in statut else "even"
                tree_recent.insert("", "end",
                                   values=(nom_complet, row[2], row[3], retour, statut),
                                   tags=(tag,))
        except Exception as e:
            print("Dashboard error:", e)

    btn_refresh = IconButton(dash, "  🔄 Actualiser le tableau de bord  ",
                             C["blue"], C["blue_hover"], command=load_dashboard)
    btn_refresh.pack(pady=5)

    # ============================================================
    # TAB 1 — LIVRES
    # ============================================================
    livres_tab = tk.Frame(notebook, bg=C["bg_dark"])
    notebook.add(livres_tab)

    section_header(livres_tab, "Gestion des Livres", "Catalogue complet de la bibliothèque")

    paned = tk.PanedWindow(livres_tab, orient="horizontal",
                           bg=C["bg_dark"], sashwidth=4, sashrelief="flat")
    paned.pack(fill="both", expand=True)

    # Panneau gauche (formulaire)
    left_l = tk.Frame(paned, bg=C["bg_card"], width=340,
                      highlightbackground=C["border"], highlightthickness=1)
    paned.add(left_l, minsize=280)

    tk.Label(left_l, text="Détails du livre",
             font=FONT_HEADER, bg=C["bg_card"], fg=C["accent"]).pack(anchor="w", padx=15, pady=(15, 5))
    tk.Frame(left_l, bg=C["border"], height=1).pack(fill="x", padx=15, pady=5)

    form_l = tk.Frame(left_l, bg=C["bg_card"])
    form_l.pack(fill="both", padx=15, pady=5)

    fields_livres = [
        ("Titre *", "ex: Le Petit Prince"),
        ("Auteur *", "ex: Antoine de Saint-Exupéry"),
        ("Genre *", "ex: Roman, Science-Fiction..."),
        ("ISBN", "ex: 978-2-07-040850-4"),
        ("Année", "ex: 1943"),
    ]
    entries_livres = []
    for i, (label, ph) in enumerate(fields_livres):
        tk.Label(form_l, text=label, font=FONT_SMALL,
                 bg=C["bg_card"], fg=C["muted"]).grid(row=i*2, column=0, sticky="w", pady=(8,0))
        e = DarkEntry(form_l, placeholder=ph, width=32)
        e.grid(row=i*2+1, column=0, sticky="ew", pady=(2,0), ipady=7)
        entries_livres.append(e)

    tk.Label(form_l, text="Disponible", font=FONT_SMALL,
             bg=C["bg_card"], fg=C["muted"]).grid(row=10, column=0, sticky="w", pady=(8,0))
    combo_dispo = DarkCombo(form_l, values=["Oui", "Non"], state="readonly", width=30)
    combo_dispo.set("Oui")
    combo_dispo.grid(row=11, column=0, sticky="ew", pady=(2,0))
    form_l.grid_columnconfigure(0, weight=1)

    # Boutons
    btns_l = tk.Frame(left_l, bg=C["bg_card"])
    btns_l.pack(fill="x", padx=15, pady=15)

    def clear_livre_form():
        for e in entries_livres:
            e.delete(0, tk.END)
            if e.placeholder:
                e._show_placeholder()
        combo_dispo.set("Oui")

    def get_livre_vals():
        return [e.get_value() for e in entries_livres] + [combo_dispo.get()]

    def validate_livre():
        vals = get_livre_vals()
        if not vals[0]: messagebox.showwarning("Champ requis", "Le titre est obligatoire !"); return False
        if not vals[1]: messagebox.showwarning("Champ requis", "L'auteur est obligatoire !"); return False
        if not vals[2]: messagebox.showwarning("Champ requis", "Le genre est obligatoire !"); return False
        if vals[4] and not vals[4].isdigit():
            messagebox.showwarning("Format", "L'année doit être un nombre !"); return False
        return True

    def ajouter_livre():
        if not check_conn() or not validate_livre(): return
        vals = get_livre_vals()
        try:
            cursor.execute("SELECT COUNT(*) FROM livres WHERE titre=%s AND auteur=%s",
                           (vals[0], vals[1]))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Doublon", "Ce livre existe déjà !"); return
            cursor.execute(
                "INSERT INTO livres (titre, auteur, genre, isbn, annee, disponible) VALUES (%s,%s,%s,%s,%s,%s)",
                [v if v else None for v in vals]
            )
            conn.commit()
            load_livres()
            load_dashboard()
            clear_livre_form()
            messagebox.showinfo("✅ Succès", "Livre ajouté avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_livre():
        if not check_conn() or not validate_livre(): return
        sel = tree_livres.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un livre à modifier"); return
        lid = tree_livres.item(sel[0])['values'][0]
        vals = get_livre_vals()
        try:
            cursor.execute(
                "UPDATE livres SET titre=%s, auteur=%s, genre=%s, isbn=%s, annee=%s, disponible=%s WHERE id=%s",
                vals + [lid]
            )
            conn.commit()
            load_livres()
            load_dashboard()
            messagebox.showinfo("✅ Succès", "Livre modifié !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_livre():
        if not check_conn(): return
        sel = tree_livres.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un livre"); return
        if not messagebox.askyesno("Confirmation", "Supprimer ce livre définitivement ?"): return
        lid = tree_livres.item(sel[0])['values'][0]
        try:
            # Vérifier qu'il n'est pas emprunté
            cursor.execute("SELECT COUNT(*) FROM emprunts WHERE id_livre=%s AND retour_effectue='Non'", (lid,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Impossible", "Ce livre est actuellement emprunté !"); return
            cursor.execute("DELETE FROM livres WHERE id=%s", (lid,))
            conn.commit()
            load_livres()
            load_dashboard()
            clear_livre_form()
            messagebox.showinfo("✅ Succès", "Livre supprimé !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    r1 = tk.Frame(btns_l, bg=C["bg_card"])
    r1.pack(fill="x", pady=3)
    IconButton(r1, "➕ Ajouter", C["green"], C["green_h"], command=ajouter_livre).pack(side="left", expand=True, fill="x", padx=3)
    IconButton(r1, "✏️ Modifier", C["blue"], C["blue_hover"], command=modifier_livre).pack(side="left", expand=True, fill="x", padx=3)
    r2 = tk.Frame(btns_l, bg=C["bg_card"])
    r2.pack(fill="x", pady=3)
    IconButton(r2, "🗑 Supprimer", C["red"], C["red_h"], command=supprimer_livre).pack(side="left", expand=True, fill="x", padx=3)
    IconButton(r2, "🧹 Vider", C["bg_input"], C["border"], command=clear_livre_form).pack(side="left", expand=True, fill="x", padx=3)

    # Panneau droit (table)
    right_l = tk.Frame(paned, bg=C["bg_dark"],
                       highlightbackground=C["border"], highlightthickness=1)
    paned.add(right_l)

    search_bar = tk.Frame(right_l, bg=C["bg_card"])
    search_bar.pack(fill="x")

    search_l = DarkEntry(search_bar, placeholder="🔍  Rechercher par titre, auteur, genre...", width=40)
    search_l.pack(side="left", padx=10, pady=10, fill="x", expand=True, ipady=7)

    filter_dispo = DarkCombo(search_bar, values=["Tous", "Disponible", "Emprunté"], state="readonly", width=14)
    filter_dispo.set("Tous")
    filter_dispo.pack(side="left", padx=5, pady=10)

    def load_livres(event=None):
        q = search_l.get_value()
        dispo_filter = filter_dispo.get()
        sql = "SELECT * FROM livres WHERE 1=1"
        params = []
        if q:
            sql += " AND (titre LIKE %s OR auteur LIKE %s OR genre LIKE %s)"
            params += [f"%{q}%", f"%{q}%", f"%{q}%"]
        if dispo_filter == "Disponible":
            sql += " AND disponible='Oui'"
        elif dispo_filter == "Emprunté":
            sql += " AND disponible='Non'"
        sql += " ORDER BY titre"
        refresh_tree(tree_livres, sql, params)
        # Colorer disponibilité
        for item in tree_livres.get_children():
            vals = tree_livres.item(item)['values']
            if vals[-1] == "Non":
                tree_livres.item(item, tags=("emprunte",))
        tree_livres.tag_configure("emprunte", foreground=C["amber"])

    IconButton(search_bar, "Rechercher", C["blue"], C["blue_hover"],
               command=load_livres).pack(side="left", padx=5, pady=10)

    search_l.bind("<Return>", load_livres)
    filter_dispo.bind("<<ComboboxSelected>>", load_livres)

    cols_l = ("id", "titre", "auteur", "genre", "isbn", "annee", "disponible")
    tree_frame_l = tk.Frame(right_l, bg=C["bg_dark"])
    tree_frame_l.pack(fill="both", expand=True, padx=5, pady=5)
    tree_livres = ttk.Treeview(tree_frame_l, columns=cols_l, show="headings")
    widths = [40, 220, 160, 120, 130, 60, 90]
    for col, w in zip(cols_l, widths):
        tree_livres.heading(col, text=col.capitalize())
        tree_livres.column(col, width=w, anchor="center")
    tree_livres.column("titre", anchor="w")
    tree_livres.column("auteur", anchor="w")
    add_scrollbars(tree_frame_l, tree_livres)

    # Compteur
    count_l = tk.Label(right_l, font=FONT_SMALL, bg=C["bg_dark"], fg=C["muted"])
    count_l.pack(anchor="e", padx=10, pady=3)

    def remplir_form_livre(event):
        sel = tree_livres.selection()
        if not sel: return
        vals = tree_livres.item(sel[0])['values']
        clear_livre_form()
        placeholders = [f[1] for f in fields_livres]
        for i, e in enumerate(entries_livres):
            e._has_placeholder = False
            e.config(fg=C["text"])
            e.delete(0, tk.END)
            if vals[i+1] and vals[i+1] != "None":
                e.insert(0, str(vals[i+1]))
            elif e.placeholder:
                e._show_placeholder()
        combo_dispo.set(vals[6])

    tree_livres.bind("<<TreeviewSelect>>", remplir_form_livre)

    # ============================================================
    # TAB 2 — MEMBRES
    # ============================================================
    membres_tab = tk.Frame(notebook, bg=C["bg_dark"])
    notebook.add(membres_tab)

    section_header(membres_tab, "Gestion des Membres", "Annuaire des adhérents")

    paned_m = tk.PanedWindow(membres_tab, orient="horizontal",
                              bg=C["bg_dark"], sashwidth=4)
    paned_m.pack(fill="both", expand=True)

    left_m = tk.Frame(paned_m, bg=C["bg_card"], width=340,
                      highlightbackground=C["border"], highlightthickness=1)
    paned_m.add(left_m, minsize=280)

    tk.Label(left_m, text="Fiche Membre",
             font=FONT_HEADER, bg=C["bg_card"], fg=C["accent"]).pack(anchor="w", padx=15, pady=(15,5))
    tk.Frame(left_m, bg=C["border"], height=1).pack(fill="x", padx=15, pady=5)

    form_m = tk.Frame(left_m, bg=C["bg_card"])
    form_m.pack(fill="both", padx=15, pady=5)

    fields_m = [
        ("Nom *", "Nom de famille"),
        ("Prénom *", "Prénom"),
        ("Email *", "exemple@mail.com"),
        ("Téléphone", "+257 XX XXX XXX"),
        ("Date inscription *", "AAAA-MM-JJ"),
    ]
    entries_membres = []
    for i, (label, ph) in enumerate(fields_m):
        tk.Label(form_m, text=label, font=FONT_SMALL,
                 bg=C["bg_card"], fg=C["muted"]).grid(row=i*2, column=0, sticky="w", pady=(8,0))
        e = DarkEntry(form_m, placeholder=ph, width=32)
        e.grid(row=i*2+1, column=0, sticky="ew", pady=(2,0), ipady=7)
        entries_membres.append(e)
    form_m.grid_columnconfigure(0, weight=1)

    def clear_m():
        for e in entries_membres:
            e.delete(0, tk.END)
            if e.placeholder: e._show_placeholder()
        # Date d'aujourd'hui par défaut
        entries_membres[4].config(fg=C["text"])
        entries_membres[4]._has_placeholder = False
        entries_membres[4].delete(0, tk.END)
        entries_membres[4].insert(0, date.today().strftime("%Y-%m-%d"))

    def validate_m():
        vals = [e.get_value() for e in entries_membres]
        if not vals[0]: messagebox.showwarning("Requis", "Le nom est obligatoire !"); return False
        if not vals[1]: messagebox.showwarning("Requis", "Le prénom est obligatoire !"); return False
        if not vals[2]: messagebox.showwarning("Requis", "L'email est obligatoire !"); return False
        if not validate_email(vals[2]):
            messagebox.showwarning("Format", "Email invalide !"); return False
        if vals[4] and not validate_date(vals[4]):
            messagebox.showwarning("Format", "Date invalide (AAAA-MM-JJ) !"); return False
        return True

    def ajouter_membre():
        if not check_conn() or not validate_m(): return
        vals = [e.get_value() for e in entries_membres]
        try:
            cursor.execute("SELECT COUNT(*) FROM membres WHERE email=%s", (vals[2],))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Doublon", "Cet email est déjà utilisé !"); return
            date_ins = vals[4] if vals[4] else date.today().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO membres (nom, prenom, email, telephone, date_inscription) VALUES (%s,%s,%s,%s,%s)",
                (vals[0], vals[1], vals[2], vals[3] or None, date_ins)
            )
            conn.commit()
            load_membres()
            load_dashboard()
            clear_m()
            messagebox.showinfo("✅ Succès", "Membre ajouté !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_membre():
        if not check_conn() or not validate_m(): return
        sel = tree_membres.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un membre"); return
        mid = tree_membres.item(sel[0])['values'][0]
        vals = [e.get_value() for e in entries_membres]
        try:
            cursor.execute(
                "UPDATE membres SET nom=%s, prenom=%s, email=%s, telephone=%s, date_inscription=%s WHERE id=%s",
                vals + [mid]
            )
            conn.commit()
            load_membres()
            load_dashboard()
            messagebox.showinfo("✅ Succès", "Membre modifié !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_membre():
        if not check_conn(): return
        sel = tree_membres.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un membre"); return
        if not messagebox.askyesno("Confirmation", "Supprimer ce membre ?"): return
        mid = tree_membres.item(sel[0])['values'][0]
        try:
            cursor.execute("SELECT COUNT(*) FROM emprunts WHERE id_membre=%s AND retour_effectue='Non'", (mid,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Impossible", "Ce membre a des emprunts actifs !"); return
            cursor.execute("DELETE FROM membres WHERE id=%s", (mid,))
            conn.commit()
            load_membres()
            load_dashboard()
            clear_m()
            messagebox.showinfo("✅ Succès", "Membre supprimé !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    btns_m = tk.Frame(left_m, bg=C["bg_card"])
    btns_m.pack(fill="x", padx=15, pady=15)
    rm1 = tk.Frame(btns_m, bg=C["bg_card"])
    rm1.pack(fill="x", pady=3)
    IconButton(rm1, "➕ Ajouter", C["green"], C["green_h"], command=ajouter_membre).pack(side="left", expand=True, fill="x", padx=3)
    IconButton(rm1, "✏️ Modifier", C["blue"], C["blue_hover"], command=modifier_membre).pack(side="left", expand=True, fill="x", padx=3)
    rm2 = tk.Frame(btns_m, bg=C["bg_card"])
    rm2.pack(fill="x", pady=3)
    IconButton(rm2, "🗑 Supprimer", C["red"], C["red_h"], command=supprimer_membre).pack(side="left", expand=True, fill="x", padx=3)
    IconButton(rm2, "🧹 Vider", C["bg_input"], C["border"], command=clear_m).pack(side="left", expand=True, fill="x", padx=3)

    right_m = tk.Frame(paned_m, bg=C["bg_dark"],
                       highlightbackground=C["border"], highlightthickness=1)
    paned_m.add(right_m)

    search_bar_m = tk.Frame(right_m, bg=C["bg_card"])
    search_bar_m.pack(fill="x")
    search_m = DarkEntry(search_bar_m, placeholder="🔍  Rechercher par nom, prénom ou email...", width=40)
    search_m.pack(side="left", padx=10, pady=10, fill="x", expand=True, ipady=7)

    def load_membres(event=None):
        q = search_m.get_value()
        if q:
            refresh_tree(tree_membres,
                "SELECT * FROM membres WHERE nom LIKE %s OR prenom LIKE %s OR email LIKE %s ORDER BY nom",
                (f"%{q}%", f"%{q}%", f"%{q}%"))
        else:
            refresh_tree(tree_membres, "SELECT * FROM membres ORDER BY nom")

    IconButton(search_bar_m, "Rechercher", C["blue"], C["blue_hover"],
               command=load_membres).pack(side="left", padx=5, pady=10)
    search_m.bind("<Return>", load_membres)

    cols_m = ("id", "nom", "prenom", "email", "telephone", "date_inscription")
    tree_frame_m = tk.Frame(right_m, bg=C["bg_dark"])
    tree_frame_m.pack(fill="both", expand=True, padx=5, pady=5)
    tree_membres = ttk.Treeview(tree_frame_m, columns=cols_m, show="headings")
    widths_m = [40, 130, 130, 200, 130, 120]
    for col, w in zip(cols_m, widths_m):
        tree_membres.heading(col, text=col.replace("_", " ").capitalize())
        tree_membres.column(col, width=w, anchor="center")
    tree_membres.column("nom", anchor="w")
    tree_membres.column("prenom", anchor="w")
    add_scrollbars(tree_frame_m, tree_membres)

    def remplir_form_m(event):
        sel = tree_membres.selection()
        if not sel: return
        vals = tree_membres.item(sel[0])['values']
        for i, e in enumerate(entries_membres):
            e._has_placeholder = False
            e.config(fg=C["text"])
            e.delete(0, tk.END)
            if vals[i+1] and str(vals[i+1]) != "None":
                e.insert(0, str(vals[i+1]))
            elif e.placeholder:
                e._show_placeholder()

    tree_membres.bind("<<TreeviewSelect>>", remplir_form_m)

    # ============================================================
    # TAB 3 — EMPRUNTS
    # ============================================================
    emprunts_tab = tk.Frame(notebook, bg=C["bg_dark"])
    notebook.add(emprunts_tab)

    section_header(emprunts_tab, "Gestion des Emprunts", "Enregistrement et suivi des prêts")

    paned_e = tk.PanedWindow(emprunts_tab, orient="horizontal",
                              bg=C["bg_dark"], sashwidth=4)
    paned_e.pack(fill="both", expand=True)

    left_e = tk.Frame(paned_e, bg=C["bg_card"], width=370,
                      highlightbackground=C["border"], highlightthickness=1)
    paned_e.add(left_e, minsize=300)

    tk.Label(left_e, text="Nouvel emprunt",
             font=FONT_HEADER, bg=C["bg_card"], fg=C["accent"]).pack(anchor="w", padx=15, pady=(15,5))
    tk.Frame(left_e, bg=C["border"], height=1).pack(fill="x", padx=15, pady=5)

    form_e = tk.Frame(left_e, bg=C["bg_card"])
    form_e.pack(fill="both", padx=15, pady=5)

    tk.Label(form_e, text="Membre *", font=FONT_SMALL,
             bg=C["bg_card"], fg=C["muted"]).grid(row=0, column=0, sticky="w", pady=(8,0))
    combo_membre = DarkCombo(form_e, width=36, state="readonly")
    combo_membre.grid(row=1, column=0, sticky="ew", pady=(2,0))

    tk.Label(form_e, text="Livre *", font=FONT_SMALL,
             bg=C["bg_card"], fg=C["muted"]).grid(row=2, column=0, sticky="w", pady=(8,0))
    combo_livre = DarkCombo(form_e, width=36, state="readonly")
    combo_livre.grid(row=3, column=0, sticky="ew", pady=(2,0))

    tk.Label(form_e, text="Date emprunt *", font=FONT_SMALL,
             bg=C["bg_card"], fg=C["muted"]).grid(row=4, column=0, sticky="w", pady=(8,0))
    entry_date_emp = DarkEntry(form_e, placeholder="AAAA-MM-JJ", width=36)
    entry_date_emp.grid(row=5, column=0, sticky="ew", pady=(2,0), ipady=7)

    tk.Label(form_e, text="Date retour prévue *", font=FONT_SMALL,
             bg=C["bg_card"], fg=C["muted"]).grid(row=6, column=0, sticky="w", pady=(8,0))
    entry_date_ret = DarkEntry(form_e, placeholder="AAAA-MM-JJ", width=36)
    entry_date_ret.grid(row=7, column=0, sticky="ew", pady=(2,0), ipady=7)

    # Bouton durée rapide
    quick_frame = tk.Frame(form_e, bg=C["bg_card"])
    quick_frame.grid(row=8, column=0, sticky="w", pady=5)
    tk.Label(quick_frame, text="Durée rapide:", font=FONT_SMALL,
             bg=C["bg_card"], fg=C["muted"]).pack(side="left", padx=(0,5))
    for days, label in [(7, "1 sem"), (14, "2 sem"), (30, "1 mois")]:
        def set_duration(d=days):
            today = date.today().strftime("%Y-%m-%d")
            ret = (date.today() + timedelta(days=d)).strftime("%Y-%m-%d")
            entry_date_emp._has_placeholder = False
            entry_date_emp.config(fg=C["text"])
            entry_date_emp.delete(0, tk.END)
            entry_date_emp.insert(0, today)
            entry_date_ret._has_placeholder = False
            entry_date_ret.config(fg=C["text"])
            entry_date_ret.delete(0, tk.END)
            entry_date_ret.insert(0, ret)
        tk.Button(quick_frame, text=label, font=FONT_SMALL,
                  bg=C["bg_input"], fg=C["accent"],
                  relief="flat", cursor="hand2", padx=8, pady=3,
                  command=set_duration).pack(side="left", padx=2)

    form_e.grid_columnconfigure(0, weight=1)

    def reload_listes():
        cursor.execute("SELECT id, nom, prenom FROM membres ORDER BY nom")
        combo_membre['values'] = [f"{r[0]} – {r[1]} {r[2]}" for r in cursor.fetchall()]
        cursor.execute("SELECT id, titre FROM livres WHERE disponible='Oui' ORDER BY titre")
        combo_livre['values'] = [f"{r[0]} – {r[1]}" for r in cursor.fetchall()]

    def clear_e():
        combo_membre.set("")
        combo_livre.set("")
        entry_date_emp.delete(0, tk.END)
        entry_date_emp._show_placeholder()
        entry_date_ret.delete(0, tk.END)
        entry_date_ret._show_placeholder()
        reload_listes()

    def ajouter_emprunt():
        if not check_conn(): return
        if not combo_membre.get(): messagebox.showwarning("Requis", "Sélectionnez un membre !"); return
        if not combo_livre.get(): messagebox.showwarning("Requis", "Sélectionnez un livre !"); return
        d_emp = entry_date_emp.get_value()
        d_ret = entry_date_ret.get_value()
        if not d_emp or not validate_date(d_emp):
            messagebox.showwarning("Format", "Date emprunt invalide (AAAA-MM-JJ) !"); return
        if not d_ret or not validate_date(d_ret):
            messagebox.showwarning("Format", "Date retour invalide (AAAA-MM-JJ) !"); return
        if d_ret < d_emp:
            messagebox.showwarning("Logique", "La date de retour doit être après l'emprunt !"); return
        try:
            id_m = combo_membre.get().split(" – ")[0]
            id_l = combo_livre.get().split(" – ")[0]
            cursor.execute("SELECT COUNT(*) FROM emprunts WHERE id_livre=%s AND retour_effectue='Non'", (id_l,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Indisponible", "Ce livre est déjà emprunté !"); return
            cursor.execute(
                "INSERT INTO emprunts (id_membre, id_livre, date_emprunt, date_retour, retour_effectue) VALUES (%s,%s,%s,%s,'Non')",
                (id_m, id_l, d_emp, d_ret)
            )
            cursor.execute("UPDATE livres SET disponible='Non' WHERE id=%s", (id_l,))
            conn.commit()
            load_emprunts()
            load_livres()
            load_dashboard()
            clear_e()
            messagebox.showinfo("✅ Succès", "Emprunt enregistré !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def retourner_livre():
        if not check_conn(): return
        sel = tree_emprunts.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un emprunt"); return
        vals = tree_emprunts.item(sel[0])['values']
        eid = vals[0]
        # Récupérer id_livre via la DB
        cursor.execute("SELECT id_livre, retour_effectue FROM emprunts WHERE id=%s", (eid,))
        row = cursor.fetchone()
        if not row: return
        id_livre, statut = row
        if statut == "Oui":
            messagebox.showinfo("Info", "Ce livre a déjà été rendu."); return
        try:
            today = date.today().strftime("%Y-%m-%d")
            cursor.execute("UPDATE emprunts SET retour_effectue='Oui', date_retour=%s WHERE id=%s",
                           (today, eid))
            cursor.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (id_livre,))
            conn.commit()
            load_emprunts()
            load_livres()
            load_dashboard()
            reload_retards()
            messagebox.showinfo("✅ Succès", "Livre retourné avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_emprunt():
        if not check_conn(): return
        sel = tree_emprunts.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un emprunt"); return
        if not messagebox.askyesno("Confirmation", "Supprimer cet emprunt ?"): return
        eid = tree_emprunts.item(sel[0])['values'][0]
        try:
            cursor.execute("DELETE FROM emprunts WHERE id=%s", (eid,))
            conn.commit()
            load_emprunts()
            load_dashboard()
            messagebox.showinfo("✅ Succès", "Emprunt supprimé !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    btns_e = tk.Frame(left_e, bg=C["bg_card"])
    btns_e.pack(fill="x", padx=15, pady=15)
    re1 = tk.Frame(btns_e, bg=C["bg_card"])
    re1.pack(fill="x", pady=3)
    IconButton(re1, "➕ Enregistrer", C["green"], C["green_h"], command=ajouter_emprunt).pack(side="left", expand=True, fill="x", padx=3)
    IconButton(re1, "📥 Retourner", C["purple"], "#6d28d9", command=retourner_livre).pack(side="left", expand=True, fill="x", padx=3)
    re2 = tk.Frame(btns_e, bg=C["bg_card"])
    re2.pack(fill="x", pady=3)
    IconButton(re2, "🗑 Supprimer", C["red"], C["red_h"], command=supprimer_emprunt).pack(side="left", expand=True, fill="x", padx=3)
    IconButton(re2, "🔄 Rafraîchir listes", C["bg_input"], C["border"], command=reload_listes).pack(side="left", expand=True, fill="x", padx=3)

    right_e = tk.Frame(paned_e, bg=C["bg_dark"],
                       highlightbackground=C["border"], highlightthickness=1)
    paned_e.add(right_e)

    search_bar_e = tk.Frame(right_e, bg=C["bg_card"])
    search_bar_e.pack(fill="x")
    search_e = DarkEntry(search_bar_e, placeholder="🔍  Rechercher par membre ou livre...", width=40)
    search_e.pack(side="left", padx=10, pady=10, fill="x", expand=True, ipady=7)

    filter_e = DarkCombo(search_bar_e, values=["Tous", "En cours", "Retournés", "En retard"],
                         state="readonly", width=14)
    filter_e.set("Tous")
    filter_e.pack(side="left", padx=5)

    def load_emprunts(event=None):
        q = search_e.get_value()
        f = filter_e.get()
        today = date.today().strftime("%Y-%m-%d")
        sql = """
            SELECT e.id, m.nom, m.prenom, l.titre,
                   e.date_emprunt, e.date_retour, e.retour_effectue
            FROM emprunts e
            JOIN membres m ON e.id_membre = m.id
            JOIN livres l ON e.id_livre = l.id
            WHERE 1=1
        """
        params = []
        if q:
            sql += " AND (m.nom LIKE %s OR m.prenom LIKE %s OR l.titre LIKE %s)"
            params += [f"%{q}%", f"%{q}%", f"%{q}%"]
        if f == "En cours":
            sql += " AND e.retour_effectue='Non'"
        elif f == "Retournés":
            sql += " AND e.retour_effectue='Oui'"
        elif f == "En retard":
            sql += f" AND e.retour_effectue='Non' AND e.date_retour < '{today}'"
        sql += " ORDER BY e.id DESC"

        for row in tree_emprunts.get_children():
            tree_emprunts.delete(row)
        cursor.execute(sql, params)
        for i, row in enumerate(cursor.fetchall()):
            retour = str(row[5])
            retour_eff = row[6]
            if retour_eff == "Oui":
                statut = "✅ Rendu"
                tag = "rendu"
            elif retour < today:
                statut = "🔴 Retard"
                tag = "retard"
            else:
                statut = "🟡 En cours"
                tag = "cours"
            tree_emprunts.insert("", "end",
                values=(row[0], f"{row[1]} {row[2]}", row[3], row[4], row[5], statut),
                tags=(tag,))
        tree_emprunts.tag_configure("retard", foreground=C["red"])
        tree_emprunts.tag_configure("rendu", foreground=C["green"])
        tree_emprunts.tag_configure("cours", foreground=C["amber"])

    IconButton(search_bar_e, "Rechercher", C["blue"], C["blue_hover"],
               command=load_emprunts).pack(side="left", padx=5, pady=10)
    search_e.bind("<Return>", load_emprunts)
    filter_e.bind("<<ComboboxSelected>>", load_emprunts)

    cols_e = ("id", "membre", "livre", "emprunté le", "retour prévu", "statut")
    tree_frame_e = tk.Frame(right_e, bg=C["bg_dark"])
    tree_frame_e.pack(fill="both", expand=True, padx=5, pady=5)
    tree_emprunts = ttk.Treeview(tree_frame_e, columns=cols_e, show="headings")
    widths_e = [40, 180, 220, 110, 110, 100]
    for col, w in zip(cols_e, widths_e):
        tree_emprunts.heading(col, text=col.capitalize())
        tree_emprunts.column(col, width=w, anchor="center")
    tree_emprunts.column("membre", anchor="w")
    tree_emprunts.column("livre", anchor="w")
    add_scrollbars(tree_frame_e, tree_emprunts)

    # ============================================================
    # TAB 4 — RETARDS
    # ============================================================
    retards_tab = tk.Frame(notebook, bg=C["bg_dark"])
    notebook.add(retards_tab)

    section_header(retards_tab, "⚠️ Livres en Retard", "Emprunts dépassant la date de retour prévue")

    cols_r = ("id", "membre", "email", "téléphone", "livre", "dû le", "jours retard")
    tree_frame_r = tk.Frame(retards_tab, bg=C["bg_dark"])
    tree_frame_r.pack(fill="both", expand=True, padx=5, pady=5)
    tree_retards = ttk.Treeview(tree_frame_r, columns=cols_r, show="headings")
    widths_r = [40, 180, 200, 130, 200, 110, 110]
    for col, w in zip(cols_r, widths_r):
        tree_retards.heading(col, text=col.capitalize())
        tree_retards.column(col, width=w, anchor="center")
    tree_retards.column("membre", anchor="w")
    tree_retards.column("livre", anchor="w")
    add_scrollbars(tree_frame_r, tree_retards)
    tree_retards.tag_configure("critique", foreground=C["red"])
    tree_retards.tag_configure("warn", foreground=C["amber"])

    retard_info = tk.Label(retards_tab, font=FONT_LABEL,
                           bg=C["bg_dark"], fg=C["muted"])
    retard_info.pack(pady=5)

    def reload_retards():
        today = date.today().strftime("%Y-%m-%d")
        for row in tree_retards.get_children():
            tree_retards.delete(row)
        cursor.execute("""
            SELECT e.id, m.nom, m.prenom, m.email, m.telephone,
                   l.titre, e.date_retour
            FROM emprunts e
            JOIN membres m ON e.id_membre = m.id
            JOIN livres l ON e.id_livre = l.id
            WHERE e.retour_effectue='Non' AND e.date_retour < %s
            ORDER BY e.date_retour ASC
        """, (today,))
        rows = cursor.fetchall()
        for row in rows:
            d_retour = row[6]
            jours = (date.today() - d_retour).days if hasattr(d_retour, 'days') else 0
            try:
                from datetime import datetime as dt
                d_obj = dt.strptime(str(d_retour), "%Y-%m-%d").date()
                jours = (date.today() - d_obj).days
            except: pass
            tag = "critique" if jours > 7 else "warn"
            tree_retards.insert("", "end",
                values=(row[0], f"{row[1]} {row[2]}", row[3], row[4], row[5],
                        str(row[6]), f"{jours} jour(s)"),
                tags=(tag,))
        retard_info.config(text=f"Total : {len(rows)} emprunt(s) en retard")

    btn_r = tk.Frame(retards_tab, bg=C["bg_dark"])
    btn_r.pack(pady=8)
    IconButton(btn_r, "🔄 Actualiser", C["blue"], C["blue_hover"],
               command=reload_retards).pack(side="left", padx=5)

    def retourner_depuis_retards():
        sel = tree_retards.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un emprunt"); return
        eid = tree_retards.item(sel[0])['values'][0]
        try:
            cursor.execute("SELECT id_livre FROM emprunts WHERE id=%s", (eid,))
            id_livre = cursor.fetchone()[0]
            today = date.today().strftime("%Y-%m-%d")
            cursor.execute("UPDATE emprunts SET retour_effectue='Oui', date_retour=%s WHERE id=%s",
                           (today, eid))
            cursor.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (id_livre,))
            conn.commit()
            reload_retards()
            load_emprunts()
            load_livres()
            load_dashboard()
            messagebox.showinfo("✅ Succès", "Livre marqué comme retourné !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    IconButton(btn_r, "📥 Marquer Retourné", C["purple"], "#6d28d9",
               command=retourner_depuis_retards).pack(side="left", padx=5)

    # ============================================================
    # TAB 5 — STATISTIQUES
    # ============================================================
    stats_tab = tk.Frame(notebook, bg=C["bg_dark"])
    notebook.add(stats_tab)

    section_header(stats_tab, "📊 Statistiques", "Analyse de l'activité de la bibliothèque")

    stats_inner = tk.Frame(stats_tab, bg=C["bg_dark"])
    stats_inner.pack(fill="both", expand=True, padx=5)

    stats_text = tk.Text(stats_inner, bg=C["bg_card"], fg=C["text"],
                         font=FONT_MONO, relief="flat", padx=20, pady=15,
                         state="disabled", wrap="word",
                         highlightbackground=C["border"], highlightthickness=1)
    stats_text.pack(fill="both", expand=True)

    def load_stats():
        if not check_conn(): return
        stats_text.config(state="normal")
        stats_text.delete("1.0", tk.END)
        today = date.today()
        lines = []
        lines.append("=" * 55)
        lines.append(f"  RAPPORT — {today.strftime('%d %B %Y')}")
        lines.append("=" * 55)

        cursor.execute("SELECT COUNT(*) FROM livres")
        lines.append(f"\n📚  Total livres          : {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM livres WHERE disponible='Oui'")
        lines.append(f"    Disponibles          : {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM livres WHERE disponible='Non'")
        lines.append(f"    Empruntés            : {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM membres")
        lines.append(f"\n👥  Total membres          : {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM emprunts")
        lines.append(f"\n🔄  Total emprunts         : {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM emprunts WHERE retour_effectue='Non'")
        lines.append(f"    En cours             : {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM emprunts WHERE retour_effectue='Non' AND date_retour < %s",
                       (today.strftime('%Y-%m-%d'),))
        lines.append(f"    En retard            : {cursor.fetchone()[0]}")

        lines.append("\n" + "-" * 55)
        lines.append("  TOP 5 LIVRES LES PLUS EMPRUNTÉS")
        lines.append("-" * 55)
        cursor.execute("""
            SELECT l.titre, l.auteur, COUNT(*) as nb
            FROM emprunts e JOIN livres l ON e.id_livre = l.id
            GROUP BY l.id ORDER BY nb DESC LIMIT 5
        """)
        for i, row in enumerate(cursor.fetchall(), 1):
            lines.append(f"  {i}. {row[0][:30]:<30} ({row[2]} fois)")

        lines.append("\n" + "-" * 55)
        lines.append("  TOP 5 MEMBRES LES PLUS ACTIFS")
        lines.append("-" * 55)
        cursor.execute("""
            SELECT m.nom, m.prenom, COUNT(*) as nb
            FROM emprunts e JOIN membres m ON e.id_membre = m.id
            GROUP BY m.id ORDER BY nb DESC LIMIT 5
        """)
        for i, row in enumerate(cursor.fetchall(), 1):
            lines.append(f"  {i}. {row[0]} {row[1]:<25} ({row[2]} emprunts)")

        lines.append("\n" + "-" * 55)
        lines.append("  GENRES LES PLUS POPULAIRES")
        lines.append("-" * 55)
        cursor.execute("""
            SELECT l.genre, COUNT(*) as nb
            FROM emprunts e JOIN livres l ON e.id_livre = l.id
            WHERE l.genre IS NOT NULL
            GROUP BY l.genre ORDER BY nb DESC LIMIT 5
        """)
        for row in cursor.fetchall():
            lines.append(f"  • {row[0]:<30} {row[1]} emprunts")

        lines.append("\n" + "=" * 55)
        stats_text.insert("1.0", "\n".join(lines))
        stats_text.config(state="disabled")

    IconButton(stats_tab, "  📊 Générer les statistiques  ",
               C["blue"], C["blue_hover"], command=load_stats).pack(pady=10)

    # ============================================================
    # CHARGEMENT INITIAL
    # ============================================================
    switch_tab(0)
    load_dashboard()
    load_livres()
    load_membres()
    load_emprunts()
    reload_retards()
    reload_listes()

    root.mainloop()
    if conn:
        conn.close()


# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    show_login(open_main_app)