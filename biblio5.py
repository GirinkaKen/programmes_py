import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime, date

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
# PALETTE DE COULEURS
# ========================
C = {
    "bg_dark":      "#0f172a",   # bleu marine très foncé
    "bg_mid":       "#1e293b",   # sidebar
    "bg_light":     "#f8fafc",   # fond principal
    "bg_card":      "#ffffff",   # cartes blanches
    "primary":      "#3b82f6",   # bleu vif
    "primary_dark": "#1d4ed8",
    "success":      "#10b981",   # vert
    "success_dark": "#059669",
    "danger":       "#ef4444",   # rouge
    "danger_dark":  "#b91c1c",
    "warning":      "#f59e0b",   # orange
    "purple":       "#8b5cf6",
    "purple_dark":  "#6d28d9",
    "info":         "#64748b",
    "info_dark":    "#475569",
    "text_dark":    "#0f172a",
    "text_mid":     "#475569",
    "text_light":   "#94a3b8",
    "border":       "#e2e8f0",
    "row_alt":      "#f1f5f9",   # lignes alternées
    "row_hover":    "#dbeafe",   # survol bleu clair
    "row_sel":      "#bfdbfe",   # sélection
    "header_bg":    "#1e293b",   # entête table
    "header_fg":    "#e2e8f0",
    "white":        "#ffffff",
}


def show_login():
    login_win = tk.Tk()
    login_win.title("Connexion — Bibliothèque")
    login_win.geometry("420x380")
    login_win.configure(bg=C["bg_dark"])
    login_win.resizable(False, False)

    # Panel central
    panel = tk.Frame(login_win, bg=C["bg_mid"], bd=0)
    panel.place(relx=0.5, rely=0.5, anchor="center", width=340, height=300)

    tk.Label(panel, text="📚", font=("Segoe UI Emoji", 32),
             bg=C["bg_mid"], fg=C["primary"]).pack(pady=(25, 5))
    tk.Label(panel, text="BIBLIOTHÈQUE", font=("Segoe UI", 14, "bold"),
             bg=C["bg_mid"], fg=C["white"]).pack()
    tk.Label(panel, text="Système de gestion", font=("Segoe UI", 9),
             bg=C["bg_mid"], fg=C["text_light"]).pack(pady=(0, 20))

    # Champs
    entry_user = tk.Entry(panel, width=28, font=("Segoe UI", 10),
                          bg=C["bg_dark"], fg=C["white"], insertbackground=C["white"],
                          relief="flat", bd=8)
    entry_user.insert(0, "Nom d'utilisateur")
    entry_user.pack(pady=3)

    entry_pass = tk.Entry(panel, width=28, font=("Segoe UI", 10),
                          bg=C["bg_dark"], fg=C["text_light"], insertbackground=C["white"],
                          relief="flat", bd=8, show="●")
    entry_pass.pack(pady=3)

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

    btn = tk.Button(panel, text="Se connecter →", command=login,
                    bg=C["primary"], fg=C["white"],
                    font=("Segoe UI", 10, "bold"), relief="flat",
                    cursor="hand2", activebackground=C["primary_dark"],
                    activeforeground=C["white"])
    btn.pack(fill="x", padx=25, pady=12, ipady=8)

    login_win.mainloop()


def open_main_app():
    global root
    root = tk.Tk()
    root.title("📚 Gestion de Bibliothèque")
    root.geometry("1550x900")
    root.minsize(1200, 700)
    root.configure(bg=C["bg_light"])

    # ========================
    # STYLES TTK GLOBAUX
    # ========================
    style = ttk.Style()
    style.theme_use("clam")

    # --- Treeview (TABLE) PRO ---
    style.configure("Pro.Treeview",
                    background=C["bg_card"],
                    foreground=C["text_dark"],
                    rowheight=38,
                    fieldbackground=C["bg_card"],
                    borderwidth=0,
                    relief="flat",
                    font=("Segoe UI", 10))

    style.configure("Pro.Treeview.Heading",
                    background=C["header_bg"],
                    foreground=C["header_fg"],
                    font=("Segoe UI", 10, "bold"),
                    relief="flat",
                    borderwidth=0,
                    padding=[12, 10])

    style.map("Pro.Treeview",
              background=[("selected", C["row_sel"])],
              foreground=[("selected", C["text_dark"])])

    style.map("Pro.Treeview.Heading",
              background=[("active", C["primary"])])

    # --- Scrollbar fine ---
    style.configure("Slim.Vertical.TScrollbar",
                    gripcount=0,
                    background=C["border"],
                    troughcolor=C["bg_light"],
                    borderwidth=0,
                    arrowsize=0,
                    width=6)

    style.configure("Slim.Horizontal.TScrollbar",
                    gripcount=0,
                    background=C["border"],
                    troughcolor=C["bg_light"],
                    borderwidth=0,
                    arrowsize=0,
                    width=6)

    # --- Boutons ---
    for name, bg, active in [
        ("Success", C["success"], C["success_dark"]),
        ("Primary", C["primary"], C["primary_dark"]),
        ("Danger",  C["danger"],  C["danger_dark"]),
        ("Info",    C["info"],    C["info_dark"]),
        ("Purple",  C["purple"],  C["purple_dark"]),
    ]:
        style.configure(f"{name}.TButton",
                        background=bg, foreground=C["white"],
                        font=("Segoe UI", 10, "bold"),
                        padding=[14, 8], borderwidth=0, focusthickness=0)
        style.map(f"{name}.TButton", background=[("active", active)])

    # --- Notebook ---
    style.configure("TNotebook", background=C["bg_light"], borderwidth=0)
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"),
                    padding=[18, 10], background="#e2e8f0")
    style.map("TNotebook.Tab",
              background=[("selected", C["white"])],
              foreground=[("selected", C["primary"])])

    # --- LabelFrame ---
    style.configure("TLabelframe", background=C["white"], bordercolor=C["border"])
    style.configure("TLabelframe.Label", background=C["white"],
                    foreground=C["primary"], font=("Segoe UI", 10, "bold"))

    # ========================
    # HEADER
    # ========================
    header = tk.Frame(root, bg=C["bg_dark"], height=64)
    header.pack(side=tk.TOP, fill="x")
    header.pack_propagate(False)

    hc = tk.Frame(header, bg=C["bg_dark"])
    hc.pack(fill="both", expand=True, padx=24)

    lf = tk.Frame(hc, bg=C["bg_dark"])
    lf.pack(side=tk.LEFT, pady=10)
    tk.Label(lf, text="📚", bg=C["bg_dark"], fg=C["primary"],
             font=("Segoe UI Emoji", 18)).pack(side=tk.LEFT, padx=(0, 8))
    tk.Label(lf, text="GESTION BIBLIOTHÈQUE", bg=C["bg_dark"], fg=C["white"],
             font=("Segoe UI", 15, "bold")).pack(side=tk.LEFT)
    tk.Label(hc, text="Système de gestion intelligent",
             bg=C["bg_dark"], fg=C["text_light"],
             font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=18)

    rf = tk.Frame(hc, bg=C["bg_dark"])
    rf.pack(side=tk.RIGHT)

    # Badge date
    date_badge = tk.Frame(rf, bg="#1e293b", padx=10, pady=4)
    date_badge.pack(side=tk.RIGHT, padx=6)
    tk.Label(date_badge, text=datetime.now().strftime("📅  %d %B %Y"),
             bg="#1e293b", fg=C["text_light"], font=("Segoe UI", 9)).pack()

    # Badge admin
    admin_badge = tk.Frame(rf, bg=C["primary"], padx=10, pady=4)
    admin_badge.pack(side=tk.RIGHT, padx=6)
    tk.Label(admin_badge, text="👤  Admin",
             bg=C["primary"], fg=C["white"], font=("Segoe UI", 9, "bold")).pack()

    # ========================
    # SIDEBAR
    # ========================
    sidebar = tk.Frame(root, bg=C["bg_mid"], width=240)
    sidebar.pack(side=tk.LEFT, fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="MENU", bg=C["bg_mid"], fg=C["text_light"],
             font=("Segoe UI", 8, "bold")).pack(pady=(28, 4), padx=20, anchor="w")
    tk.Frame(sidebar, bg="#334155", height=1).pack(fill="x", padx=20, pady=8)

    menu_buttons = []

    def switch_tab(index):
        notebook.select(index)
        highlight_button(index)

    def highlight_button(index):
        for i, (btn, dot) in enumerate(menu_buttons):
            if i == index:
                btn.configure(bg=C["primary"], fg=C["white"])
                dot.configure(bg=C["primary"])
            else:
                btn.configure(bg=C["bg_mid"], fg=C["text_light"])
                dot.configure(bg=C["bg_mid"])

    def on_enter(e, btn, dot):
        btn.configure(bg="#2d3f55")
        dot.configure(bg="#2d3f55")

    def on_leave(e, btn, dot, idx):
        nb_idx = notebook.index("current")
        if nb_idx != idx:
            btn.configure(bg=C["bg_mid"])
            dot.configure(bg=C["bg_mid"])

    menu_items = [
        ("🏠", "Dashboard", 0),
        ("📖", "Livres", 1),
        ("👥", "Membres", 2),
        ("🔄", "Emprunts", 3),
    ]

    for icon, text, idx in menu_items:
        row = tk.Frame(sidebar, bg=C["bg_mid"], cursor="hand2")
        row.pack(fill="x", padx=12, pady=3)

        dot = tk.Frame(row, bg=C["bg_mid"], width=4)
        dot.pack(side=tk.LEFT, fill="y")

        inner = tk.Frame(row, bg=C["bg_mid"], padx=14, pady=11)
        inner.pack(side=tk.LEFT, fill="both", expand=True)

        tk.Label(inner, text=f"{icon}  {text}", bg=C["bg_mid"], fg=C["text_light"],
                 font=("Segoe UI", 11), anchor="w").pack(anchor="w")

        btn_ref = inner.winfo_children()[0]
        menu_buttons.append((row, dot))

        row.bind("<Button-1>", lambda e, i=idx: switch_tab(i))
        inner.bind("<Button-1>", lambda e, i=idx: switch_tab(i))
        btn_ref.bind("<Button-1>", lambda e, i=idx: switch_tab(i))
        row.bind("<Enter>", lambda e, r=row, d=dot: (r.configure(bg="#2d3f55"), d.configure(bg="#2d3f55"),
                 [c.configure(bg="#2d3f55") for c in r.winfo_children()],
                 [c.configure(bg="#2d3f55") for c in r.winfo_children()[1].winfo_children()]))
        row.bind("<Leave>", lambda e, r=row, d=dot, i=idx: None)

    highlight_button(0)

    # ========================
    # ZONE PRINCIPALE
    # ========================
    main_area = tk.Frame(root, bg=C["bg_light"])
    main_area.pack(side=tk.RIGHT, expand=True, fill="both")

    container = tk.Frame(main_area, bg=C["bg_light"])
    container.pack(expand=True, fill="both", padx=16, pady=16)

    notebook = ttk.Notebook(container)
    notebook.pack(expand=True, fill="both")

    # ========================
    # HELPER: TABLE PROFESSIONNELLE
    # ========================
    def make_pro_table(parent, columns, col_widths=None, col_anchors=None):
        """
        Crée une table professionnelle avec :
        - En-têtes stylisés fond foncé
        - Lignes alternées (zebrastripe)
        - Scrollbars fines
        - Bordures subtiles
        """
        wrapper = tk.Frame(parent, bg=C["bg_card"],
                           highlightbackground=C["border"],
                           highlightthickness=1)
        wrapper.pack(fill="both", expand=True)

        # Scrollbars fines
        vsb = ttk.Scrollbar(wrapper, orient="vertical", style="Slim.Vertical.TScrollbar")
        hsb = ttk.Scrollbar(wrapper, orient="horizontal", style="Slim.Horizontal.TScrollbar")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tree = ttk.Treeview(wrapper,
                            columns=columns,
                            show="headings",
                            style="Pro.Treeview",
                            yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        tree.pack(fill="both", expand=True)
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        # Configuration colonnes
        for i, col in enumerate(columns):
            label = col.replace("_", " ").title()
            w = col_widths[i] if col_widths else 130
            anch = col_anchors[i] if col_anchors else "center"
            tree.heading(col, text=f"  {label}", anchor="w")
            tree.column(col, width=w, anchor=anch, minwidth=60)

        # Couleurs lignes alternées
        tree.tag_configure("odd",  background=C["bg_card"])
        tree.tag_configure("even", background=C["row_alt"])
        tree.tag_configure("retard",  background="#fef2f2", foreground="#b91c1c")
        tree.tag_configure("actif",   background="#f0fdf4", foreground="#065f46")
        tree.tag_configure("nonDispo",background="#fff7ed", foreground="#92400e")

        return tree, wrapper

    def insert_rows(tree, rows, special_col=None, special_val=None, tag_map=None):
        """Insère les lignes avec zebrastripe et tags spéciaux."""
        tree.delete(*tree.get_children())
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            if special_col is not None and tag_map:
                val = str(row[special_col]).strip()
                tag = tag_map.get(val, tag)
            tree.insert("", "end", values=row, tags=(tag,))

    # ========================
    # UTILITAIRES
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
                messagebox.showwarning("Champ obligatoire", f"Le champ '{labels[i]}' est obligatoire !")
                entries[i].focus()
                return False
        return True

    def actualiser_table(table_name, tree, special_col=None, tag_map=None):
        if not check_connexion():
            return
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        insert_rows(tree, rows, special_col=special_col, tag_map=tag_map)

    # ========================
    # HELPER: BOUTON ACTION
    # ========================
    def action_btn(parent, text, color, hover, cmd):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=C["white"],
                      font=("Segoe UI", 10, "bold"),
                      relief="flat", cursor="hand2",
                      activebackground=hover,
                      activeforeground=C["white"],
                      padx=14, pady=7, bd=0)
        b.bind("<Enter>", lambda e: b.configure(bg=hover))
        b.bind("<Leave>", lambda e: b.configure(bg=color))
        return b

    # ========================
    # HELPER: CHAMP FORMULAIRE
    # ========================
    def make_field(parent, label, row, is_combo=False, values=None, default=""):
        tk.Label(parent, text=label, bg=C["white"], fg=C["text_mid"],
                 font=("Segoe UI", 9, "bold")).grid(row=row*2, column=0,
                 columnspan=2, sticky="w", padx=16, pady=(10, 2))
        if is_combo:
            ent = ttk.Combobox(parent, values=values, state="readonly", width=30)
            ent.set(default)
        else:
            ent = tk.Entry(parent, width=32, font=("Segoe UI", 10),
                           bg=C["bg_light"], fg=C["text_dark"],
                           relief="flat", bd=0,
                           insertbackground=C["primary"],
                           highlightthickness=1,
                           highlightbackground=C["border"],
                           highlightcolor=C["primary"])
        ent.grid(row=row*2+1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 4), ipady=7)
        return ent

    # ========================
    # BADGE DE STATUT (pour affichage)
    # ========================
    def status_badge_label(parent, text, color):
        f = tk.Frame(parent, bg=color, padx=8, pady=2)
        tk.Label(f, text=text, bg=color, fg="white",
                 font=("Segoe UI", 8, "bold")).pack()
        return f

    # ========================
    # DASHBOARD
    # ========================
    dash_tab = tk.Frame(notebook, bg=C["bg_light"])
    notebook.add(dash_tab, text="  🏠 Dashboard  ")

    # Header dashboard
    dh = tk.Frame(dash_tab, bg=C["bg_light"])
    dh.pack(fill="x", padx=30, pady=(28, 0))
    tk.Label(dh, text="Tableau de bord",
             font=("Segoe UI", 24, "bold"), bg=C["bg_light"], fg=C["text_dark"]).pack(anchor="w")
    tk.Label(dh, text="Vue d'ensemble des activités de la bibliothèque",
             font=("Segoe UI", 10), bg=C["bg_light"], fg=C["text_mid"]).pack(anchor="w", pady=(4, 0))

    tk.Frame(dash_tab, bg=C["border"], height=1).pack(fill="x", padx=30, pady=16)

    cards_row = tk.Frame(dash_tab, bg=C["bg_light"])
    cards_row.pack(fill="x", padx=24)

    def create_dash_card(parent, icon, title, value, color, subtitle=""):
        card = tk.Frame(parent, bg=C["bg_card"],
                        highlightbackground=C["border"],
                        highlightthickness=1)
        card.pack(side=tk.LEFT, expand=True, fill="both", padx=8, pady=8)

        # Bande colorée top
        tk.Frame(card, bg=color, height=4).pack(fill="x")

        inner = tk.Frame(card, bg=C["bg_card"], padx=22, pady=18)
        inner.pack(fill="both", expand=True)

        # Icône dans cercle coloré
        icon_f = tk.Frame(inner, bg=color, width=44, height=44)
        icon_f.pack(anchor="w")
        icon_f.pack_propagate(False)
        tk.Label(icon_f, text=icon, bg=color, fg="white",
                 font=("Segoe UI Emoji", 16)).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text=str(value),
                 font=("Segoe UI", 34, "bold"),
                 bg=C["bg_card"], fg=color).pack(anchor="w", pady=(12, 0))
        tk.Label(inner, text=title,
                 font=("Segoe UI", 11, "bold"),
                 bg=C["bg_card"], fg=C["text_dark"]).pack(anchor="w")
        if subtitle:
            tk.Label(inner, text=subtitle,
                     font=("Segoe UI", 8),
                     bg=C["bg_card"], fg=C["text_light"]).pack(anchor="w", pady=(2, 0))

    def load_dashboard():
        if not conn:
            return
        try:
            cursor.execute("SELECT COUNT(*) FROM livres"); total_livres = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM membres"); total_membres = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM emprunts WHERE retour_effectue='Non' OR retour_effectue IS NULL")
            en_cours = cursor.fetchone()[0]
            today = date.today().strftime('%Y-%m-%d')
            cursor.execute("""SELECT COUNT(*) FROM emprunts
                WHERE (retour_effectue='Non' OR retour_effectue IS NULL) AND date_retour < %s""", (today,))
            en_retard = cursor.fetchone()[0]

            for w in cards_row.winfo_children():
                w.destroy()

            create_dash_card(cards_row, "📚", "Livres total", total_livres, C["primary"], "dans la collection")
            create_dash_card(cards_row, "👥", "Membres actifs", total_membres, C["success"], "inscrits")
            create_dash_card(cards_row, "🔄", "Emprunts en cours", en_cours, C["warning"], "non retournés")
            create_dash_card(cards_row, "⚠️", "En retard", en_retard, C["danger"], "dépassé la date")
        except Exception as e:
            print("Erreur dashboard:", e)

    load_dashboard()

    act_frame = tk.Frame(dash_tab, bg=C["bg_light"])
    act_frame.pack(pady=20)
    action_btn(act_frame, "🔄  Actualiser le tableau", C["primary"], C["primary_dark"],
               load_dashboard).pack(ipadx=10, ipady=4)

    # ========================
    # ONGLET LIVRES
    # ========================
    livres_tab = ttk.Frame(notebook)
    notebook.add(livres_tab, text="  📖 Livres  ")

    lv_main = tk.Frame(livres_tab, bg=C["bg_light"])
    lv_main.pack(fill="both", expand=True)

    # --- Panel gauche (formulaire) ---
    lv_left = tk.Frame(lv_main, bg=C["bg_card"], width=320,
                       highlightbackground=C["border"], highlightthickness=1)
    lv_left.pack(side="left", fill="y", padx=(12, 6), pady=12)
    lv_left.pack_propagate(False)

    tk.Label(lv_left, text="📖  Gestion des Livres",
             font=("Segoe UI", 13, "bold"), bg=C["bg_card"], fg=C["text_dark"]).pack(
             pady=(20, 4), padx=16, anchor="w")
    tk.Frame(lv_left, bg=C["border"], height=1).pack(fill="x", padx=16, pady=8)

    labels_livres = ["Titre", "Auteur", "Genre", "ISBN", "Année", "Disponible"]
    entries_livres = []
    lv_form = tk.Frame(lv_left, bg=C["bg_card"])
    lv_form.pack(fill="x")
    lv_form.columnconfigure(0, weight=1)

    for i, label in enumerate(labels_livres):
        if label == "Disponible":
            ent = make_field(lv_form, label, i, is_combo=True, values=["Oui", "Non"], default="Oui")
        else:
            ent = make_field(lv_form, label, i)
        entries_livres.append(ent)

    tk.Frame(lv_left, bg=C["border"], height=1).pack(fill="x", padx=16, pady=12)

    # --- Panel droit (table) ---
    lv_right = tk.Frame(lv_main, bg=C["bg_light"])
    lv_right.pack(side="right", fill="both", expand=True, padx=(6, 12), pady=12)

    # Barre recherche
    search_bar = tk.Frame(lv_right, bg=C["bg_card"],
                          highlightbackground=C["border"], highlightthickness=1)
    search_bar.pack(fill="x", pady=(0, 8))

    tk.Label(search_bar, text="🔍", bg=C["bg_card"], fg=C["text_mid"],
             font=("Segoe UI", 11)).pack(side="left", padx=(12, 4))
    lv_search = tk.Entry(search_bar, width=36, font=("Segoe UI", 10),
                         bg=C["bg_card"], fg=C["text_dark"], relief="flat",
                         insertbackground=C["primary"])
    lv_search.pack(side="left", ipady=10, padx=4)
    lv_search.insert(0, "Rechercher par titre ou auteur...")
    lv_search.bind("<FocusIn>", lambda e: lv_search.delete(0, "end") if lv_search.get().startswith("Rechercher") else None)

    # Titre + compteur
    lv_header = tk.Frame(lv_right, bg=C["bg_light"])
    lv_header.pack(fill="x", pady=(0, 6))
    tk.Label(lv_header, text="Liste des Livres",
             font=("Segoe UI", 14, "bold"), bg=C["bg_light"], fg=C["text_dark"]).pack(side="left")

    # TABLE LIVRES
    lv_cols = ("id", "titre", "auteur", "genre", "isbn", "annee", "disponible")
    lv_widths = [50, 220, 160, 120, 130, 80, 90]
    lv_anchors = ["center", "w", "w", "center", "center", "center", "center"]
    tree_livres, _ = make_pro_table(lv_right, lv_cols, lv_widths, lv_anchors)

    # Fonctions livres
    def reload_livres():
        cursor.execute("SELECT * FROM livres")
        rows = cursor.fetchall()
        tag_map = {"Oui": "actif", "Non": "nonDispo"}
        insert_rows(tree_livres, rows, special_col=6, tag_map=tag_map)

    def ajouter_livre():
        if not check_connexion(): return
        if not valider_champs(entries_livres, [True,True,True,True,True,True], labels_livres): return
        try:
            titre = entries_livres[0].get().strip()
            auteur = entries_livres[1].get().strip()
            isbn = entries_livres[3].get().strip()
            cursor.execute("SELECT COUNT(*) FROM livres WHERE (titre=%s AND auteur=%s) OR isbn=%s",
                           (titre, auteur, isbn or None))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Doublon", "Ce livre existe déjà !")
                return
            vals = [e.get().strip() or None for e in entries_livres]
            cursor.execute("INSERT INTO livres (titre,auteur,genre,isbn,annee,disponible) VALUES (%s,%s,%s,%s,%s,%s)", vals)
            conn.commit()
            reload_livres(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Livre ajouté avec succès !")
            for e in entries_livres:
                if hasattr(e, "set"): e.set("")
                else: e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_livre():
        if not check_connexion(): return
        try:
            sel = tree_livres.selection()[0]
            lid = tree_livres.item(sel)['values'][0]
            cursor.execute("UPDATE livres SET titre=%s,auteur=%s,genre=%s,isbn=%s,annee=%s,disponible=%s WHERE id=%s",
                           [e.get().strip() for e in entries_livres] + [lid])
            conn.commit(); reload_livres(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Livre modifié !")
        except IndexError:
            messagebox.showwarning("Sélection", "Sélectionnez un livre dans la table")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_livre():
        if not check_connexion(): return
        if not messagebox.askyesno("Confirmation", "Supprimer ce livre définitivement ?"): return
        try:
            sel = tree_livres.selection()[0]
            lid = tree_livres.item(sel)['values'][0]
            cursor.execute("DELETE FROM livres WHERE id=%s", (lid,))
            conn.commit(); reload_livres(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Livre supprimé !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rechercher_livre():
        q = lv_search.get().strip()
        if q.startswith("Rechercher"): q = ""
        tree_livres.delete(*tree_livres.get_children())
        if q:
            cursor.execute("SELECT * FROM livres WHERE titre LIKE %s OR auteur LIKE %s",
                           (f"%{q}%", f"%{q}%"))
        else:
            cursor.execute("SELECT * FROM livres")
        rows = cursor.fetchall()
        tag_map = {"Oui": "actif", "Non": "nonDispo"}
        insert_rows(tree_livres, rows, special_col=6, tag_map=tag_map)

    def fill_form_from_selection_livres(e):
        try:
            sel = tree_livres.selection()[0]
            vals = tree_livres.item(sel)['values']
            for i, ent in enumerate(entries_livres):
                if hasattr(ent, "set"): ent.set(str(vals[i+1]))
                else:
                    ent.delete(0, tk.END)
                    ent.insert(0, str(vals[i+1]))
        except: pass

    tree_livres.bind("<<TreeviewSelect>>", fill_form_from_selection_livres)

    # Boutons livres (dans left panel)
    btn_grid = tk.Frame(lv_left, bg=C["bg_card"])
    btn_grid.pack(fill="x", padx=16, pady=8)
    action_btn(btn_grid, "➕  Ajouter", C["success"], C["success_dark"], ajouter_livre).pack(fill="x", pady=3)
    action_btn(btn_grid, "✏️  Modifier", C["primary"], C["primary_dark"], modifier_livre).pack(fill="x", pady=3)
    action_btn(btn_grid, "🗑  Supprimer", C["danger"], C["danger_dark"], supprimer_livre).pack(fill="x", pady=3)

    # Boutons barre recherche
    action_btn(search_bar, "Rechercher", C["primary"], C["primary_dark"],
               rechercher_livre).pack(side="left", padx=6, pady=8)
    action_btn(search_bar, "↻ Reset", C["info"], C["info_dark"],
               reload_livres).pack(side="left", pady=8)

    # ========================
    # ONGLET MEMBRES
    # ========================
    membres_tab = ttk.Frame(notebook)
    notebook.add(membres_tab, text="  👥 Membres  ")

    mb_main = tk.Frame(membres_tab, bg=C["bg_light"])
    mb_main.pack(fill="both", expand=True)

    mb_left = tk.Frame(mb_main, bg=C["bg_card"], width=320,
                       highlightbackground=C["border"], highlightthickness=1)
    mb_left.pack(side="left", fill="y", padx=(12, 6), pady=12)
    mb_left.pack_propagate(False)

    tk.Label(mb_left, text="👥  Gestion des Membres",
             font=("Segoe UI", 13, "bold"), bg=C["bg_card"], fg=C["text_dark"]).pack(
             pady=(20, 4), padx=16, anchor="w")
    tk.Frame(mb_left, bg=C["border"], height=1).pack(fill="x", padx=16, pady=8)

    labels_membres = ["Nom", "Prénom", "Email", "Téléphone", "Date Inscription (AAAA-MM-JJ)"]
    entries_membres = []
    mb_form = tk.Frame(mb_left, bg=C["bg_card"])
    mb_form.pack(fill="x")
    mb_form.columnconfigure(0, weight=1)

    for i, label in enumerate(labels_membres):
        ent = make_field(mb_form, label, i)
        entries_membres.append(ent)

    tk.Frame(mb_left, bg=C["border"], height=1).pack(fill="x", padx=16, pady=12)

    mb_right = tk.Frame(mb_main, bg=C["bg_light"])
    mb_right.pack(side="right", fill="both", expand=True, padx=(6, 12), pady=12)

    mb_search_bar = tk.Frame(mb_right, bg=C["bg_card"],
                             highlightbackground=C["border"], highlightthickness=1)
    mb_search_bar.pack(fill="x", pady=(0, 8))
    tk.Label(mb_search_bar, text="🔍", bg=C["bg_card"], fg=C["text_mid"],
             font=("Segoe UI", 11)).pack(side="left", padx=(12, 4))
    mb_search = tk.Entry(mb_search_bar, width=36, font=("Segoe UI", 10),
                         bg=C["bg_card"], fg=C["text_dark"], relief="flat",
                         insertbackground=C["primary"])
    mb_search.pack(side="left", ipady=10, padx=4)
    mb_search.insert(0, "Rechercher par nom ou prénom...")
    mb_search.bind("<FocusIn>", lambda e: mb_search.delete(0,"end") if mb_search.get().startswith("Rechercher") else None)

    tk.Label(mb_right, text="Liste des Membres",
             font=("Segoe UI", 14, "bold"), bg=C["bg_light"], fg=C["text_dark"]).pack(anchor="w", pady=(0, 6))

    cols_membres = ("id", "nom", "prenom", "email", "telephone", "date_inscription")
    mb_widths   = [50, 130, 130, 200, 130, 140]
    mb_anchors  = ["center","w","w","w","center","center"]
    tree_membres, _ = make_pro_table(mb_right, cols_membres, mb_widths, mb_anchors)

    def reload_membres():
        cursor.execute("SELECT * FROM membres")
        insert_rows(tree_membres, cursor.fetchall())

    def ajouter_membre():
        if not check_connexion(): return
        if not valider_champs(entries_membres, [True]*5, labels_membres): return
        try:
            email = entries_membres[2].get().strip()
            cursor.execute("SELECT COUNT(*) FROM membres WHERE email=%s", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Doublon", "Email déjà utilisé !")
                return
            vals = tuple(e.get().strip() for e in entries_membres)
            cursor.execute("INSERT INTO membres (nom,prenom,email,telephone,date_inscription) VALUES (%s,%s,%s,%s,%s)", vals)
            conn.commit(); reload_membres(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Membre ajouté avec succès !")
            for e in entries_membres: e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_membre():
        if not check_connexion(): return
        try:
            sel = tree_membres.selection()[0]
            mid = tree_membres.item(sel)['values'][0]
            cursor.execute("UPDATE membres SET nom=%s,prenom=%s,email=%s,telephone=%s,date_inscription=%s WHERE id=%s",
                           [e.get().strip() for e in entries_membres] + [mid])
            conn.commit(); reload_membres(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Membre modifié !")
        except IndexError:
            messagebox.showwarning("Sélection", "Sélectionnez un membre dans la table")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_membre():
        if not check_connexion(): return
        if not messagebox.askyesno("Confirmation", "Supprimer ce membre définitivement ?"): return
        try:
            sel = tree_membres.selection()[0]
            mid = tree_membres.item(sel)['values'][0]
            cursor.execute("DELETE FROM membres WHERE id=%s", (mid,))
            conn.commit(); reload_membres(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Membre supprimé !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rechercher_membre():
        q = mb_search.get().strip()
        if q.startswith("Rechercher"): q = ""
        tree_membres.delete(*tree_membres.get_children())
        if q:
            cursor.execute("SELECT * FROM membres WHERE nom LIKE %s OR prenom LIKE %s", (f"%{q}%", f"%{q}%"))
        else:
            cursor.execute("SELECT * FROM membres")
        insert_rows(tree_membres, cursor.fetchall())

    def fill_membres_form(e):
        try:
            sel = tree_membres.selection()[0]
            vals = tree_membres.item(sel)['values']
            for i, ent in enumerate(entries_membres):
                ent.delete(0, tk.END)
                ent.insert(0, str(vals[i+1]))
        except: pass

    tree_membres.bind("<<TreeviewSelect>>", fill_membres_form)

    mb_btn_grid = tk.Frame(mb_left, bg=C["bg_card"])
    mb_btn_grid.pack(fill="x", padx=16, pady=8)
    action_btn(mb_btn_grid, "➕  Ajouter", C["success"], C["success_dark"], ajouter_membre).pack(fill="x", pady=3)
    action_btn(mb_btn_grid, "✏️  Modifier", C["primary"], C["primary_dark"], modifier_membre).pack(fill="x", pady=3)
    action_btn(mb_btn_grid, "🗑  Supprimer", C["danger"], C["danger_dark"], supprimer_membre).pack(fill="x", pady=3)

    action_btn(mb_search_bar, "Rechercher", C["primary"], C["primary_dark"], rechercher_membre).pack(side="left", padx=6, pady=8)
    action_btn(mb_search_bar, "↻ Reset", C["info"], C["info_dark"], reload_membres).pack(side="left", pady=8)

    # ========================
    # ONGLET EMPRUNTS
    # ========================
    emprunts_tab = ttk.Frame(notebook)
    notebook.add(emprunts_tab, text="  🔄 Emprunts  ")

    em_main = tk.Frame(emprunts_tab, bg=C["bg_light"])
    em_main.pack(fill="both", expand=True)

    em_left = tk.Frame(em_main, bg=C["bg_card"], width=340,
                       highlightbackground=C["border"], highlightthickness=1)
    em_left.pack(side="left", fill="y", padx=(12, 6), pady=12)
    em_left.pack_propagate(False)

    tk.Label(em_left, text="🔄  Gestion des Emprunts",
             font=("Segoe UI", 13, "bold"), bg=C["bg_card"], fg=C["text_dark"]).pack(
             pady=(20, 4), padx=16, anchor="w")
    tk.Frame(em_left, bg=C["border"], height=1).pack(fill="x", padx=16, pady=8)

    labels_emprunts = ["Membre", "Livre", "Date Emprunt", "Date Retour Prévue", "Retour Effectué"]
    entries_emprunts = []
    em_form = tk.Frame(em_left, bg=C["bg_card"])
    em_form.pack(fill="x")
    em_form.columnconfigure(0, weight=1)

    for i, label in enumerate(labels_emprunts):
        if label in ("Membre", "Livre"):
            ent = make_field(em_form, label, i, is_combo=True, values=[], default="")
        elif label == "Retour Effectué":
            ent = make_field(em_form, label, i, is_combo=True, values=["Oui","Non"], default="Non")
        else:
            ent = make_field(em_form, label, i)
        entries_emprunts.append(ent)

    tk.Frame(em_left, bg=C["border"], height=1).pack(fill="x", padx=16, pady=12)

    em_right = tk.Frame(em_main, bg=C["bg_light"])
    em_right.pack(side="right", fill="both", expand=True, padx=(6, 12), pady=12)

    em_search_bar = tk.Frame(em_right, bg=C["bg_card"],
                             highlightbackground=C["border"], highlightthickness=1)
    em_search_bar.pack(fill="x", pady=(0, 8))
    tk.Label(em_search_bar, text="🔍", bg=C["bg_card"], fg=C["text_mid"],
             font=("Segoe UI", 11)).pack(side="left", padx=(12, 4))
    em_search = ttk.Combobox(em_search_bar, width=34, state="readonly")
    em_search.pack(side="left", ipady=6, padx=4)

    tk.Label(em_right, text="Liste des Emprunts",
             font=("Segoe UI", 14, "bold"), bg=C["bg_light"], fg=C["text_dark"]).pack(anchor="w", pady=(0, 6))

    cols_emprunts = ("id", "id_membre", "id_livre", "date_emprunt", "date_retour", "retour_effectue")
    em_widths  = [50, 90, 80, 140, 140, 130]
    em_anchors = ["center","center","center","center","center","center"]
    tree_emprunts, _ = make_pro_table(em_right, cols_emprunts, em_widths, em_anchors)

    def charger_listes_emprunts():
        if not check_connexion(): return
        try:
            cursor.execute("SELECT id, nom, prenom FROM membres ORDER BY nom")
            entries_emprunts[0]['values'] = [f"{r[0]} - {r[1]} {r[2]}" for r in cursor.fetchall()]
            cursor.execute("SELECT id, titre FROM livres WHERE disponible='Oui' ORDER BY titre")
            entries_emprunts[1]['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
            # Aussi pour la recherche
            cursor.execute("SELECT id, nom, prenom FROM membres ORDER BY nom")
            em_search['values'] = ["Tous les membres"] + [f"{r[0]} - {r[1]} {r[2]}" for r in cursor.fetchall()]
            em_search.set("Tous les membres")
        except: pass

    def reload_emprunts():
        cursor.execute("SELECT * FROM emprunts")
        rows = cursor.fetchall()
        tag_map = {"Oui": "actif", "Non": "nonDispo"}
        insert_rows(tree_emprunts, rows, special_col=5, tag_map=tag_map)

    def ajouter_emprunt():
        if not check_connexion(): return
        if not valider_champs(entries_emprunts, [True]*5, labels_emprunts): return
        try:
            id_membre = entries_emprunts[0].get().split(" - ")[0]
            id_livre  = entries_emprunts[1].get().split(" - ")[0]
            date_emp  = entries_emprunts[2].get().strip()
            date_ret  = entries_emprunts[3].get().strip()
            retour    = entries_emprunts[4].get().strip()

            cursor.execute("SELECT COUNT(*) FROM emprunts WHERE id_livre=%s AND retour_effectue='Non'", (id_livre,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Indisponible", "Ce livre est déjà emprunté !")
                return
            if date_ret < date_emp:
                messagebox.showwarning("Erreur", "La date de retour est antérieure à l'emprunt !")
                return
            cursor.execute("INSERT INTO emprunts (id_membre,id_livre,date_emprunt,date_retour,retour_effectue) VALUES (%s,%s,%s,%s,%s)",
                           (id_membre, id_livre, date_emp, date_ret, retour))
            dispo = "Non" if retour == "Non" else "Oui"
            cursor.execute("UPDATE livres SET disponible=%s WHERE id=%s", (dispo, id_livre))
            conn.commit()
            reload_emprunts(); reload_livres(); load_dashboard()
            charger_listes_emprunts()
            messagebox.showinfo("✅ Succès", "Emprunt enregistré !")
            for e in entries_emprunts:
                if hasattr(e, "set"): e.set("")
                else: e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def retourner_livre():
        if not check_connexion(): return
        try:
            sel = tree_emprunts.selection()[0]
            eid = tree_emprunts.item(sel)['values'][0]
            ilv = tree_emprunts.item(sel)['values'][2]
            today = datetime.today().strftime('%Y-%m-%d')
            cursor.execute("UPDATE emprunts SET retour_effectue='Oui', date_retour=%s WHERE id=%s", (today, eid))
            cursor.execute("UPDATE livres SET disponible='Oui' WHERE id=%s", (ilv,))
            conn.commit()
            reload_emprunts(); reload_livres(); load_dashboard()
            charger_listes_emprunts()
            messagebox.showinfo("✅ Succès", "Livre retourné avec succès !")
        except IndexError:
            messagebox.showwarning("Sélection", "Sélectionnez un emprunt dans la table")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_emprunt():
        if not check_connexion(): return
        try:
            sel = tree_emprunts.selection()[0]
            eid = tree_emprunts.item(sel)['values'][0]
            cursor.execute("UPDATE emprunts SET id_membre=%s,id_livre=%s,date_emprunt=%s,date_retour=%s,retour_effectue=%s WHERE id=%s",
                           [e.get().strip() for e in entries_emprunts] + [eid])
            conn.commit(); reload_emprunts(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Emprunt modifié !")
        except IndexError:
            messagebox.showwarning("Sélection", "Sélectionnez un emprunt dans la table")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_emprunt():
        if not check_connexion(): return
        if not messagebox.askyesno("Confirmation", "Supprimer cet emprunt définitivement ?"): return
        try:
            sel = tree_emprunts.selection()[0]
            eid = tree_emprunts.item(sel)['values'][0]
            cursor.execute("DELETE FROM emprunts WHERE id=%s", (eid,))
            conn.commit(); reload_emprunts(); load_dashboard()
            messagebox.showinfo("✅ Succès", "Emprunt supprimé !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rechercher_emprunt():
        q = em_search.get().strip()
        tree_emprunts.delete(*tree_emprunts.get_children())
        if q and q != "Tous les membres":
            id_membre = q.split(" - ")[0]
            cursor.execute("SELECT * FROM emprunts WHERE id_membre=%s", (id_membre,))
        else:
            cursor.execute("SELECT * FROM emprunts")
        tag_map = {"Oui": "actif", "Non": "nonDispo"}
        insert_rows(tree_emprunts, cursor.fetchall(), special_col=5, tag_map=tag_map)

    em_btn_grid = tk.Frame(em_left, bg=C["bg_card"])
    em_btn_grid.pack(fill="x", padx=16, pady=8)
    action_btn(em_btn_grid, "➕  Emprunter", C["success"], C["success_dark"], ajouter_emprunt).pack(fill="x", pady=3)
    action_btn(em_btn_grid, "📥  Retourner", C["purple"], C["purple_dark"], retourner_livre).pack(fill="x", pady=3)
    action_btn(em_btn_grid, "✏️  Modifier",  C["primary"], C["primary_dark"], modifier_emprunt).pack(fill="x", pady=3)
    action_btn(em_btn_grid, "🗑  Supprimer", C["danger"],  C["danger_dark"],  supprimer_emprunt).pack(fill="x", pady=3)

    action_btn(em_search_bar, "Rechercher", C["primary"], C["primary_dark"], rechercher_emprunt).pack(side="left", padx=6, pady=8)
    action_btn(em_search_bar, "↻ Tous", C["info"], C["info_dark"], reload_emprunts).pack(side="left", pady=8)

    # Légende couleurs
    legend = tk.Frame(em_right, bg=C["bg_light"])
    legend.pack(anchor="w", pady=(6, 0))
    tk.Label(legend, text="Légende :", bg=C["bg_light"], fg=C["text_mid"],
             font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0,8))
    for txt, color in [("✅ Retourné", C["success"]), ("🔄 En cours", C["warning"]), ("⚠️ Retard", C["danger"])]:
        tk.Label(legend, text=txt, bg=color, fg="white",
                 font=("Segoe UI", 8, "bold"), padx=8, pady=2).pack(side="left", padx=4)

    # ========================
    # CHARGEMENT INITIAL
    # ========================
    charger_listes_emprunts()
    reload_livres()
    reload_membres()
    reload_emprunts()

    root.mainloop()
    if conn:
        conn.close()


# ========================
# POINT D'ENTRÉE
# ========================
show_login()