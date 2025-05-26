# 🧠 DeepSeek Batch Name Matcher

Tool ini digunakan untuk mencocokkan nama dalam dataset terhadap nama standar menggunakan **DeepSeek LLM API**. Sistem ini mendukung pemrosesan batch dan menghasilkan output dalam format JSON atau Excel.

---

## 📁 Struktur Proyek

```
.
├── batch_runner.py                # Script utama untuk menjalankan proses batch
├── match_standard_name_json.py   # Modul logika pencocokan nama standar
├── config.env                     # File konfigurasi untuk API Key dan model
├── requirements.txt              # Daftar dependensi Python
├── file/                          # Folder berisi file input Excel
│   ├── BHMP_Hospital.xlsx
│   ├── BHMP_Hospital_Brand.xlsx
│   └── standard_name_DB.xlsx
```

---

## ⚙️ Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/deepseek-name-matcher.git
cd deepseek-name-matcher
```

### 2. Buat Virtual Environment (Opsional)

```bash
python -m venv venv
source venv/bin/activate        # Untuk Windows: venv\Scripts\activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key

Edit file `config.env` dan masukkan API key DeepSeek kamu:

```env
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_API_ENDPOINT=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_MODEL=deepseek-chat
```

> Kamu juga bisa menambahkan `.env` file jika menggunakan konfigurasi lokal secara langsung.

---

## 🚀 Menjalankan Program

```bash
python batch_runner.py
```

Script akan:
- Membaca konfigurasi dari `config.env`
- Memproses input data dari folder `file/`
- Mengirim data ke DeepSeek API dan mencocokkan nama
- Menyimpan hasil yang telah dicocokkan ke output file

Pastikan file input berada di dalam folder `file/` dan struktur kolom sesuai dengan yang diharapkan di dalam script.

---

## 🧩 Dependensi

Berikut adalah library yang digunakan:

- `openai`
- `python-dotenv`
- `pandas`
- `openpyxl`
- `tqdm`

Instal dengan:

```bash
pip install -r requirements.txt
```

---

## 📄 Lisensi

MIT License.
