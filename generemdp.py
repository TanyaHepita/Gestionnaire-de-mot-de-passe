import tkinter as tk
from tkinter import messagebox
from random import choice

class GenereMdp:
    def __init__(self, master, app_instance):
        self.master = master
        self.master.title("Générateur de mot de passe")
        self.app_instance = app_instance

        # Les cases à cocher
        self.caseMinuscules_var = tk.BooleanVar()
        self.caseMinuscules = tk.Checkbutton(self.master, text="Minuscules", variable=self.caseMinuscules_var)
        self.caseMajuscules_var = tk.BooleanVar()
        self.caseMajuscules = tk.Checkbutton(self.master, text="Majuscules", variable=self.caseMajuscules_var)
        self.caseChiffres_var = tk.BooleanVar()
        self.caseChiffres = tk.Checkbutton(self.master, text="Chiffres", variable=self.caseChiffres_var)
        self.caseSymboles_var = tk.BooleanVar()
        self.caseSymboles = tk.Checkbutton(self.master, text="Symboles", variable=self.caseSymboles_var)

        # Les boutons
        self.boutonQuitter = tk.Button(self.master, text="Quitter", command=self.quitter)
        self.boutonCopier = tk.Button(self.master, text="Copier", command=self.copier)
        self.boutonGenerer = tk.Button(self.master, text="Générer", command=self.generer)

        # Le champ de texte
        self.champTexte = tk.Entry(self.master, width=30)

        # La glissière
        self.glissiereTaille = tk.Scale(self.master, from_=8, to=30, orient=tk.HORIZONTAL, label="Taille : 8", command=self.changerTailleMotDePasse)

        # Positionnement des éléments
        self.caseMajuscules.grid(row=0, column=0, pady=5)
        self.glissiereTaille.grid(row=0, column=2, pady=5, columnspan=3)
        self.caseMinuscules.grid(row=0, column=1, pady=5)
        self.caseChiffres.grid(row=1, column=0, pady=5)
        self.caseSymboles.grid(row=1, column=1, pady=5)
        self.champTexte.grid(row=2, column=1, pady=10)
        self.boutonQuitter.grid(row=3, column=2, pady=5)
        self.boutonCopier.grid(row=3, column=0, pady=5)
        self.boutonGenerer.grid(row=3, column=1, pady=5)

        # Configuration de la fenêtre
        self.master.protocol("WM_DELETE_WINDOW", self.quitter)
        self.caseMinuscules.select()
        self.caseChiffres.select()

    def quitter(self):
        self.master.destroy()

    def copier(self):
        mot_de_passe = self.champTexte.get()
        if mot_de_passe:
            self.master.clipboard_clear()
            self.master.clipboard_append(mot_de_passe)
            self.master.update()
            messagebox.showinfo("Copier", f"Le mot de passe a été copié dans le presse-papiers:\n{mot_de_passe}", parent=self.master)
        else:
            messagebox.showwarning("Mot de passe vide", "Le champ de mot de passe est vide.", parent=self.master)
        return mot_de_passe

    #ICI POUR CHANGER ALGO GENERATION MDP
    def genererMotDePasse(self, tailleMotDePasse=8, minuscules=True, majuscules=True, chiffres=True, symboles=True):
        caracteres = ""
        if minuscules:
            caracteres += "abcdefghijklmnopqrstuvwxyz"
        if majuscules:
            caracteres += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if chiffres:
            caracteres += "0123456789"
        if symboles:
            caracteres += "&~#{([-|_\^@)=+$]}*%!/:.;?,"
        motDePasse = "".join(choice(caracteres) for _ in range(tailleMotDePasse))
        return motDePasse

    def generer(self):
        taille_mot_de_passe = self.glissiereTaille.get()
        minuscules = False
        majuscules = False
        chiffres = False
        symboles = False

        if self.caseMinuscules_var.get():
            minuscules = True
        if self.caseMajuscules_var.get():
            majuscules = True
        if self.caseChiffres_var.get():
            chiffres = True
        if self.caseSymboles_var.get():
            symboles = True

        mot_de_passe = self.genererMotDePasse(taille_mot_de_passe, minuscules, majuscules, chiffres, symboles)
        self.champTexte.delete(0, tk.END)
        self.champTexte.insert(0, mot_de_passe)
    
    def changerTailleMotDePasse(self, event):
        taille = self.glissiereTaille.get()
        self.glissiereTaille.configure(label=f"Taille : {taille}")


