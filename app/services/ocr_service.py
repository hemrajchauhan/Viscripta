## app/services/ocr_service.py

import cv2
import pytesseract
import numpy as np
from paddleocr import PaddleOCR
from fastapi import UploadFile
from PIL import Image
from app.utils.image_utils import save_upload_to_temp

# Initialize OCR engine
ocr_engine = PaddleOCR(use_angle_cls=True, lang=['en','de'])

async def perform_ocr(file: UploadFile) -> str:
    """
    Extract text from the uploaded file using PaddleOCR.
    """
    # Save upload to temp file
    path = save_upload_to_temp(file)
    # Preprocess for cleaner input
    ocr = PaddleOCR(
        use_doc_orientation_classify=False, 
        use_doc_unwarping=False, 
        use_textline_orientation=False) # text detection + text recognition
    # ocr = PaddleOCR(use_doc_orientation_classify=True, use_doc_unwarping=True) # text image preprocessing + text detection + textline orientation classification + text recognition
    # ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False) # text detection + textline orientation classification + text recognition
    # ocr = PaddleOCR(
    #     text_detection_model_name="PP-OCRv5_server_det",
    #     text_recognition_model_name="PP-OCRv5_server_rec",
    #     use_doc_orientation_classify=False,
    #     use_doc_unwarping=False,
    #     use_textline_orientation=False) # Switch to PP-OCRv5_server models

    result = ocr.predict(path)
    texts = []
#    scores = []
    for res in result:
        info = res.json
        rec = info['res']
        texts.append(rec['rec_texts'])
#        scores.append(rec['rec_scores'])
    
#    flat = [x for s in scores for x in (s if isinstance(s, (list, tuple)) else [s])]
#    avg_confidence = sum(flat) / len(flat) if flat else 0.0
#    print("Recognized lines and their confidences:")
    for text in texts:
        # If t is a list of lines, join them into one string
        if isinstance(text, (list, tuple)):
            text = " ".join(text)
    return text

async def extract_table(file: UploadFile) -> dict:
    path = save_upload_to_temp(file)
    # Attempt PaddleOCR table detection
    raw_result = ocr_engine.predict(path)
    if raw_result:
        # Serialize numpy arrays to lists for JSON
        def serialize(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, list):
                return [serialize(x) for x in obj]
            if isinstance(obj, tuple):
                return [serialize(x) for x in obj]
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            return obj

        result = serialize(raw_result)
        return {"method": "paddleocr", "result": result}

    # Fallback: OpenCV + Tesseract
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,30))
    horizontal = cv2.dilate(cv2.erode(thresh, h_kernel), h_kernel)
    vertical = cv2.dilate(cv2.erode(thresh, v_kernel), v_kernel)
    mask = cv2.add(horizontal, vertical)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cells = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 30 and h > 20:
            cell_img = img[y:y+h, x:x+w]
            txt = pytesseract.image_to_string(cell_img, config='--psm 7').strip()
            cells.append({"x": x, "y": y, "w": w, "h": h, "text": txt})
    return {"method": "fallback", "cells": cells}
