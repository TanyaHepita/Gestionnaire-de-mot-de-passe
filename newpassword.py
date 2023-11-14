import tkinter as tk
from tkinter import messagebox


class NewPasswordWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Nouveau Mot de Passe")

        # Entrée pour le nom du mot de passe
        password_name_label = tk.Label(self.master, text="Nom du mot de passe:", anchor="e")
        password_name_label.pack()
        self.password_name_entry = tk.Entry(self.master)
        self.password_name_entry.pack(pady=5)

        # Entrée pour le nouveau mot de passe
        password_label = tk.Label(self.master, text="Nouveau mot de passe:", anchor="e")
        password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=10)

        # Option pour afficher/masquer le mot de passe
        self.show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(self.master, text="Afficher le mot de passe", variable=self.show_password_var,
                                                command=self.toggle_password_visibility, anchor="e")
        show_password_checkbox.pack(pady=5)

        # Bouton pour générer un mot de passe fort
        generate_password_button = tk.Button(self.master, text="Générer un mot de passe fort", command=self.generate_strong_password)
        generate_password_button.pack(pady=10)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def generate_strong_password(self):
        # Ajoute ici la logique pour générer un mot de passe fort
        messagebox.showinfo("Mot de Passe Fort", "Mot de passe fort généré!")