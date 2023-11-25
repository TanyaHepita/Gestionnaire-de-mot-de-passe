import tkinter as tk
from tkinter import messagebox
import re
from generemdp import GenereMdp
from urllib.parse import urlparse
import sqlite3

conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la connexion avec la base de données
#A voir comment recuperer celle de interface

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor() 

conseil = False 
class NewPasswordWindow:
    def __init__(self, master, app_instance, mode):
        self.master = master
        self.mode = mode
        self.master.title("Nouveau Mot de Passe")
        self.app_instance = app_instance
        

        selected_item = self.app_instance.tree.selection()
        item_values = self.app_instance.tree.item(selected_item, "values")
        
        
        

        # Entrée pour le nom du mot de passe
        password_name_label = tk.Label(self.master, text="Titre :", font=('Helvetica', 10, 'bold'))
        password_name_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_name_entry = tk.Entry(self.master)
        if selected_item and mode == "modifier":
            self.password_name_entry.delete(0, tk.END)
            self.password_name_entry.insert(0, item_values[0])
            
        self.password_name_entry.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        # Entrée pour l'url
        password_URL_label = tk.Label(self.master, text="URL:", font=('Helvetica', 10, 'bold'))
        password_URL_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_URL_entry = tk.Entry(self.master)
        if selected_item and mode == "modifier":
            self.password_URL_entry.delete(0, tk.END)
            self.password_URL_entry.insert(0, item_values[2])  
       
        self.password_URL_entry.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        # Entrée pour le pseudo du mot de passe
        password_pseudo_label = tk.Label(self.master, text="Votre pseudo:", font=('Helvetica', 10, 'bold'))
        password_pseudo_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_pseudo_entry = tk.Entry(self.master)
        if selected_item and mode == "modifier":
            self.password_pseudo_entry.delete(0, tk.END)
            self.password_pseudo_entry.insert(0, item_values[1])  
       
        self.password_pseudo_entry.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        # Entrée pour le nouveau mot de passe
        password_label = tk.Label(self.master, text="Nouveau mot de passe:", font=('Helvetica', 10, 'bold'))
        password_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.password_entry = tk.Entry(self.master, show="*")
        if selected_item and mode == "modifier":
            mot_de_passe_id = None
            if item_values:
                cursor.execute('SELECT mot_de_passe FROM mots_de_passe WHERE titre = ? AND utilisateur = ? AND url = ?',
                            (item_values[0], item_values[1], item_values[2]))
                result = cursor.fetchone()
                if result:
                    password = result[0]
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

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
   
   
    def ajouter_mot_de_passe(self, titre, utilisateur, mot_de_passe, url, note=None):
        
        cursor.execute('''
                INSERT INTO mots_de_passe (titre, utilisateur, mot_de_passe, url)
                VALUES (?, ?, ?, ?) ''', (str(titre), str(utilisateur), str(mot_de_passe), str(url)))
        conn.commit()
        #conn.close() -- Mis en commentaire car avec on ne peut pas mettre 2 mots de passe à la suite car la connexion se ferme sans se reouvrir

    
    def modifier_mot_de_passe(self, titre, utilisateur, mot_de_passe, url):
        selected_item = self.app_instance.tree.selection()
        if selected_item:
            item_values = self.app_instance.tree.item(selected_item, "values")
            mot_de_passe_id = None
            if item_values:
                cursor.execute('SELECT id FROM mots_de_passe WHERE titre = ? AND utilisateur = ? AND url = ?',
                            (item_values[0], item_values[1], item_values[2]))
                result = cursor.fetchone()
                if result:
                    mot_de_passe_id = result[0] #prend l'id du mot de passe
            # Vérifier si l'ID du mot de passe a été trouvé
            if mot_de_passe_id:
                # Supprimer le mot de passe de la base de données pour rajouter le nouveau apres 
                #Car pas possivle modif in sqlite3 (A VERIFIER)
                cursor.execute('DELETE FROM mots_de_passe WHERE id = ?', (mot_de_passe_id,))
                conn.commit()
                # Supprimer l'élément sélectionné du treeview 
                self.app_instance.tree.delete(selected_item)
            self.ajouter_mot_de_passe(titre, utilisateur, mot_de_passe, url)
        
    

    def save_password(self):
        # Récupérer les valeurs des entrées
        title = self.password_name_entry.get()
        pseudo = self.password_pseudo_entry.get()
        password = self.password_entry.get()
        password_conf = self.password_entry_conf.get()
        url = self.password_URL_entry.get()
        global conseil
      
        # Vérifier si les champs sont vides
        if not title or not pseudo or not password or not url:
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.", parent=self.master)
            return
        if password_conf != password:
            messagebox.showwarning("Mot de passe incompatible", "Veuillez mettre les mêmes mots de passe.", parent=self.master)
            return
        
        if not self.is_strong_password(password) and not conseil:
            messagebox.showwarning("Mot de passe faible", "Conseil pour mot de passe fort doit avoir au moins 8 caractères, des majuscules, des minuscules et des caractères spéciaux.", parent=self.master)
            conseil = True
            return
        
        if not self.is_valid_url(url): 
            messagebox.showwarning("URL non valide", "Veuillez écrire une URL valide", parent=self.master)
            return
        if self.mode == "new" :
            # Ajouter les nouvelles données à l'exemple_data (ou à ta base de données)
            self.ajouter_mot_de_passe(title, pseudo, password, url)
            self.app_instance.update_treeview() 
            # Afficher un message de succès
            messagebox.showinfo("Succès", "Mot de passe ajouté avec succès à la base de données.", parent=self.master)
        else :
            self.modifier_mot_de_passe(title,pseudo,password, url)
            self.app_instance.update_treeview() 
            # Afficher un message de succès
            messagebox.showinfo("Succès", "Mot de passe modifié avec succès à la base de données.", parent=self.master)

        # Fermer la fenêtre
        self.master.destroy()

    """
        Vérifie si le mot de passe passé est fort, cependant n'est utilisé
        que pour conseil car pour des mdp de banque ex: il ne faut que des chiffres      
    """ 
    def is_strong_password(self, password):
        # Utiliser une expression régulière pour vérifier la force du mot de passe
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-_+=]).{8,}$')
        return bool(regex.match(password))

    """
        Verifie si l'url est valide
        Utilise urlparse pour décomposer l'URL en différentes 
         parties et vérifier si les parties essentielles sont présentes

    """ 
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False