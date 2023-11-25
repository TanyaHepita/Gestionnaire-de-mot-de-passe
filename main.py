import hashlib
import os
import tkinter as tk
from interface import PasswordManager
from tkinter import simpledialog, messagebox
import re
import sqlite3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



def encrypt_file(input_file, output_file, key):
    # Générer la clé aléatoire
    iv = get_random_bytes(16)

    # Créer un objet AES avec le mode de chiffrement CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Lire le contenu de la base de donnée
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Ajouter un remplissage pour que la longueur du texte soit un multiple de 16
    padded_plaintext = plaintext + b'\0' * (16 - len(plaintext) % 16)

    # Chiffrer le texte
    ciphertext = cipher.encrypt(padded_plaintext)

    # Écrire le vecteur d'initialisation dans le fichier de sortie
    with open(output_file, 'wb') as f:
        f.write(iv)

    # Écrire le texte chiffré dans le fichier de sortie
    with open(output_file, 'ab') as f:
        f.write(ciphertext)

def decrypt_file(input_file, output_file, key):
    # Lire la clé depuis le fichier d'entrée
    with open(input_file, 'rb') as f:
        iv = f.read(16)

    # Créer un objet AES avec le mode de chiffrement CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Lire le texte chiffré depuis le fichier d'entrée
    with open(input_file, 'rb') as f:
        # Ignorer les 16 premiers octets (IV)
        f.read(16)
        ciphertext = f.read()

    # Déchiffrer le texte
    decrypted_text = cipher.decrypt(ciphertext)

    # Enlever le remplissage ajouté lors du chiffrement
    unpadded_text = decrypted_text.rstrip(b'\0')

    # Écrire le texte déchiffré dans le fichier de sortie
    with open(output_file, 'wb') as f:
        f.write(unpadded_text)



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
    
        open_interface()
    else:
        messagebox.showerror("Authentification échouée", "Mot de passe incorrect. Authentification échouée.")

def open_interface():
    root = tk.Tk()
    root.geometry("800x600")  # taille de la fenêtre
    create_bd()
    app = PasswordManager(root)
    root.mainloop()
    conn.close()



conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la connexion avec la base de données

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()


#Création de la BDD pour TEST, à déplacer dans le module de création du mdp maître

        #---------------------------------
"""
    Créer la base de donnée

    Si elle n'existe pas créer la table et 2 mots de passe exemple
"""
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
    
    if result is not None or result2 is not None:
        return

    else:

        cursor.execute('''
                    INSERT OR IGNORE INTO mots_de_passe (titre, utilisateur, mot_de_passe, url)
                    VALUES (?, ?, ?, ?) ''', ("Facebook", "Alan30", "SecurePass!456", "http://facebook.com"))
        cursor.execute('''
                    INSERT OR IGNORE INTO mots_de_passe (titre, utilisateur, mot_de_passe, url)
                    VALUES ("Banque","Ada2372", "45637877", "http://hellobank.com") ''')
        conn.commit()  


#-------------------------------------------------Master----------------------------

if __name__ == "__main__":

    # Vérifie si le fichier du mot de passe maître existe
    if os.path.exists("master_password.txt"):
        # Si le fichier existe, demande à l'utilisateur de s'authentifier
        authenticate()
    else:
        # Si le fichier n'existe pas, crée un mot de passe maître
        create_master_password()
        # Ensuite, demande à l'utilisateur de s'authentifier
        authenticate()