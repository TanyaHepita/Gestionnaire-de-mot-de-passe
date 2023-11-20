import tkinter as tk
from tkinter import messagebox
import re
from generemdp import GenereMdp
import sqlite3

conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la conncexion avec la base de données

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

class NewPasswordWindow:
    def __init__(self, master, app_instance):
        self.master = master
        self.master.title("Nouveau Mot de Passe")
        self.app_instance = app_instance

        # Entrée pour le nom du mot de passe
        password_name_label = tk.Label(self.master, text="Titre :", font=('Helvetica', 10, 'bold'))
        password_name_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_name_entry = tk.Entry(self.master)
        self.password_name_entry.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        # Entrée pour le pseudo
        password_pseudo_label = tk.Label(self.master, text="Votre pseudo:", font=('Helvetica', 10, 'bold'))
        password_pseudo_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_pseudo_entry = tk.Entry(self.master)
        self.password_pseudo_entry.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        # Entrée pour le nouveau mot de passe
        password_label = tk.Label(self.master, text="Nouveau mot de passe:", font=('Helvetica', 10, 'bold'))
        password_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_entry = tk.Entry(self.master)
        self.password_entry.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        # Confirmation pour le nouveau mot de passe
        password_label_conf = tk.Label(self.master, text="Confirmer votre mot de passe:", font=('Helvetica', 10, 'bold'))
        password_label_conf.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_entry_conf = tk.Entry(self.master, show="*")
        self.password_entry_conf.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.NW)

        # Option pour afficher/masquer le mot de passe
        self.show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(self.master, text="Afficher les mots de passe", variable=self.show_password_var,
                                                command=self.toggle_password_visibility)
        show_password_checkbox.pack(pady=5, anchor=tk.NW)

        # Bouton pour générer un mot de passe fort
        generate_password_button = tk.Button(self.master, text="Générer un mot de passe fort", command=self.open_generate_password_window)
        generate_password_button.pack(pady=20, anchor=tk.NW)

        # Bouton pour valider et sauvegarder le mot de passe
        validate_button = tk.Button(self.master, text="Valider", command=self.save_password)
        validate_button.pack(pady=10, padx=70, anchor=tk.NW)

    def open_generate_password_window(self):
        generate_password_window = tk.Toplevel(self.master)
        generate_password_window.geometry("550x200")  # taille de la fenêtre
        generate_password_app = GenereMdp(generate_password_window, self)
      
          
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
            self.password_entry_conf.config(show="")
        else:
            self.password_entry.config(show="*")
            self.password_entry_conf.config(show="*")
    
    def ajouter_mot_de_passe(self, site, utilisateur, mot_de_passe, note=None):
        cursor.execute('''
                INSERT INTO mots_de_passe (site, utilisateur, mot_de_passe)
                VALUES (?, ?, ?) ''', (str(site), str(utilisateur), str(mot_de_passe)))
        conn.commit()
        conn.close()
    
    def save_password(self):
        # Récupérer les valeurs des entrées
        title = self.password_name_entry.get()
        pseudo = self.password_pseudo_entry.get()
        password = self.password_entry.get()
        password_conf = self.password_entry_conf.get()

        # Vérifier si les champs sont vides
        if not title or not pseudo or not password:
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.", parent=self.master)
            return
        if password_conf != password:
            messagebox.showwarning("Mot de passe incompatible", "Veuillez mettre les mêmes mots de passe.", parent=self.master)
            return
        if not self.is_strong_password(password):
            messagebox.showwarning("Mot de passe faible", "Le mot de passe doit avoir au moins 8 caractères, des majuscules, des minuscules et des caractères spéciaux.", parent=self.master)
            return

        # Ajouter les nouvelles données à l'exemple_data (ou à ta base de données)
        self.ajouter_mot_de_passe(title,pseudo,password)
        self.app_instance.update_treeview()
        

        # Afficher un message de succès
        messagebox.showinfo("Succès", "Mot de passe ajouté avec succès à la base de données.", parent=self.master)

        # Fermer la fenêtre
        self.master.destroy()

    def is_strong_password(self, password):
        # Utiliser une expression régulière pour vérifier la force du mot de passe
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-_+=]).{8,}$')
        return bool(regex.match(password))

