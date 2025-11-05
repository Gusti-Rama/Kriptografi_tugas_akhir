import streamlit as st
import koneksi as conn

# --- PERUBAHAN DIMULAI DI SINI ---
def home():
    st.title("💬 Selamat Datang di Vanish")
    st.markdown("Pilih obrolan di sidebar kiri atau tambahkan obrolan baru untuk memulai.")
    
    st.divider()
    with st.container(border=True):
        st.subheader("🔒 Bagaimana Obrolan Aman Ini Bekerja?")
        st.markdown(
            """
            Vanish dirancang untuk privasi absolut. Semua pesan Anda diamankan menggunakan **Enkripsi Berlapis** sebelum pernah meninggalkan komputer Anda.
            """
        )
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### 1. Ditulis (Plaintext)")
            st.markdown("Anda menulis pesan seperti biasa di halaman 'Demo Enkripsi'.")
        with c2:
            st.markdown("#### 2. Dienkripsi (Super-Enkripsi)")
            st.markdown("Pesan dienkripsi dengan **Caesar**, lalu **XOR**, lalu **RSA**.")
        with c3:
            st.markdown("#### 3. Dikirim (Ciphertext)")
            st.markdown("Hanya teks acak (ciphertext) yang disimpan di database dan dikirim ke penerima.")
        
        st.markdown("---") 
        st.markdown("#### 📖 Cara Mengirim dan Membaca Pesan")
        st.markdown(
            """
            Karena keamanan ini, Anda **tidak bisa** langsung mengetik di kotak obrolan. Anda harus menggunakan halaman **'🧪 Demo Super-Enkripsi'**
            * **Untuk Mengirim Pesan:**
                1.  Buka '🧪 Demo Super-Enkripsi'.
                2.  Tulis pesan Anda di tab **'Proses Enkripsi'**.
                3.  Klik 'Enkripsi'.
                4.  Salin (Copy) **'Hasil Akhir'** (ciphertext).
                5.  Tempel (Paste) di kotak pesan obrolan dan kirim
            * **Untuk Membaca Pesan:**
                1.  Salin (Copy) pesan ciphertext yang Anda terima dari gelembung obrolan.
                2.  Buka '🧪 Demo Super-Enkripsi'.
                3.  Tempel (Paste) ke tab **'Proses Dekripsi'**.
                4.  Klik 'Dekripsi' untuk melihat pesan asli.
            """
        )
        st.warning(
            "**PENTING:** Anda dan penerima harus menyetujui dan menggunakan **Kunci (Shift & XOR)** yang sama persis agar pesan bisa dibaca!",
            icon="🔑"
        )
    st.divider()
    
    # Row 2: Call to Action
    st.header("Apa yang ingin Anda lakukan?")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("Buka Obrolan")
            st.info("Pilih nama pengguna dari daftar 'Your Chats' di sidebar kiri.")
    with c2:
        with st.container(border=True):
            st.subheader("Mulai Obrolan Baru")
            st.info("Gunakan kotak teks 'Add New Chat' di sidebar kiri untuk mencari pengguna baru.")
    # --- PERUBAHAN SELESAI DI SINI --