import tkinter as tk
from tkinter import ttk, messagebox
from newpassword import NewPasswordWindow

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

        # Ajouter des lignes d'exemple
        example_data = [
            ("Compte Microsoft", "user123", "*****", "https://www.example1.com"),
            ("Compte Protime", "admin_pro", "******","https://www.example1.com"),
            ("Compte Gmail", "john.doe@gmail.com", "montant", "https://www.example1.com"),
            ("Compte Facebook", "fb_user", "*********", "https://www.example1.com"),
            ("Compte Twitter", "twitter_user", "*********", "https://www.example1.com")
        ]

        for data in example_data:
            self.tree.insert("", "end", values=data)

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

    def open_new_password_window(self):
        new_password_window = tk.Toplevel(self.master)
        new_password_window.geometry("600x500")  # taille de la fenêtre
        new_password_app = NewPasswordWindow(new_password_window, self, "new")

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
            password = item_values[2]  # Récupérer le mot de passe
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
        selected_item = self.tree.selection()
        if selected_item:
            # Ici, tu peux ajouter la suppression dans la BDD
            self.tree.delete(selected_item)
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner une ligne pour supprimer.")

root = tk.Tk()
root.geometry("1200x800")  # taille de la fenêtre
app = PasswordManager(root)
root.mainloop()