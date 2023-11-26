import tkinter as tk
from tkinter import ttk, messagebox
from newpassword import NewPasswordWindow
import sqlite3



class PasswordManager:
    """
        Initialise l'interface du gestionnaire

        Créer les boutons et affiche les mots de passe de la base de donnée
    
    """
    def __init__(self, master, main_instance):
        self.master = master
        self.master.title("Gestionnaire de Mot de Passe")
        self.master.configure(bg="#b0c4de")
        self.main_instance = main_instance

        # Titre pour la création du nouveau mot de passe
        new_password_label = tk.Label(self.master, text="Bienvenue sur votre Gestionnaire de mots de passe", font=("Helvetica", 16, "bold"), anchor="e", background="#b0c4de")
        new_password_label.pack(pady=10)

        # Création du tableau
        self.tree = ttk.Treeview(self.master, columns=("Titre", "Pseudo", "URL"), show="headings")

        # Configurer les en-têtes de colonnes
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Pseudo", text="Pseudo")
        #self.tree.heading("Mot de Passe", text="Mot de Passe")
        self.tree.heading("URL", text="URL")

        # Configurer la largeur des colonnes
        self.tree.column("Titre", width=150)
        self.tree.column("Pseudo", width=150)
        #self.tree.column("Mot de Passe", width=150)
        self.tree.column("URL", width=200)

        # Récupérer les données de la base de données et les afficher dans le treeview 
        self.update_treeview() 

        # Ajouter le tableau à la fenêtre
        self.tree.pack(side=tk.TOP, anchor=tk.W, pady=50, padx=10)

        # Bouton pour ouvrir la fenêtre de création de mot de passe
        open_new_password_button = tk.Button(self.master, text="Ajouter un nouveau mot de passe", command=self.open_new_password_window)
        open_new_password_button.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        # Bouton pour ouvrir la fenêtre de création de mot de passe
        open_modif_password_button = tk.Button(self.master, text="Modifier", command=self.edit_new_password_window)
        open_modif_password_button.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        # Bouton pour copier
        copy_button = tk.Button(self.master, text="Copier mot de passe", command=self.copy_selected)
        copy_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)

        # Bouton pour supprimer
        delete_button = tk.Button(self.master, text="Supprimer", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)

        modif_maitre_button = tk.Button(self.master, text="Modifier le mot de passe maitre", command= self.modify_master_password)
        modif_maitre_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)
        #si on ouvre il faut fermer la fenetre actuelle

    '''
        Fait la mise à jour de l'affichage des mots de passe 

    '''
    def update_treeview(self):
            # Effacer toutes les lignes du treeview
            for item in self.tree.get_children(): 
                self.tree.delete(item)
            # Récupérer les données de la base de données et les afficher dans le treeview
            cursor.execute('SELECT * FROM mots_de_passe')
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=(row[1], row[2], row[4]))

    '''
        Ouvre password_window en mode nouveau

    '''
    def open_new_password_window(self):
        new_password_window = tk.Toplevel(self.master)
        new_password_window.geometry("600x500")  # taille de la fenêtre
        new_password_app = NewPasswordWindow(new_password_window, self, "new")

    def modify_master_password(self):
        self.master.destroy()
        self.main_instance.change_master_password()

    '''
        Ouvre password_window en mode modifier

        Verifie si un mot de passe à été selectionné pour la modification et 
        envoie les informations de la ligne selectionnées à NewPasswordWindow
    '''
    def edit_new_password_window(self):
        selected_item = self.tree.selection()

        if selected_item:
            edit_password_window = tk.Toplevel(self.master)
            edit_password_window.geometry("600x500")  # taille de la fenêtre
            edit_password_app = NewPasswordWindow(edit_password_window, self, "modifier")
        else:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un élément à modifier.")

    
   
    """
        Copie le mot de passe

        Recupère le mot de passe selectionné et le copie dans le presse papier

    """
    def copy_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            mot_de_passe_id = None
            if item_values:
                cursor.execute('SELECT mot_de_passe FROM mots_de_passe WHERE titre = ? AND utilisateur = ? AND url = ?',
                           (item_values[0], item_values[1], item_values[2]))
                result = cursor.fetchone()
                if result :
                    password =  result  # Récupérer le mot de passe
                    self.master.clipboard_clear()
                    self.master.clipboard_append(password)
                    self.master.update()
                    
                    
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner une ligne pour copier.")



    """
        Supprime mot de passe 

        Une fois la ligne selectionnée le mot passe entier est supprimé de la base de donnée
    """
    def delete_selected(self):
        #reponse = messagebox.askquestion("Question", "Voulez-vous continuer?")
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            mot_de_passe_id = None
            if item_values:
                cursor.execute('SELECT id FROM mots_de_passe WHERE titre = ? AND utilisateur = ? AND url = ?',
                            (item_values[0], item_values[1], item_values[2]))
                result = cursor.fetchone()
                if result:
                    mot_de_passe_id = result[0]
            # Vérifier si l'ID du mot de passe a été trouvé
            if mot_de_passe_id:
                # Supprimer le mot de passe de la base de données
                self.supprimer_mot_de_passe(mot_de_passe_id)
                # Supprimer l'élément sélectionné du treeview 
                self.tree.delete(selected_item)
            else:
                messagebox.showwarning("Erreur", "Impossible de trouver l'ID du mot de passe.") 
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner une ligne pour supprimer.")

    """
        Supprime mot de passe de la base
    """
    def supprimer_mot_de_passe(self, mot_de_passe_id):
        cursor.execute('DELETE FROM mots_de_passe WHERE id = ?', (mot_de_passe_id,))
        conn.commit()

	
#-------------------------------------------Main-----------------------
	
conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la connexion avec la base de données

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

