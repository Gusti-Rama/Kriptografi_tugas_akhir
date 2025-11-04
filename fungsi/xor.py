def xor_encrypt(text):
    key = "69"
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted


def xor_decrypt(encrypted_text):
    key = "69" 
    return xor_encrypt(encrypted_text) 
