import getpass
from cryptography.fernet import Fernet
import bcrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
# use pbkdf2 to generate a key from password 
def generate_derived_key(password, salt):
    # create pbkdf2hmac key deriv function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # iterations can be adjusted
        salt=salt,
        length=32
    )
    
    # derive key from password
    dkey = kdf.derive(password.encode())
    
    return dkey

# generate random symmetric key
def generate_random_key(): # default key value is 32 bytes (256 bits), Fernet uses AES-CTR
    rkey = Fernet.generate_key()
    return rkey

# use Fernet (Python symmetric key encryption alg) to encrypt/decrypt key
# encrypt symmetric key using derived key 
def encrypt_symm_key(rkey, dkey):
    try:
        # Use dkey to create a Fernet cipher
        cipher = Fernet(dkey)
        # Encrypt rkey using cipher
        ekey = cipher.encrypt(rkey)
        return ekey
    except Exception as e:
        print("Encryption error: ", e)
        return None

# decrypt the encrypted symmetric key using the derived key    
def decrypt_symm_key(ekey, dkey):
    try:
         # create fernet cipher using dkey
         cipher = Fernet(dkey)
         
         # decrypt ekey
         rkey = cipher.decrypt(ekey)
         
         return rkey
    except Exception as e:
        # invalid key/data
        print("DECRYPTION ERROR OH NO!", e)
        return None

# use to encrypt user's data using the symmetric key
def encrypt_data(data, symmetric_key):
    pass

# decrypt the user's encrypted data using symmetric key
def decrypt_data(encrypted_data, symmetric_key):
    pass

        
