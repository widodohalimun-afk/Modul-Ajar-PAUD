import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# ==========================================
# KONFIGURASI API KEY
# ==========================================
API_KEY = "AIzaSyCVj54iK7YyLPtczMv-k85QvzyBWfjDcH8" 
genai.configure(api_key=API_KEY)

# ==========================================
# IDENTITAS SEKOLAH (KONFIGURASI TETAP)
# ==========================================
NAMA_SEKOLAH = "TK ISLAM BAITUL INAYAH"
ALAMAT_SEKOLAH = "Jl. Raya Baitul Inayah No. 01"
KONTAK_SEKOLAH = "HP. 0812-xxxx-xxxx, Email: sekolah@inayah.com"

# ==========================================
# FUNGSI PDF (FONT TIMES NEW ROMAN)
# ==========================================
class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_font('Times', 'B', 14)
            self.cell(0, 10, NAMA_SEKOLAH, ln=True, align='C')
            self.set_font('Times', '', 10)
            self.cell(0, 5, ALAMAT_SEKOLAH, ln=True, align='C')
            self.cell(0, 5, KONTAK_SEKOLAH, ln=True, align='C')
            self.line(10, 32, 200, 32)
            self.ln(10)

def generate_pdf(text, filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=11)
    # Clean text for FPDF latin-1
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, clean_text)
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# ANTARMUKA PENGGUNA (UI)
# ==========================================
st.set_page_config(page_title="Generator Ibischool", layout="wide")
st.title("📄 Ibischool Curriculum Generator (Edisi Komprehensif)")

with st.sidebar:
    st.header("⚙️ Pengaturan Dokumen")
    judul = st.selectbox("Jenis Dokumen", ["Modul Ajar Kurikulum Merdeka", "Perancangan Pembelajaran Mendalam", "RPP Harian"])
    ta = st.text_input("Tahun Ajaran", "2025/2026")
    guru = st.text_input("Nama Guru", "Widodo Halimun")
    ks = st.text_input("Kepala Sekolah", "Siti Aminah, S.Pd")
    st.divider()
    st.info("Sistem akan menyesuaikan output berdasarkan referensi dokumen standar PAUD Jateng/Ibischool.")

col1, col2 = st.columns(2)
with col1:
    topik = st.text_input("Topik Utama")
    subtopik = st.text_input("Subtopik")
    usia = st.selectbox("Jenjang/Usia", ["KB (2-3 Thn)", "KB (3-4 Thn)", "A (4-5 Thn)", "B (5-6 Thn)"])
with col2:
    hari = st.slider("Jumlah Hari", 1, 6, 5)
    model_belajar = st.selectbox("Model Belajar", ["Inkuiri", "Loose Parts", "Project Based Learning", "Sentra"])
    alokasi = st.text_input("Alokasi Waktu", "5 x 3 JP")

if st.button("🚀 GENERATE DOKUMEN SEKARANG"):
    if not topik or not subtopik:
        st.error("Isi Topik dan Subtopik terlebih dahulu!")
    else:
        with st.spinner("Sedang menyinkronkan data dengan standar Ibischool..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # MASTER PROMPT SESUAI REFERENSI DOKUMEN
                prompt = f"""
                Bertindaklah sebagai Pakar Pengembang Kurikulum PAUD Ibischool. 
                Buatlah {judul} lengkap berdasarkan referensi struktur dokumen terbaru (Permendikdasmen No 13 Tahun 2025).

                DATA INPUT:
                Sekolah: {NAMA_SEKOLAH}
                Topik: {topik} | Subtopik: {subtopik}
                Usia: {usia} | Hari: {hari} hari | Alokasi: {alokasi}
                Model: {model_belajar} | Tahun Ajaran: {ta}

                STRUKTUR OUTPUT (WAJIB ADA):
                1. KOP & IDENTITAS: Buat persis seperti dokumen referensi (Penulis, Semester, Fase, Minggu ke, dsb).
                2. IDENTIFIKASI (Narasi): Buat narasi paragraf untuk Peserta Didik, Materi Pelajaran, dan Dimensi Profil Lulusan (sinkronkan dengan CP).
                3. CAPAIAN PEMBELAJARAN (CP): Ambil elemen Nilai Agama & Budi Pekerti, Jati Diri, dan Dasar Literasi/STEAM yang relevan.
                4. TUJUAN PEMBELAJARAN: List dengan penomoran.
                5. MEDIA & APE: Daftar Alat dan Bahan (Loose Parts) dan penjelasan cara kerja APE.
                6. KEGIATAN INTI: Buat rencana harian untuk {hari} hari. Sertakan Nama Kegiatan (Bold), Alat/Bahan, dan Langkah Pembelajaran mendetail per paragraf.
                7. ASESMEN (Format Tabel/List): Sertakan format untuk Catatan Anekdot, Ceklis IKTP, dan Dokumentasi Hasil Karya.
                8. PENGESAHAN: Tanda tangan Kepala Sekolah ({ks}) dan Guru ({guru}).

                Gaya Bahasa: Formal, hangat, Times New Roman style, tanpa kata 'AI'.
                """

                response = model.generate_content(prompt)
                hasil = response.text
                
                st.success("Berhasil! Silakan tinjau dan download.")
                st.markdown(hasil)
                
                # Tombol Download
                pdf_data = generate_pdf(hasil, subtopik)
                st.download_button(
                    label="📥 Download PDF (Standar Ibischool)",
                    data=pdf_data,
                    file_name=f"Modul_{subtopik}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
