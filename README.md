# 📄 Viscripta

**Viscripta** is a fast, modular API for intelligent PDF and OCR processing. Built with **FastAPI**, it combines the power of **PaddleOCR**, **Tesseract**, and **PyPDF** to handle scanned documents, extract structured text, and parse tables — all through a clean, developer-friendly interface.

> ✨ *Viscripta – Document intelligence through vision and precision.*

---

## 🚀 Core Features

### 📄 PDF Tools
- ✅ Merge multiple PDF files
- ✅ *Coming Soon*: Split PDFs by page ranges
- ✅ *Coming Soon*: Rotate, delete, or reorder pages
- ✅ *Coming Soon*: Convert images (JPG/PNG) to PDF
- ✅ *Coming Soon*: Add watermark (text/image) to PDF pages

### 🔍 OCR & Text Extraction
- ✅ OCR for scanned PDFs and images (PaddleOCR)
- ✅ Table extraction from scans with fallback logic
- 🧪 *Coming Soon*: Generate searchable PDFs with embedded OCR text

### 🧠 Smart Table Parsing
- Detect and extract table structures using:
  - PaddleOCR (deep learning)
  - OpenCV + Tesseract (fallback)
- Export results as structured JSON or CSV

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/hemrajchauhan/viscripta.git
cd viscripta
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract (Linux/macOS)
```bash
sudo apt install tesseract-ocr
```

---

## ▶️ Running the API
```bash
uvicorn main:app --reload
```

Access the API at:
http://localhost:8000

Swagger docs:
http://localhost:8000/docs

---

## 🧪 Example Usage
## 📌 Merge PDFs
```bash
curl -X POST http://localhost:8000/merge \
  -F "files=@file1.pdf" -F "files=@file2.pdf" \
  --output merged.pdf
```

## 📌 OCR Image
```bash
curl -X POST http://localhost:8000/ocr \
  -F "file=@scan.png"
```

## 📌 Extract Table from Scanned Document
```bash
curl -X POST http://localhost:8000/extract-table \
  -F "file=@table_image.jpg"
```

---

## 📦 Deployment
Run with Docker (optional)
Coming soon – Dockerfile with PaddleOCR runtime and FastAPI app.

---

## 🧠 Tech Stack
- FastAPI – Lightweight Python API framework
- PaddleOCR – Advanced OCR with table layout support
- Tesseract – OCR fallback engine
- PyPDF / pdfplumber – PDF handling and page operations
- OpenCV – Visual grid detection and image pre-processing

---

## 🤝 Contributing
Contributions welcome! Please:
- Open an issue to propose a feature or bugfix
- Fork the repo and submit a pull request
- Follow Pythonic code style and include docstrings

---

## 📜 License
[Apache License 2.0](https://github.com/hemrajchauhan/Viscripta/blob/main/LICENSE) © [Hemraj Chauhan]
---

## 🌐 Contact
Created by [Hemraj Chauhan](https://hemrajchauhan.com)

Reach out with ideas, feature requests, or collaboration offers!
