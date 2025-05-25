## tests/test_endpoints.py

import io
import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from PIL import Image, ImageDraw, ImageFont

from app.main import app

client = TestClient(app)

def create_blank_pdf(page_count=1):
    writer = PdfWriter()
    for _ in range(page_count):
        writer.add_blank_page(width=72, height=72)
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    return buf


def create_text_image(text="Hello", size=(300, 100)):
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", size=28)  # a readable system font
    except:
        font = ImageFont.load_default()  # fallback
    draw.text((10, 10), text, fill='black', font=font)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def test_merge_pdfs():
    pdf1 = create_blank_pdf()
    pdf2 = create_blank_pdf()
    files = [
        ('files', ('a.pdf', pdf1.getvalue(), 'application/pdf')),
        ('files', ('b.pdf', pdf2.getvalue(), 'application/pdf'))
    ]
    response = client.post("/merge/", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > len(pdf1.getvalue())


def test_ocr_endpoint():
    img = create_text_image("Test OCR")
    files = {'file': ('test.png', img.getvalue(), 'image/png')}
    response = client.post("/ocr/", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert "text" in json_data
    assert "Test" in json_data["text"]


def test_extract_table_endpoint():
    size = (300, 200)
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    draw.line((50, 50, 250, 50), fill='black')
    draw.line((50, 150, 250, 150), fill='black')
    draw.line((50, 50, 50, 150), fill='black')
    draw.line((250, 50, 250, 150), fill='black')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    files = {'file': ('table.png', buf.getvalue(), 'image/png')}
    response = client.post("/extract-table/", files=files)
    assert response.status_code == 200
    result = response.json()
    assert "method" in result
    assert result["method"] in ("paddleocr", "fallback")
    assert isinstance(result.get("cells", []), list)
