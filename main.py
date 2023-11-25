from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


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


if __name__ == "__main__":
    # Spécifier le chemin du fichier d'entrée (SQL non chiffré)
    input_file_path = "//wsl.localhost/Ubuntu/root/Gestionnaire-de-mot-de-passe-1/test.sql"

    # Spécifier le chemin du fichier de sortie (SQL chiffré)
    output_file_path = "//wsl.localhost/Ubuntu/root/Gestionnaire-de-mot-de-passe-1/res.sql"

    # Générer une clé AES de 32 octets pour AES-256
    key = os.urandom(32) 

    # Chiffrer le fichier
    encrypt_file(input_file_path, output_file_path, key)

    print(f"Fichier chiffré avec succès avec la clé : {key.hex()}")

    # Spécifier le chemin du fichier de sortie déchiffré
    decrypted_output_file_path = "//wsl.localhost/Ubuntu/root/Gestionnaire-de-mot-de-passe-1/res_dechiffre.sql"

    # Déchiffrer le fichier
    decrypt_file(output_file_path, decrypted_output_file_path, key)

    print(f"Fichier déchiffré avec succès.")

