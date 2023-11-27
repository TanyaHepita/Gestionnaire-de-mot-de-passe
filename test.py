from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def encrypt_file(input_file, key):
    # Générer un vecteur d'initialisation (IV) aléatoire
    iv = get_random_bytes(16)

    # Créer un objet AES avec le mode de chiffrement CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Lire le contenu du fichier d'entrée
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Ajouter un remplissage pour que la longueur du texte soit un multiple de 16
    padded_plaintext = plaintext + b'\0' * (16 - len(plaintext) % 16)

    # Chiffrer le texte
    ciphertext = cipher.encrypt(padded_plaintext)

    # Écrire le vecteur d'initialisation dans le fichier de sortie
    with open(input_file, 'wb') as f:
        f.write(iv)

    # Écrire le texte chiffré dans le fichier de sortie
    with open(input_file, 'ab') as f:
        f.write(ciphertext)

def decrypt_file(input_file, key):
    # Lire le vecteur d'initialisation depuis le fichier d'entrée
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
    with open(input_file, 'wb') as f:
        f.write(unpadded_text)

if __name__ == "__main__":
    # Spécifier le chemin du fichier d'entrée (SQL non chiffré)
    input_file_path = "test.sql"

    # Générer une clé AES de 16, 24 ou 32 octets
    key = "eadd49a0d9fb2db27334991ce3fcfe4e77ab9777e68223478114810ac1b88d30" 
    key_bytes = bytes.fromhex(key) # 32 octets pour AES-256

    # Déchiffrer le fichier
    decrypt_file(input_file_path, key_bytes)

    print(f"Fichier déchiffré avec succès.")


    
