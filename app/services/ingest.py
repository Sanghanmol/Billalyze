import pytesseract
from PIL import Image
import pdfplumber
import re
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_vendor(text: str) -> str:
    lines = text.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    # Heuristic 1: Look for words like Mart, Store, etc.
    for line in lines[:5]:
        if re.search(
            r"(mart|store|supermarket|bazaar|bazar|shop|retail|traders)", line, re.I
        ):
            return line

    for line in lines[:5]:
        if line.isupper() and 2 <= len(line.split()) <= 4:
            return line
    if lines:
        return lines[0]

    return "Unknown"


def detect_category(text: str) -> str:
    text_lower = text.lower()

    category_keywords = {
        "Groceries": ["grocery", "vegetable", "fruit", "supermarket", "kirana", "mart"],
        "Electronics": ["laptop", "phone", "electronics", "charger", "tv", "usb"],
        "Clothing": [
            "shirt",
            "jeans",
            "clothing",
            "apparel",
            "fashion",
            "kurta",
            "t-shirt",
        ],
        "Food & Dining": [
            "restaurant",
            "food",
            "meal",
            "dine",
            "pizza",
            "burger",
            "cafe",
            "biryani",
        ],
        "Transportation": [
            "uber",
            "ola",
            "taxi",
            "auto",
            "cab",
            "ride",
            "bus",
            "train",
        ],
        "Healthcare": ["medicine", "hospital", "clinic", "pharma", "health", "doctor"],
        "Utilities": ["electricity", "water", "bill", "gas", "internet", "broadband"],
        "Entertainment": ["movie", "netflix", "hotstar", "ticket", "theatre", "event"],
        "Education": ["tuition", "school", "college", "course", "exam", "learning"],
    }

    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return category

    return "General"


def extract_data(text: str) -> dict:
    vendor = extract_vendor(text)
    amount = re.search(
        r"(?:₹|\$|Rs\.?|INR)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)", text
    )
    date = re.search(r"(\d{2}[-/]\d{2}[-/]\d{4})", text)

    return {
        "vendor": vendor,
        "amount": float(amount.group(1).replace(",", "")) if amount else 0.0,
        "date": (
            datetime.strptime(date.group(1), "%d-%m-%Y").date()
            if date
            else datetime.today().date()
        ),
        "category": detect_category(text),
    }


def process_file(file_path: str) -> dict:
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith((".jpg", ".jpeg", ".png")):
        text = pytesseract.image_to_string(Image.open(file_path))
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format")

    return extract_data(text)
