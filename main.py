
from Crypto import Random
from Crypto.Cipher import AES

# Vecteurs d'initialisation
iv_AES = Random.new().read(AES.block_size)

key_AES = 'abcdefghijklmnop'

aese = AES.new(key_AES, AES.MODE_CFB, iv_AES)
aesd = AES.new(key_AES, AES.MODE_CFB, iv_AES)


plaintext = 'Hello! World'

plaintext = aesd.decrypt(aese.encrypt(plaintext))

print(plaintext)