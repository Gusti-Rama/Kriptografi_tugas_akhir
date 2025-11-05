import streamlit as st
from PIL import Image
from fungsi import steganography
import io

def stego_page():
    """Menampilkan halaman untuk menyembunyikan dan mengekstrak pesan dari gambar."""
    
    st.title("🖼️ Kalkulator Steganografi LSB")
    st.info("Sembunyikan pesan rahasia di dalam gambar, atau ekstrak pesan dari gambar.")

    with st.expander("⚙️ Pengaturan Lanjutan (Adaptive LSB)"):
        st.markdown("""
        Metode Adaptive LSB menyembunyikan data di area gambar yang "kompleks" (banyak detail) 
        agar lebih sulit dideteksi.
        """)
        
        threshold_percentile = st.slider(
            "Threshold Kompleksitas (Persentil)",
            min_value=1,
            max_value=99,
            value=60,
            key="stego_threshold",
            help="""
            - **Nilai Rendah (cth: 10):** Menggunakan 90% area gambar. Kapasitas besar, tapi kurang aman.
            - **Nilai Tinggi (cth: 90):** Hanya menggunakan 10% area gambar (paling kompleks). Kapasitas kecil, tapi sangat aman.
            - **Default: 60** (menggunakan 40% area terkompleks).
            """
        )
        st.info(f"Pengaturan saat ini: **{100 - threshold_percentile}%** area gambar terkompleks akan digunakan.")

    tab1, tab2 = st.tabs(["Sembunyikan Pesan (Encode)", "Ekstrak Pesan (Decode)"])

    with tab1:
        st.header("Sembunyikan Pesan ke Dalam Gambar")
        
        cover_image_file = st.file_uploader(
            "1. Upload Gambar Sampul (Cover Image):", 
            type=['png', 'jpg', 'jpeg', 'bmp'],
            key="stego_enc_upload"
        )
        
        secret_message = st.text_area(
            "2. Masukkan Pesan Rahasia:",
            key="stego_enc_text",
            height=150
        )
        
        if st.button("Sembunyikan Pesan (Adaptive)", key="stego_enc_btn", use_container_width=True):
            if cover_image_file and secret_message:
                with st.spinner("Mengonversi gambar & menyembunyikan pesan..."):
                    try:
                        image = Image.open(cover_image_file)
                        
                        # Paksa konversi ke PNG (lossless) di memori
                        with io.BytesIO() as output:
                            image.save(output, format="PNG")
                            png_data = output.getvalue()
                        image_lossless = Image.open(io.BytesIO(png_data))

                        # Gunakan gambar lossless untuk embedding
                        stego_image = steganography.embed_msg(image_lossless, secret_message, threshold_percentile)
                        
                        st.success("Pesan berhasil disembunyikan!")
                        st.image(stego_image, caption="Gambar dengan Pesan Tersembunyi (Stego-Image)")
                        
                        buf = io.BytesIO()
                        stego_image.save(buf, format="PNG")
                        byte_im = buf.getvalue()

                        st.download_button(
                            label="Download Gambar (Stego-Image)",
                            data=byte_im,
                            file_name="stego_image.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    except ValueError as e:
                        st.error(f"{e}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
            else:
                st.warning("Harap upload gambar dan masukkan pesan terlebih dahulu.")

    with tab2:
        st.header("Ekstrak Pesan dari Gambar")
        
        stego_image_file = st.file_uploader(
            "1. Upload Gambar Berisi Pesan (Stego-Image):", 
            type=['png'],
            key="stego_dec_upload"
        )
        
        st.warning("Pastikan 'Pengaturan Lanjutan' di atas SAMA PERSIS dengan yang digunakan saat menyembunyikan pesan.")
        
        if st.button("Ekstrak Pesan (Adaptive)", key="stego_dec_btn", use_container_width=True):
            if stego_image_file:
                with st.spinner("Menganalisis gambar dan mencari pesan..."):
                    try:
                        image = Image.open(stego_image_file)
                        
                        extracted_message = steganography.extract_msg(image, threshold_percentile)
                        
                        if extracted_message:
                            st.success("Pesan rahasia berhasil ditemukan!")
                            st.text_area("Pesan:", value=extracted_message, height=150, disabled=True)
                        else:
                            st.warning("Tidak ada pesan rahasia yang ditemukan. (Coba periksa 'Pengaturan Lanjan' Anda atau pastikan gambar asli bukan JPG).")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat mengekstrak: {e}")
            else:
                st.warning("Harap upload gambar terlebih dahulu.")