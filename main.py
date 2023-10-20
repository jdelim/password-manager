from encryption import *
from database import *

def main():
    
    master_password = getpass.getpass(prompt="Enter your master password: ")
    #master_password = input("Please enter your master password: ")
    print(f"Your master password is: {master_password} ")

    # generate random key for user after "Login"
    rkey = generate_random_key()
    salt = bcrypt.gensalt()    
    #print(f"Salt is: {salt}")
    #print(f"\nThe symmetric key (rkey) that will encrypt your data is: {rkey}")
    
    # Get dkey and ekey
    dkey = generate_derived_key(master_password, salt)
    #print(f"\nYour derived key from your master password is: {dkey}")
    
    ekey = encrypt_symm_key(rkey, dkey)
    #print(f"\nYour encrypted symmetric key (ekey) using dkey is: {ekey}")
    
    
    # Ask user for passwords
    print("\nPlease enter your passwords individually, type \"done\" when finished.")
    myPasswords = []
    prompt = ""
    while prompt != "done":
        prompt = input("\nPlease enter a password: ")
        if (prompt != "done"):
            myPasswords.append(prompt)
        # Display passwords as user enters them
        print(f"Your current passwords are: {myPasswords}")
    
    # Encrypt passwords when user types "encrypt"
    print("\nThank you, please type \"encrypt\" to encrypt your passwords!")
    encPrompt = input()
    while encPrompt != "encrypt":
        print("Please type \"encrypt\"!")
        encPrompt = input()
    
    encrypted_passwords = []
    for password in myPasswords:
        encrypted_data = encrypt_data(password, rkey)
        encrypted_passwords.append(encrypted_data)
    print(f"\nYour encrypted passwords are: {encrypted_passwords}")
    
    # Decrypt passwords
    decrypted_passwords = []
    print("\nPlease type your master password to decrypt your passwords!")
    decPrompt = ""

    while decPrompt != rkey:
        print("Please type your master password!")
        decPrompt = input()
        # derive a key from user input
        derived_user_key = generate_derived_key(decPrompt, salt)
        decPrompt = decrypt_symm_key(ekey, derived_user_key)
    for data in encrypted_passwords:
        decrypted_data = decrypt_data(data, decPrompt)
        decrypted_passwords.append(decrypted_data)
    
    print(f"\nYour decrypted passwords are: {decrypted_passwords}")
    
    # Decrypt passwords when user types in master password
if __name__ == "__main__":
    main()