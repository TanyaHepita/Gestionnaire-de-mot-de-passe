import hashlib
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import re

def is_strong_password(password):
    # Vérifie si le mot de passe est robuste
    return bool(re.match(r'^(?=.*[A-Z].*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{16,}$', password))

def create_master_password():
    while True:
        # Demande à l'utilisateur de créer un mot de passe maître robuste
        master_password = simpledialog.askstring("Création du mot de passe maître", "Créez votre mot de passe maître robuste (au moins 16 caractères, 2 majuscules, des chiffres, des caractères spéciaux) : ")
        
        if is_strong_password(master_password):
            break
        else:
            messagebox.showwarning("Mot de passe faible", "Le mot de passe n'est pas assez robuste. Veuillez réessayer.")

    # Utilise un hash pour stocker le mot de passe de manière sécurisée
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    
    # Enregistre le hash dans un fichier sur la clé USB
    with open("master_password.txt", "w") as file:
        file.write(hashed_password)
        
    messagebox.showinfo("Succès", "Mot de passe maître créé avec succès.")

def authenticate():
    # Demande à l'utilisateur de saisir le mot de passe maître
    input_password = simpledialog.askstring("Authentification", "Entrez votre mot de passe maître : ")
    
    # Charge le hash du mot de passe depuis le fichier
    with open("master_password.txt", "r") as file:
        stored_password = file.read()
        
    # Vérifie si le hash du mot de passe entré correspond au hash enregistré
    if hashlib.sha256(input_password.encode()).hexdigest() == stored_password:
        messagebox.showinfo("Authentification réussie", "Bienvenue ! Authentification réussie.")
        # Tu peux ajouter le reste de ton programme ici
    else:
        messagebox.showerror("Authentification échouée", "Mot de passe incorrect. Authentification échouée.")

# Vérifie si le fichier du mot de passe maître existe
if os.path.exists("master_password.txt"):
    # Si le fichier existe, demande à l'utilisateur de s'authentifier
    authenticate()
else:
    # Si le fichier n'existe pas, crée un mot de passe maître
    create_master_password()
    # Ensuite, demande à l'utilisateur de s'authentifier
    authenticate()
