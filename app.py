import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# ==========================================
# 01. KONFIGURASI SISTEM & API
# ==========================================
API_KEY = "PASTE_KODE_AIza_ANDA_DI_SINI" 
genai.configure(api_key=API_KEY)

# ==========================================
# 02. IDENTITAS SEKOLAH (DIKUNCI)
# ==========================================
# Sesuai dengan permintaan untuk identitas yang dikunci
NAMA_SATUAN = "TK ISLAM BAITUL INAYAH"
ALAMAT_SATUAN = "Jl. Raya Baitul Inayah No. 01"
KOTA_SISTEM = "Jakarta"

# ==========================================
# 03. FUNGSI CETAK PDF (GAYA TIMES NEW ROMAN)
# ==========================================
class IbischoolPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_font('Times', 'B', 14)
            self.cell(0, 10, NAMA_SATUAN.upper(), ln=True, align='C')
            self.set_font('Times', '', 10)
            self.cell(0, 5, ALAMAT_SATUAN, ln=True, align='C')
            self.line(10, 32, 200, 32)
            self.ln(10)

def cetak_dokumen(konten, guru, ks, tgl_cetak):
    pdf = IbischoolPDF()
    pdf.add_page()
    pdf.set_font("Times", size=11)
    # Menghindari error karakter asing
    text = konten.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, txt=text)
    
    # Tanda Tangan (Sig Container dari gaya HTML)
    pdf.ln(20)
    pdf.cell(0, 10, f"{tgl_cetak}", ln=True, align='R')
    pdf.ln(5)
    
    y_pos = pdf.get_y()
    pdf.set_font("Times", 'B', 11)
    # Kolom Kiri: Kepala Sekolah
    pdf.set_xy(10, y_pos)
    pdf.cell(95, 5, "Mengesahkan,", 0, 1, 'C')
    pdf.cell(95, 5, "Kepala Sekolah", 0, 1, 'C')
    pdf.ln(15)
    pdf.cell(95, 5, f"{ks.upper()}", 0, 1, 'C')
    
    # Kolom Kanan: Guru
    pdf.set_xy(105, y_pos)
    pdf.cell(95, 5, "", 0, 1, 'C')
    pdf.cell(95, 5, "Guru Kelas", 0, 1, 'C')
    pdf.ln(15)
    pdf.set_xy(105, pdf.get_y())
    pdf.cell(95, 5, f"{guru.upper()}", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 04. ANTARMUKA INPUT (GAYA HTML MASTER)
# ==========================================
st.set_page_config(page_title="RKH Digital Ibischool Master", layout="wide")

# Header Style
st.markdown("<h1 style='text-align: center; color: #1e40af;'>RKH DIGITAL IBISCHOOL MASTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px;'>Sistem Perancangan Pembelajaran PAUD Terpadu - Edisi Indonesia Premium</p>", unsafe_allow_html=True)

# Sidebar (Identitas Dokumen & Lembaga)
with st.sidebar:
    st.header("01. Identitas Dokumen")
    judul_pilihan = st.selectbox("Judul Dokumen", [
        "Modul Pembelajaran Mendalam", 
        "Rencana Pelaksanaan Pembelajaran Mendalam",
        "Perancangan Pembelajaran Mendalam"
    ])
    ta = st.text_input("Tahun Ajaran", "2025/2026")
    tgl_full = st.text_input("Kota & Waktu", f"{KOTA_SISTEM}, {datetime.date.today().strftime('%d %B %Y')}")
    
    st.header("02. Identitas Pengesahan")
    nama_ks = st.text_input("Nama Kepala Sekolah", "SITI AMINAH, S.Pd")
    nama_guru = st.text_input("Nama Guru / Penulis", "WIDODO HALIMUN")
    
    st.divider()
    st.info(f"Database Terkunci: {NAMA_SATUAN}")

# Kolom Utama (Identitas Modul)
st.subheader("03. Identitas Modul & Pertemuan")
col1, col2, col3 = st.columns(3)

with col1:
    tema_besar = st.selectbox("Topik Utama (Tema P5/Intra)", [
        "Diriku / Aku Istimewa", "Aku Sayang Bumi", "Aku Cinta Indonesia", 
        "Lingkunganku", "Binatang", "Tanaman", "Kendaraan", "Alam Semesta"
    ])
    bingkai = st.selectbox("Bingkai Visual", ["Formal", "Alam (Pohon)", "Kendaraan", "Makanan", "Sekolah"])

with col2:
    subtopik = st.text_input("Subtopik (Cth: Identitas Diriku)")
    usia = st.selectbox("Kelompok Usia", ["KB (2-3 Thn)", "KB (3-4 Thn)", "A (4-5 Thn)", "B (5-6 Thn)"])

with col3:
    hari = st.slider("Jumlah Pertemuan (Hari)", 1, 6, 5)
    model_belajar = st.selectbox("Model Belajar", ["Inkuiri", "Sentra", "Loose Parts", "PjBL", "Montessori"])

# ==========================================
# 05. LOGIKA GENERASI (MASTER PROMPT)
# ==========================================
if st.button("🚀 KEMBANGKAN PERENCANAAN LENGKAP"):
    if not subtopik or API_KEY == "PASTE_KODE_AIza_ANDA_DI_SINI":
        st.error("Lengkapi Subtopik dan pastikan API KEY sudah benar!")
    else:
        with st.spinner("Sistem Ibischool Sedang Menyelaraskan Perencanaan Master..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Menggabungkan Master Prompt Anda dengan Referensi Dokumen
                prompt_final = f"""
                Gunakan peran sebagai Pakar Kurikulum PAUD Ibischool. 
                Buatlah dokumen {judul_pilihan} yang sinkron dengan struktur Deep Learning.

                IDENTITAS:
                Sekolah: {NAMA_SATUAN} | Tahun Ajaran: {ta} | Model: {model_belajar}
                Topik: {tema_besar} | Subtopik: {subtopik} | Untuk {hari} hari.

                STRUKTUR WAJIB (GAYA DOKUMEN REFERENSI):
                1. IDENTIFIKASI: Narasi mendalam (paragraf) tentang Peserta Didik, Materi Pelajaran, dan Dimensi Profil Pelajaran Pancasila (DPL).
                2. DESAIN PEMBELAJARAN: Cantumkan CP sesuai Permendikdasmen No 13 Tahun 2025, Lintas Disiplin Ilmu, dan Tujuan Pembelajaran.
                3. PENGALAMAN BELAJAR: Rincian {hari} hari dengan tahap AWAL, INTI, dan PENUTUP. 
                   Setiap hari wajib ada: Nama Kegiatan (Bold), Alat & Bahan, dan Langkah Pembelajaran mendetail.
                4. ASESMEN: Sertakan format Tabel Catatan Anekdot dan Ceklis IKTP (10 poin).

                ATURAN: Bahasa Indonesia formal, Times New Roman style, tanpa kata 'AI'.
                """
                
                response = model.generate_content(prompt_final)
                hasil_teks = response.text
                
                st.success("Perencanaan Master Berhasil Disusun!")
                st.markdown(hasil_teks)
                
                # Download Section
                pdf_bytes = cetak_dokumen(hasil_teks, nama_guru, nama_ks, tgl_full)
                st.download_button(
                    label="📥 UNDUH SEBAGAI PDF (MASTER IBISCHOOL)",
                    data=pdf_bytes,
                    file_name=f"RKH_Ibischool_{subtopik}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Sistem Sibuk atau API Bermasalah: {e}")

