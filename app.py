import streamlit as st
import google.generativeai as genai

# ==========================================
# KONFIGURASI MASTER
# ==========================================
# Masukkan API Key AIza... Anda di sini
API_KEY = "AIzaSyCVj54iK7YyLPtczMv-k85QvzyBWfjDcH8" 
genai.configure(api_key=API_KEY)

# Pengaturan Tampilan Website
st.set_page_config(page_title="Master Generator Modul PAUD", layout="wide")

st.title("🚀 Master Generator Modul Ajar PAUD")
st.info("Versi Master: Nama Guru & Sekolah dapat diubah secara dinamis.")

# BAGIAN INPUT IDENTITAS (Di Versi Master ini masih bisa diisi manual)
with st.sidebar:
    st.header("🔑 Lisensi & Pengesahan")
    nama_user = st.text_input("Nama Guru/Penyusun", "Admin Master")
    nama_sekolah = st.text_input("Nama Satuan PAUD", "TK Islam Baitul Inayah")
    nama_ks = st.text_input("Nama Kepala Sekolah", "....................")
    st.divider()
    st.caption("Catatan: Di versi jual, bagian ini akan dikunci/dihilangkan.")

# BAGIAN INPUT KONTEN MODUL
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        topik = st.text_input("Topik Utama", placeholder="Contoh: Alam Semesta")
        subtopik = st.text_input("Subtopik", placeholder="Contoh: Bintang di Langit")
        model_belajar = st.selectbox("Model Belajar", ["Play Based Learning", "Project Based Learning", "Inquiry Based Learning"])
    
    with col2:
        hari = st.slider("Jumlah Pertemuan (Hari)", 1, 6, 1)
        waktu = st.text_input("Alokasi Waktu", "08.00 - 10.30 WIB")

# TOMBOL GENERATE
if st.button("BUAT MODUL SEKARANG"):
    if not topik or not subtopik:
        st.warning("Mohon isi Topik dan Subtopik!")
    else:
        with st.spinner("Sedang memproses modul sesuai standar Pakar PAUD..."):
            try:
                model_ai = genai.GenerativeModel('gemini-1.5-flash')
                
                # PROMPT RAHASIA ANDA (Sudah Terintegrasi)
                prompt_full = f"""
                SYSTEM PROMPT: GENERATOR MODUL AJAR PAUD
                PERAN: Anda adalah seorang Pakar Pengembang Kurikulum PAUD (Fase Fondasi) di Indonesia dengan spesialisasi pada Pembelajaran Mendalam (Deep Learning), Berkesadaran (Mindfulness), dan Bermakna.

                INSTRUKSI UTAMA:
                Buatlah konten rencana pembelajaran yang komprehensif berdasarkan data input:
                Topik Utama: {topik}
                Subtopik: {subtopik}
                Model Belajar: {model_belajar}
                Jumlah Pertemuan: {hari} Hari
                Alokasi Waktu: {waktu}

                KETENTUAN FORMAT OUTPUT (WAJIB DIPATUHI):
                GAYA BAHASA: Formal, edukatif, namun hangat (khas PAUD).
                FORMAT NARASI (PARAGRAF): Wajib pada Identifikasi Peserta Didik, Materi Pelajaran, Capaian Pembelajaran, Lintas Disiplin Ilmu, Topik Pembelajaran, Praktik Pedagogis.
                FORMAT PENOMORAN: Wajib pada Dimensi Profil Lulusan, Tujuan Pembelajaran, Langkah Inti.

                STRUKTUR KONTEN:
                1. SEKSI IDENTIFIKASI & MEDIA (BAGIAN A)
                2. SEKSI DESAIN PEMBELAJARAN (BAGIAN B)
                3. SEKSI PENGALAMAN BELAJAR (BAGIAN C)
                4. LAMPIRAN ASESMEN (10 IKTP)

                PENGESAHAN:
                Tuliskan di bagian akhir:
                Mengetahui,
                Kepala Sekolah: {nama_ks}
                Guru Kelas: {nama_user}
                Satuan PAUD: {nama_sekolah}

                CATATAN: Jangan sebut kata 'AI' atau 'Generator' di hasil akhir.
                """

                response = model_ai.generate_content(prompt_full)
                st.success("Modul Berhasil Dibuat!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
