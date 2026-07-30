Berikut adalah draf file README yang sudah difokuskan sepenuhnya pada **Komparasi, Pemasangan, dan Perbedaan Penggunaan antara Local AI Agent dan Cloud AI Agent**, tanpa bagian *roadmap* atau item pendukung lainnya.

---

# 🚀 SIOD Agent (Smart Infrastructure Observability & Decision Agent)

> AI-powered Infrastructure Observability Agent built with Python, Goose CLI, Ollama, and Llama 3.2.

---

# 📖 Overview

**SIOD Agent** adalah repositori dan panduan praktis dalam menerapkan *Agentic AI* untuk kebutuhan *Infrastructure Observability* dan otomatisasi sistem. Documentasi ini memuat **perbandingan mendalam antara Local AI Agent dan Cloud AI Agent**, petunjuk **pemasangan (installation)**, serta **perbedaan alur penggunaan (usage workflow)** pada kedua arsitektur tersebut.

---

# ⚖️ Perbandingan: Local AI Agent vs. Cloud AI Agent

| Parameter | Local AI Agent (e.g., Ollama + Llama 3.2) | Cloud AI Agent (e.g., OpenAI GPT-4o / Claude) |
| --- | --- | --- |
| **Privasi & Keamanan Data** | **Sangat Tinggi** — Seluruh data, log, dan kueri sistem diproses di server lokal tanpa ada trafik keluar. | **Terbatas** — Data dan konteks sistem dikirim via API ke server penyedia layanan (*third-party*). |
| **Biaya Operasional** | **Gratis (Bebas Token)** — Hanya membutuhkan modal perangkat keras/server lokal (*CapEx*). | **Pay-per-Use** — Membayar biaya API berdasarkan jumlah token yang digunakan (*OpEx*). |
| **Ketergantungan Internet** | **100% Offline** — Dapat berjalan pada jaringan terisolasi (*air-gapped environment*). | **Wajib Online** — Membutuhkan koneksi internet publik yang stabil dan cepat. |
| **Kemampuan Reasoning** | Terbatas pada kapasitas model lokal (misal: 3B–14B parameter). | **Sangat Tinggi** — Mampu menyelesaikan penalaran logika dan instruksi yang sangat kompleks. |
| **Kapasitas Context Window** | Dibatasi oleh alokasi RAM/VRAM fisik di server lokal. | Sangat Besar (Mencapai 128k hingga 1M+ token per sesi). |
| **Kecepatan Response** | Cepat untuk model kecil, namun bergantung pada spesifikasi CPU/GPU lokal. | Konsisten dan cepat, namun dipengaruhi oleh *network latency*. |

---

# 🛠️ Petunjuk Pemasangan (Installation)

### Option A: Pemasangan Local AI Agent (Ollama + Goose)

Gunakan metode ini jika kamu menginginkan privasi mutlak dan kebebasan biaya token.

#### 1. Pasang Engine Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh

```

#### 2. Unduh Model & Buat Custom Context Window

Buat file `Modelfile` untuk memperbesar alokasi *context slot* (mencegah batas token cepat habis):

```dockerfile
FROM llama3.2:3b
PARAMETER num_ctx 16384

```

Jalankan perintah pembuatan model:

```bash
ollama create llama3.2-siod -f Modelfile

```

#### 3. Konfigurasi Goose CLI

Edit file konfigurasi Goose pada lokasi `~/.config/goose/config.yaml`:

```yaml
GOOSE_TELEMETRY_ENABLED: false
OLLAMA_HOST: localhost
active_provider: ollama
providers:
  ollama:
    enabled: true
    model: llama3.2-siod
    configured: true
extensions:
  developer:
    enabled: true
    type: builtin
    name: developer
  todo:
    enabled: true
    type: platform
    name: todo

```

---

### Option B: Pemasangan Cloud AI Agent (OpenAI / Anthropic + Goose)

Gunakan metode ini jika kamu membutuhkan kemampuan analisis log dan *troubleshooting* tingkat tinggi.

#### 1. Ekspor API Key ke Environment System

```bash
# Untuk OpenAI (GPT-4o / GPT-4o-mini)
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxx"

# Atau untuk Anthropic (Claude 3.5 Sonnet)
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxx"

```

#### 2. Konfigurasi Goose CLI

Sesuaikan file `~/.config/goose/config.yaml` untuk mengarahkan penyedia utama ke Cloud Provider:

```yaml
GOOSE_TELEMETRY_ENABLED: false
active_provider: openai
providers:
  openai:
    enabled: true
    model: gpt-4o-mini
    configured: true
extensions:
  developer:
    enabled: true
    type: builtin
    name: developer
  todo:
    enabled: true
    type: platform
    name: todo

```

---

# 🔄 Perbedaan Penggunaan (Usage Workflow)

### 1. Cara Menjalankan Local AI Agent

Saat menggunakan Local AI Agent, kamu harus memastikan *service* backend lokal aktif terlebih dahulu sebelum membuka sesi agen.

```bash
# 1. Pastikan service Ollama berjalan di latar belakang
systemctl status ollama

# 2. Jalankan sesi Goose bersih (mengabaikan riwayat lama agar token efisien)
goose session start --new

```

* **Manajemen Token:** Pada model lokal, perhatikan akumulasi ekstensi yang aktif. Jika respons mulai melambat, matikan ekstensi yang tidak terpakai pada `config.yaml`.
* **Karakteristik Respons:** Respons diproses secara internal oleh GPU/CPU lokal. Tidak ada risiko *rate limit* dari penyedia API luar.

---

### 2. Cara Menjalankan Cloud AI Agent

Pada Cloud AI Agent, kamu tidak perlu mengelola *service* lokal. Semua beban komputasi di-handle oleh *cloud provider*.

```bash
# 1. Pastikan API Key sudah terpasang di sesi terminal
echo $OPENAI_API_KEY

# 2. Jalankan Goose CLI secara langsung
goose session

```

* **Manajemen Token:** Agen dapat membaca direktori besar atau file log berukuran raksasa tanpa perlu khawatir kehabisan *context window*.
* **Karakteristik Respons:** Lebih andal dalam mengeksekusi instruksi *tool calling* yang bertumpuk dan rumit, namun setiap interaksi memotong kuota/saldo API kamu.

---

# 📂 Project Structure

```
siod-agent/

├── Modelfile                # Custom configuration untuk context slot Ollama (Local Setup)
├── config/
│   └── goose_config.yaml    # Template konfigurasi Goose (Local/Cloud)
├── logs/
│   └── agent_session.log    # Log eksekusi agen
└── README.md

```

---

# 📄 License

This project is created for educational, research, and portfolio purposes.
