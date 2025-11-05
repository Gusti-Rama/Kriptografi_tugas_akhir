import streamlit as st # <-- PERUBAHAN
import mysql.connector
import pandas as pd
# Hapus 'os' dan 'load_dotenv', sudah tidak diperlukan

# Hapus load_dotenv()

def get_connection():
    """Create a new MySQL connection from Streamlit Secrets."""
    # --- PERUBAHAN DIMULAI DI SINI ---
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        port=st.secrets["DB_PORT"],
        autocommit=False,
    )
    # --- PERUBAHAN SELESAI ---


# Di file koneksi.py

def run_query(query: str, params: tuple | None = None, fetch: bool = False):
    """Execute a SQL query.

    - When fetch=True, returns a pandas DataFrame (can be empty) or None on error.
    - When fetch=False, commits changes and returns True on success, False on error.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch:
            rows = cursor.fetchall()
            return pd.DataFrame(rows)
        else:
            conn.commit()
            return True 
    except mysql.connector.Error as err: 
        print(f"Database Error: {err}") 
        if conn is not None:
            conn.rollback()
        
        if fetch:
            return None
        else:
            return False
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()