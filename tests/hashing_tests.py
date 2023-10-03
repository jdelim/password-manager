from encryption import *

def main():
    # create derived key from a master password
    masterpwtest = "yes321"
    salt = bcrypt.gensalt() # store this along with pw
    dkey = generate_derived_key(masterpwtest, salt)
    #print(f"Derived key is: {dkey}")
    
    # generate rkey
    rkey = generate_random_key()
    #print(f"Random key is: {rkey}")
    
    # encrypt rkey using dkey to get ekey
    ekey = encrypt_symm_key(rkey, dkey)
    #print(f"Encrypted key is: {ekey}")
    
    # decrypt ekey using dkey to get rkey
    decrypted_rkey = decrypt_symm_key(ekey, dkey)
    # if (decrypted_rkey == rkey):
    #     print(f"rkeys match! rkey1 is {rkey} and decrypted_rkey is {decrypted_rkey}")
    # elif (decrypted_rkey != rkey):
    #     print(f"rkeys don't match! rkey1 is {rkey} and decrypted_rkey is {decrypted_rkey}")
    
    # encrypt data (string)
    myPassword = "abcdefg"
    myPassword2 = "abcde1fg"
    
    encrypted_data = encrypt_data(myPassword, rkey)
    encrypted_data2 = encrypt_data(myPassword2, rkey)
    print(f"Encrypted data is: {encrypted_data}")
    print(f"Second encrypted data is: {encrypted_data2}")
    
    # decrypt data 
    decrypted_data = decrypt_data(encrypted_data, rkey)
    decrypted_data_2 = decrypt_data(encrypted_data2, rkey)
    print(f"Decrypted data is: {decrypted_data}")
    print(f"Second decrypted data is: {decrypted_data_2}")
    
if __name__ == "__main__":
    main()