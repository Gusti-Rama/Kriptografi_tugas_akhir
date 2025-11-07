# Vanish Chat

Vanish adalah website chat aman yang dirancang dengan fokus utama pada privasi dan keamanan data. Website ini menerapkan berbagai algoritma kriptografi modern dan klasik untuk melindungi pesan teks, file, dan gambar, memastikan bahwa hanya pengirim dan penerima yang dituju yang dapat mengakses informasi.

Proyek ini dibuat untuk memenuhi Tugas Akhir Mata Kuliah Kriptografi kelas IF-B.

-   **Reza Rasendriya Adi Putra (123230030)**
-   **Gusti Rama (123230040)**

## 🛡️ Fitur Keamanan

Vanish mengimplementasikan tiga fungsionalitas kriptografi utama untuk mengamankan berbagai jenis data:

1.  **Super-Enkripsi (Pesan Teks)**
    -   Pesan teks diamankan menggunakan tiga lapisan enkripsi (Caesar Cipher, XOR Cipher, dan RSA) sebelum dikirim.
    -   Hanya *ciphertext* akhir yang disimpan di database, sehingga administrator server pun tidak dapat membaca isinya.
    -   Kunci (Caesar Shift & Kunci XOR) harus disepakati secara manual antara pengirim dan penerima.

2.  **Enkripsi File (Semua Jenis File)**
    -   Mengamankan pengiriman file (dokumen, video, audio, .zip, dll.) menggunakan algoritma *block cipher* simetris **Blowfish**.
    -   Kunci enkripsi (berbasis *password*) harus dibagikan secara aman kepada penerima untuk dekripsi.

3.  **Steganografi (Teks/Gambar dalam Gambar)**
    -   Menyembunyikan pesan teks rahasia atau gambar rahasia lain di dalam sebuah gambar sampul (cover image).
    -   Menggunakan metode **Adaptive LSB (Least Significant Bit)**, yang secara cerdas menyisipkan data di area gambar yang paling kompleks untuk menghindari deteksi visual.
    -   Nilai *Threshold* bertindak sebagai kunci yang harus disepakati oleh kedua belah pihak.

4.  **Keamanan Database & Login**
    -   **Login:** Menggunakan *hashing* **PBKDF2-HMAC-SHA256** dengan *salt* unik untuk setiap pengguna, mencegah serangan *rainbow table*.
    -   **Database:** Seluruh data sensitif di dalam database (username, pesan, nama file, dan data file itu sendiri) dienkripsi menggunakan **ChaCha20-Poly1305**, sebuah *stream cipher* modern yang terautentikasi (AEAD).

## 💻 Technology Stack

-   **Frontend:** Streamlit
-   **Backend:** Python
-   **Database:** MySQL
-   **Bahasa:** Python
-   **Library Utama:**
    -   `pycryptodome` (RSA, Blowfish, ChaCha20-Poly1305, PBKDF2)
    -   `mysql-connector-python` (Koneksi Database)
    -   `pandas` (Manipulasi Data)
    -   `Pillow (PIL)` & `numpy` (Pemrosesan Gambar & Steganografi)
    -   `python-dotenv` (Manajemen Konfigurasi)

## 🤓 Panduan Instalasi & Konfigurasi

Ikuti langkah-langkah ini untuk menjalankan proyek Vanish di environment lokal Anda.

### 1. Prerequisite

-   Python 3.13+
-   Server Database MySQL (atau MariaDB)

### 2. Clone Repository

```bash
git clone https://github.com/Gusti-Rama/Kriptografi_tugas_akhir
cd Kriptografi_tugas_akhir
```

### 3. Siapkan Database

1.  Buka *client* MySQL Anda (phpMyAdmin).
2.  Buat database baru dengan nama `vanish` (atau nama lain pilihan Anda). Gunakan collation **utf8mb4_general_ci**.
    ```sql
    CREATE DATABASE vanish
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;
    ```
3.  Impor file SQL yang ada di folder database`database/vanish.sql`.

### 4. Konfigurasi Environment

1.  Install semua dependensi yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```
2.  Copy paste file `.env.example` dan rename menjadi `.env`:

3.  Buka dan edit file `.env` dengan konfigurasi database Anda dan kunci enkripsi unik.
    ```ini
    # Konfigurasi Database
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=password_database_anda
    DB_NAME=vanish
    DB_PORT=port_database_anda #biasanya 3306

    # Kunci untuk enkripsi database Chacha20
    DB_ENCRYPTION_KEY=buat-kunci-rahasia-yang-sangat-kuat-disini
    ```
    **PENTING:** `DB_ENCRYPTION_KEY` adalah kunci master untuk mengenkripsi/mendekripsi data di database. **Jangan pernah ubah kunci ini** setelah website digunakan, atau semua data yang ada di database tidak akan bisa dibaca kembali.

### 5. Jalankan Streamlit

Setelah semua konfigurasi selesai, jalankan Streamlit:

```bash
streamlit run app.py
```

Website akan terbuka di *browser* Anda.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).