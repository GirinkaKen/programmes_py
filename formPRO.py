# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:45:22 2026

@author: PC
"""

import tkinter as tk
from tkinter import messagebox


class FormulaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire d'inscription")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Frame principale
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Titre
        tk.Label(frame, text="Formulaire d'inscription", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Champs
        self.nom = self.creer_champ(frame, "Nom", 1)
        self.prenom = self.creer_champ(frame, "Prénom", 2)
        self.age = self.creer_champ(frame, "Âge", 3)
        self.ville = self.creer_champ(frame, "Ville", 4)

        # Bouton
        tk.Button(frame, text="Soumettre", command=self.soumettre,
                  font=("Arial", 12), bg="#007BFF", fg="white",
                  padx=10, pady=5).grid(row=5, column=0, columnspan=2, pady=20)

    def creer_champ(self, parent, label, row):
        tk.Label(parent, text=label + " :", anchor="w").grid(row=row, column=0, sticky="w", pady=5)
        entry = tk.Entry(parent, width=25)
        entry.grid(row=row, column=1, pady=5)
        return entry

    def soumettre(self):
        n = self.nom.get().strip()
        p = self.prenom.get().strip()
        a = self.age.get().strip()
        v = self.ville.get().strip()

        # Validation
        if not (n and p and a and v):
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")
            return

        if not a.isdigit():
            messagebox.showerror("Erreur", "L'âge doit être un nombre.")
            return

        # Succès
        messagebox.showinfo(
            "Succès",
            f"Bienvenue {p} {n} !\nÂge : {a} ans\nVille : {v}"
        )

        # Reset des champs
        self.reset()

    def reset(self):
        self.nom.delete(0, tk.END)
        self.prenom.delete(0, tk.END)
        self.age.delete(0, tk.END)
        self.ville.delete(0, tk.END)


# Point d'entrée
if __name__ == "__main__":
    root = tk.Tk()
    app = FormulaireApp(root)
    root.mainloop()