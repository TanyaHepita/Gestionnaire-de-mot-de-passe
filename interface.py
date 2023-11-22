import tkinter as tk
from tkinter import ttk, messagebox
from newpassword import NewPasswordWindow
import sqlite3

conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la conncexion avec la base de données

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()
#Création de la BDD pour TEST, à déplacer dans le module de création du mdp maître
        #---------------------------------
def create_bd():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS mots_de_passe (
                                id INTEGER PRIMARY KEY,
                                site TEXT NOT NULL,
                                utilisateur TEXT NOT NULL,
                                mot_de_passe TEXT NOT NULL,
                                note TEXT
                )  ''')

create_bd()
        #------------------------


class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestionnaire de Mot de Passe")
        self.master.configure(bg="#b0c4de")

        # Titre pour la création du nouveau mot de passe
        new_password_label = tk.Label(self.master, text="Bienvenue sur votre Gestionnaire de mots de passe", font=("Helvetica", 16, "bold"), anchor="e", background="#b0c4de")
        new_password_label.pack(pady=10)

        # Création du tableau
        self.tree = ttk.Treeview(self.master, columns=("Titre", "Pseudo", "Mot de Passe"), show="headings")

        # Configurer les en-têtes de colonnes
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Pseudo", text="Pseudo")
        self.tree.heading("Mot de Passe", text="Mot de Passe")

        # Configurer la largeur des colonnes
        self.tree.column("Titre", width=150)
        self.tree.column("Pseudo", width=150)
        self.tree.column("Mot de Passe", width=150)

        # Récupérer les données de la base de données et les afficher dans le treeview
        
        
        self.update_treeview()
        
        # Ajouter le tableau à la fenêtre
        self.tree.pack(side=tk.TOP, anchor=tk.W, pady=50, padx=10)

        # Bouton pour ouvrir la fenêtre de création de mot de passe
        open_new_password_button = tk.Button(self.master, text="Ajouter un nouveau mot de passe", command=self.open_new_password_window)
        open_new_password_button.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        # Bouton pour copier
        copy_button = tk.Button(self.master, text="Copier", command=self.copy_selected)
        copy_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)

        # Bouton pour supprimer
        delete_button = tk.Button(self.master, text="Supprimer", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5, anchor=tk.NW)

    def update_treeview(self):
            # Effacer toutes les lignes du treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Récupérer les données de la base de données et les afficher dans le treeview
            cursor.execute('SELECT * FROM mots_de_passe')
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=(row[1], row[2], row[3]))
                
    def open_new_password_window(self):
        new_password_window = tk.Toplevel(self.master)
        new_password_window.geometry("600x500")  # taille de la fenêtre
        new_password_app = NewPasswordWindow(new_password_window, self)

    # faire un copier du mot de passe
    def copy_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            password = item_values[2]  # Récupérer le mot de passe
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            self.master.update()
            messagebox.showinfo("Copier", f"Le mot de passe a été copié dans le presse-papiers:\n{password}")
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner une ligne pour copier.")
    
    def supprimer_mot_de_passe(self, mot_de_passe_id):
        cursor.execute('DELETE FROM mots_de_passe WHERE id = ?', (mot_de_passe_id,))
        conn.commit()


    # Cette fonction supprime le mot de passe de la ligne sélectionnée
    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            mot_de_passe_id = None
            if item_values:
                cursor.execute('SELECT id FROM mots_de_passe WHERE site = ? AND utilisateur = ? AND mot_de_passe = ?',
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

                messagebox.showinfo("Supprimer", "La ligne a été supprimée avec succès.")
            else:
                messagebox.showwarning("Erreur", "Impossible de trouver l'ID du mot de passe.")
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner une ligne pour supprimer.")

root = tk.Tk()
root.geometry("1200x800")  # taille de la fenêtre
app = PasswordManager(root)
root.mainloop()
conn.close()

