import tkinter as tk
from tkinter import messagebox
from random import choice
from random import sample
import string 

class GenereMdp:
    """
        Affiche la fenetre de generation de mot de passe
        @master: fenetre créée
        @new_instance : instance de la classe interface
    """
    def __init__(self, master, new_instance):
        self.master = master
        self.master.title("Générateur de mot de passe")
        self.new_instance = new_instance

        # Les cases à cocher
        self.caseMinuscules_var = tk.BooleanVar()
        self.caseMinuscules = tk.Checkbutton(self.master, text="Minuscules", variable=self.caseMinuscules_var)
        self.caseMajuscules_var = tk.BooleanVar()
        self.caseMajuscules = tk.Checkbutton(self.master, text="Majuscules", variable=self.caseMajuscules_var)
        self.caseChiffres_var = tk.BooleanVar()
        self.caseChiffres = tk.Checkbutton(self.master, text="Chiffres", variable=self.caseChiffres_var)
        self.caseSymboles_var = tk.BooleanVar()
        self.caseSymboles = tk.Checkbutton(self.master, text="Symboles", variable=self.caseSymboles_var)

        self.caseMinuscules.select()  # Pour cocher par défaut
        self.caseMajuscules.select()  
        self.caseChiffres.select()  
        self.caseSymboles.select()  

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
    
    """
        Quitte la fenetre
    """
    def quitter(self):
        self.master.destroy()


    """
        Copie le mot de passe généré dans le presse papier
        et dans le champs mot de passe
    """
    def copier(self):
        mot_de_passe = self.champTexte.get()
        if mot_de_passe:
            self.master.clipboard_clear()
            self.master.clipboard_append(mot_de_passe)
            self.master.update()
            self.new_instance.password_entry.delete(0, tk.END)
            self.new_instance.password_entry.insert(0, mot_de_passe)
            self.new_instance.password_entry_conf.delete(0, tk.END)
            self.new_instance.password_entry_conf.insert(0, mot_de_passe)
        else:
            messagebox.showwarning("Mot de passe vide", "Le champ de mot de passe est vide.", parent=self.master)
        return mot_de_passe




	
    """
        Génère un mot de passe fort
        @args: bool (true si option cochée, false sinon)
        @return: mot de passe généré
    """
    def genererMotDePasse(self, tailleMotDePasse=8, minuscules=True, majuscules=True, chiffres=True, symboles=True):  
        caracteres = ""
        motDePasse = ""
        if minuscules:
            caracteres += string.ascii_lowercase
            motDePasse += choice(string.ascii_lowercase)
        if majuscules:
            caracteres += string.ascii_uppercase
            motDePasse += choice(string.ascii_uppercase)
        if chiffres:
            caracteres += string.digits
            motDePasse += choice(string.digits)
        if symboles:
            caracteres += "&~#{([-|_\^@)=+$]}*%!/:.;?,"
            motDePasse += choice("&~#{([-|_\^@)=+$]}*%!/:.;?,")


        motDePasse += "".join(choice(caracteres) for _ in range(tailleMotDePasse - len(motDePasse)))

        # Mélanger le mot de passe pour plus de sécurité
        motDePasse = ''.join(sample(motDePasse, len(motDePasse)))
        
        return motDePasse


    """
        Prend en compte les choix de l'utilisateur et génère son mot de passe
    """
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
        if not majuscules and not minuscules and  not chiffres and not symboles:
            messagebox.showwarning("Impossible de générer", "Veuillez cocher les cases.", parent=self.master)
            return

        mot_de_passe = self.genererMotDePasse(taille_mot_de_passe, minuscules, majuscules, chiffres, symboles)
        self.champTexte.delete(0, tk.END)
        self.champTexte.insert(0, mot_de_passe)
    
    """
        Met à jour l'affichage de la taille du mot de passe
        @event (tk.Event): L'événement associé au changement de valeur de la glissière.
    """
    def changerTailleMotDePasse(self, event):
        taille = self.glissiereTaille.get()
        self.glissiereTaille.configure(label=f"Taille : {taille}")
