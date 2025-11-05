import streamlit as st # <-- PERUBAHAN
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
import base64
import hashlib
# Hapus 'os', sudah tidak diperlukan

def get_db_key():
    """
    Mendapatkan kunci 32-byte dari Streamlit Secrets.
    """
    # --- PERUBAHAN DIMULAI DI SINI ---
    key_str = st.secrets.get("DB_ENCRYPTION_KEY")
    if key_str:
        return hashlib.sha256(key_str.encode('utf-8')).digest()
    else:
        print("PERINGATAN: 'DB_ENCRYPTION_KEY' tidak disetel di Streamlit Secrets.")
        # Fallback ini mungkin gagal di server, pastikan secret diatur
        return hashlib.sha256(b"kunci_database_rahasia_default").digest()
    # --- PERUBAHAN SELESAI ---

KEY = get_db_key()

def encrypt_db_data(data_bytes: bytes) -> bytes:
    """
    Mengenkripsi bytes menggunakan ChaCha20-Poly1305.
    Mengembalikan format: base64(nonce + ciphertext + tag)
    """
    try:
        cipher = ChaCha20_Poly1305.new(key=KEY)
        nonce = cipher.nonce 
        
        ciphertext, tag = cipher.encrypt_and_digest(data_bytes)
        
        encrypted_payload = base64.b64encode(nonce + ciphertext + tag)
        return encrypted_payload
    except Exception as e:
        print(f"Error enkripsi DB: {e}")
        raise e

def decrypt_db_data(encrypted_payload: bytes) -> bytes:
    """
    Mendekripsi bytes dari format base64(nonce + ciphertext + tag).
    Mengembalikan data bytes asli.
    """
    try:
        encrypted_data = base64.b64decode(encrypted_payload)
        
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:-16]
        tag = encrypted_data[-16:]
        
        cipher = ChaCha20_Poly1305.new(key=KEY, nonce=nonce)
        
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_bytes
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error dekripsi DB (kunci salah atau data korup): {e}")
        raise ValueError("Gagal mendekripsi data database. Kunci mungkin salah atau data korup.")

def encrypt_db_string(data_string: str) -> bytes:
    """
    Helper function untuk mengenkripsi string ke payload ChaCha20.
    """
    data_bytes = data_string.encode('utf-8')
    return encrypt_db_data(data_bytes)

def decrypt_db_string(encrypted_payload: bytes) -> str:
    """
    Helper function untuk mendekripsi payload ChaCha20 ke string.
    """
    decrypted_bytes = decrypt_db_data(encrypted_payload)
    return decrypted_bytes.decode('utf-8')