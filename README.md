# 🧾 Receipt and Bill Parser App

A full-stack mini-application to upload receipts (images, PDFs, text files), extract structured data using OCR, and view insights such as total spend, top vendors, and trends.

---

## ✅ Features

- Upload `.jpg`, `.png`, `.pdf`, `.txt` files via API
- Extracts vendor, amount, date, and category
- Saves parsed data to SQLite database
- View analytics dashboard with charts and tables
- Native search, sort, and aggregations in Python

---

## 🛠️ Technologies Used

| Component        | Technology         | Purpose                                      |
|------------------|--------------------|----------------------------------------------|
| 🧠 Backend       | FastAPI            | API creation and routing                     |
| 💾 Database      | SQLite + SQLAlchemy| Lightweight storage, ORM for easy queries    |
| 📷 OCR Engine    | Tesseract (pytesseract) | Image and PDF text extraction           |
| 🖼️ Frontend      | Streamlit + Plotly | UI and visualizations                        |
| 📦 Validation    | Pydantic           | Type checking and data integrity             |
| 📁 File Parsing  | PyMuPDF / PIL      | PDF/image reading and preprocessing          |

---

## 🏗️ Architecture & Design Choices

- **Modular Structure**:
  - `backend/` handles ingestion, parsing, storage, and API endpoints
  - `frontend/` displays UI via Streamlit and hits backend APIs
  - `models/` defines data schemas via Pydantic and SQLAlchemy
- **Decoupled OCR**: Allows switching OCR backend if needed
- **Lightweight DB**: SQLite for ease and no external dependency
- **Custom Algorithms**: Sorting and searching implemented natively for learning and performance clarity

---

## 🔍 How It Works – User Journey

1. 🧾 **Upload Receipt** – User uploads a bill (image, PDF, or text)
2. 🔍 **Text Extraction** – OCR (pytesseract) or plain text parsing runs
3. 📊 **Data Extraction** – Regex and rule-based logic fetch:
   - Vendor
   - Date
   - Amount
4. 🗃️ **Storage** – Parsed data is validated and stored in SQLite
5. 📈 **Visualized Insights** – Streamlit displays:
   - Table of receipts
   - Spending summary
   - Top vendors (bar chart)
   - Trends (line chart)

---

## ⚙️ Setup Instructions

- git clone https://github.com/yourusername/receipt-parser-app.git
- cd receipt-parser-app
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\\Scripts\\activate
- pip install -r requirements.txt

---

## 🚀 Running the App

1. ⚙️ Start backend (FastAPI):
   uvicorn app.main:app --reload
   
2. Test file upload at:
   http://localhost:8000/docs (interactive Swagger UI)

3. 🌐 Start frontend (Streamlit):
- cd ui
- streamlit run dashboard.py
- Open in browser: http://localhost:8501

  ---

  ## 📉 Limitations

- OCR accuracy depends on image clarity and layout  
- Vendor and category mapping is rule-based and may miss some edge cases  
- Time-series graphs assume a consistent date format  
- Does not support multi-currency or multilingual OCR (yet)  

---

## 🤔 Assumptions

- All receipts contain a recognizable amount and date format  
- Receipts follow a mostly predictable format (common vendors, keywords)  
- Input files are small (not bulk-uploaded in thousands)  

---

## 🙏 Acknowledgment

This project was made with ❤️ to explore the intersection of OCR, data processing, and full-stack development.

---
