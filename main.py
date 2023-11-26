import sys
import bcrypt
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QCheckBox, QInputDialog)
from interface import PasswordManager
import tkinter as tk
from tkinter import simpledialog, messagebox
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


# Chemin vers le fichier qui stockera le hash du mot de passe maître
PASSWORD_FILE = 'master_password_hash.txt'

class PasswordMain(QWidget):
    def __init__(self):
        super().__init__()
        self.master_password_hash = None
        self.check_for_existing_master_password()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Entrez votre mot de passe maître' if self.master_password_hash else "Créez votre mot de passe maître, Le mot de passe doit avoir une longeur d' au moin 16 caractéres et contenir au moins : un chiffre,une lettre majuscule,une letrre minuscule et un caractère spécial")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Mot de passe maître')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.show_password_checkbox = QCheckBox('Afficher le mot de passe', self)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        
        self.submit_button = QPushButton('Valider', self)
        self.submit_button.clicked.connect(self.authenticate_or_create)
        
        self.change_password_button = QPushButton('Changer le mot de passe maître', self)
        self.change_password_button.clicked.connect(self.change_master_password)
        self.change_password_button.setEnabled(False)  # Désactivé jusqu'à authentification
        
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.change_password_button)

        self.setLayout(layout)
        self.setWindowTitle('Gestionnaire de mots de passe')

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def check_for_existing_master_password(self):
        # Vérifiez si le fichier contenant le hash du mot de passe maître existe
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, 'rb') as file:
                self.master_password_hash = file.read()

    def authenticate_or_create(self):
        password = self.password_input.text()
        if not self.master_password_hash:
            # Créer un nouveau mot de passe maître
            if self.is_strong_password(password):
                self.create_master_password(password)
                self.label.setText('Le mot de passe maître a été créé.')
                self.change_password_button.setEnabled(True)
            else:
                self.label.setText('Le mot de passe n\'est pas assez robuste.')
        else:
            # Authentifier l'utilisateur
            if bcrypt.checkpw(password.encode('utf-8'), self.master_password_hash):
                self.label.setText('Authentification réussie.')
                self.change_password_button.setEnabled(True)
                self.open_interface()
            else:
                self.label.setText('Échec de l\'authentification.')

    def create_master_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with open(PASSWORD_FILE, 'wb') as file:
            file.write(hashed)
        self.master_password_hash = hashed

    def open_interface(self):
        root = tk.Tk()
        root.geometry("800x600")  # taille de la fenêtre
        create_bd()
        app = PasswordManager(root)
        root.mainloop()
        conn.close()

    def change_master_password(self):
        current_password, ok = QInputDialog.getText(self, 'Vérification',
                                                    'Entrez votre mot de passe actuel:',
                                                    QLineEdit.Password)
        if ok and bcrypt.checkpw(current_password.encode('utf-8'), self.master_password_hash):
            new_password, ok = QInputDialog.getText(self, 'Changer le mot de passe maître',
                                                    'Entrez le nouveau mot de passe maître:',
                                                    QLineEdit.Password)
            if ok and self.is_strong_password(new_password):
                self.create_master_password(new_password)
                self.label.setText('Le mot de passe maître a été changé avec succès.')
            elif not ok:
                self.label.setText('Changement de mot de passe annulé.')
            else:
                self.label.setText('Le nouveau mot de passe n\'est pas assez robuste.')
        else:
            self.label.setText('Le mot de passe actuel est incorrect.')

    def is_strong_password(self, password):
        return len(password) > 15 and any(char.isdigit() for char in password) and \
               any(char.isupper() for char in password) and any(char.islower() for char in password)


conn = sqlite3.connect('gestionnaire_mdp.db') #Ouvre la connexion avec la base de données

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()


#Création de la BDD pour TEST, à déplacer dans le module de création du mdp maître
        #--------------------------------
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordMain()
    ex.show()
    sys.exit(app.exec_())
