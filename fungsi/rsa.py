def rsa_encrypt(message):
    e = 17
    n = 3233 
    
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted


def rsa_decrypt(encrypted):
    d = 2753
    n = 3233 

    if isinstance(encrypted, str):
        encrypted_list = encrypted.split()
    else:
        encrypted_list = encrypted

    decrypted = ''.join(chr(pow(int(char), d, n)) for char in encrypted_list)
    return decrypted
