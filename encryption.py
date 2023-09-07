import cryptography

class Encryption:
    def __init__(self):
        pass
        # add parameters later
        
    # use BCRYPT (a key derivation func) to derive a key
    def generate_derived_key(self, password, salt):
        pass
    # generate random symmetric key
    def generate_random_key(self, key_length):
        pass
    
    # use Fernet (Python symmetric key encryption alg) to encrypt/decrypt key
    # encrypt symmetric key using derived key 
    def encrypt_symm_key(self, symm_key, derived_key):
        pass
    
    # decrypt the encrypted symmetric key using the derived key    
    def decrypt_symm_key(self, encrypted_key, derived_key):
        pass
    
    # use to encrypt user's data using the symmetric key
    def encrypt_data(self, data, symmetric_key):
        pass
    
    # decrypt the user's encrypted data using symmetric key
    def decrypt_data(self, encrypted_data, symmetric_key):
        pass

        
