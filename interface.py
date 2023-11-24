import tkinter as tk
from tkinter import ttk, messagebox
from newpassword import NewPasswordWindow
import sqlite3



class PasswordManager:
    """
        Initialise l'interface du gestionnaire

        Créer les boutons et affiche les mots de passe de la base de donnée
    
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Gestionnaire de Mot de Passe")
        self.master.configure(bg="#b0c4de")

        # Titre pour la création du nouveau mot de passe
        new_password_label = tk.Label(self.master, text="Bienvenue sur votre Gestionnaire de mots de passe", font=("Helvetica", 16, "bold"), anchor="e", background="#b0c4de")
        new_password_label.pack(pady=10)

        # Création du tableau
        self.tree = ttk.Treeview(self.master, columns=("Titre", "Pseudo", "Mot de Passe", "URL"), show="headings")

        # Configurer les en-têtes de colonnes
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Pseudo", text="Pseudo")
        self.tree.heading("Mot de Passe", text="Mot de Passe")
        self.tree.heading("URL", text="URL")

        # Configurer la largeur des colonnes
        self.tree.column("Titre", width=150)
        self.tree.column("Pseudo", width=150)
        self.tree.column("Mot de Passe", width=150)
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
        copy_button = tk.Button(self.master, text="Copier", command=self.copy_selected)
        copy_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)

        # Bouton pour supprimer
        delete_button = tk.Button(self.master, text="Supprimer", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)

    '''
        Fait la mise à jour de l'affichage des mot de passe 


    '''
    def update_treeview(self):
            # Effacer toutes les lignes du treeview
            for item in self.tree.get_children(): 
                self.tree.delete(item)
            # Récupérer les données de la base de données et les afficher dans le treeview
            cursor.execute('SELECT * FROM mots_de_passe')
            rows = cursor.fetchall()
            for row in rows:
                #mot_de_passe_masque = '*' * len(row[3])
                self.tree.insert("", "end", values=(row[1], row[2], row[3], row[4]))

    '''
        Ouvre password_window en mode nouveau

    '''
    def open_new_password_window(self):
        new_password_window = tk.Toplevel(self.master)
        new_password_window.geometry("600x500")  # taille de la fenêtre
        new_password_app = NewPasswordWindow(new_password_window, self, "new")

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
                cursor.execute('SELECT mot_de_passe FROM mots_de_passe WHERE titre = ? AND utilisateur = ? AND mot_de_passe = ? AND url = ?',
                           (item_values[0], item_values[1], item_values[2], item_values[3]))
                print(item_values[0])
                result = cursor.fetchone()
                print(result)
                if result :
                    password =  result  # Récupérer le mot de passe
                    self.master.clipboard_clear()
                    self.master.clipboard_append(password)
                    self.master.update()
                    print("bien copier")
                    
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner une ligne pour copier.")

    """
        Supprime mot de passe 

        Une fois la ligne selectionnée le mot passe entier est supprimé de la base de donnée
    """

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            mot_de_passe_id = None
            if item_values:
                cursor.execute('SELECT id FROM mots_de_passe WHERE titre = ? AND utilisateur = ? AND mot_de_passe = ? AND url = ?',
                            (item_values[0], item_values[1], item_values[2], item_values[3]))
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

    
    def supprimer_mot_de_passe(self, mot_de_passe_id):
        cursor.execute('DELETE FROM mots_de_passe WHERE id = ?', (mot_de_passe_id,))
        conn.commit()

	
#-------------------------------------------Main-----------------------
	
conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la connexion avec la base de données

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()


#Création de la BDD pour TEST, à déplacer dans le module de création du mdp maître

        #---------------------------------
def create_bd():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS mots_de_passe (
                                id INTEGER PRIMARY KEY,
                                titre TEXT NOT NULL,
                                utilisateur TEXT NOT NULL,
                                mot_de_passe TEXT NOT NULL,
                                url TEXT NOT NULL,
                                note TEXT

                )  ''')
    
    # Vérifier si les données exemple ont été insérées (CAR INSERT OR IGNORE NE MARCHE PAS)
    cursor.execute('''
        SELECT id FROM mots_de_passe
        WHERE titre = "Facebook" AND utilisateur = "Alan30" AND url = "http://facebook.com"
    ''')
    result = cursor.fetchone()

    cursor.execute('''
        SELECT id FROM mots_de_passe
        WHERE titre = "Banque" AND utilisateur = "Ada2372" AND url = "http://hellobank.com"
    ''')
    result2 = cursor.fetchone()
    
    if result is not None and result2 is not None:
        return

    else:

        cursor.execute('''
                    INSERT OR IGNORE INTO mots_de_passe (titre, utilisateur, mot_de_passe, url)
                    VALUES (?, ?, ?, ?) ''', ("Facebook", "Alan30", "SecurePass!456", "http://facebook.com"))
        cursor.execute('''
                    INSERT OR IGNORE INTO mots_de_passe (titre, utilisateur, mot_de_passe, url)
                    VALUES ("Banque","Ada2372", "45637877", "http://hellobank.com") ''')
        conn.commit()  
   
        #------------------------


root = tk.Tk()
root.geometry("1200x800")  # taille de la fenêtre
create_bd()
app = PasswordManager(root)
root.mainloop()
conn.close()