def xor_encrypt(text, key):
    if not key:  
        key = "default" 
        
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted


def xor_decrypt(encrypted_text, key):
    if not key:
        key = "default"
        
    return xor_encrypt(encrypted_text, key) 