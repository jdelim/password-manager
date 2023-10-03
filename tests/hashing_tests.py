from encryption import *

def main():
    # create derived key from a master password
    masterpwtest = "yes321"
    salt = bcrypt.gensalt() # store this along with pw
    dkey = generate_derived_key(masterpwtest, salt)
    print(f"Derived key is: {dkey}")
    
    # generate rkey
    rkey = generate_random_key()
    print(f"Random key is: {rkey}")
    
    # encrypt rkey using dkey to get ekey
    ekey = encrypt_symm_key(rkey, dkey)
    print(f"Encrypted key is: {ekey}")
    
    # decrypt ekey using dkey to get rkey
    decrypted_rkey = decrypt_symm_key(ekey, dkey)
    if (decrypted_rkey == rkey):
        print(f"rkeys match! rkey1 is {rkey} and decrypted_rkey is {decrypted_rkey}")
    elif (decrypted_rkey != rkey):
        print(f"rkeys don't match! rkey1 is {rkey} and decrypted_rkey is {decrypted_rkey}")
    
if __name__ == "__main__":
    main()