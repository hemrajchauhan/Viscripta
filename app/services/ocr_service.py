## app/services/ocr_service.py

import io
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import pytesseract
import cv2
from fastapi import UploadFile
from app.utils.image_utils import save_upload_to_temp

# Initialize engines
ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')

def _ocr_with_paddle(image_path: str) -> dict:
    result = ocr_engine.ocr(image_path, cls=True)
    return {"method": "paddleocr", "result": result}

async def perform_ocr(file: UploadFile) -> str:
    path = save_upload_to_temp(file)
    # Try PaddleOCR first
    data = _ocr_with_paddle(path)
    # Concatenate text lines
    text = "\n".join([line[1][0] for line in data["result"]])
    return text

async def extract_table(file: UploadFile) -> dict:
    path = save_upload_to_temp(file)
    # Try PaddleOCR table detection
    table_data = _ocr_with_paddle(path)
    if table_data and table_data.get("result"):
        return table_data
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
        x,y,w,h = cv2.boundingRect(cnt)
        if w>30 and h>20:
            cell_img = img[y:y+h, x:x+w]
            txt = pytesseract.image_to_string(cell_img, config='--psm 7').strip()
            cells.append({"x":x, "y":y, "w":w, "h":h, "text":txt})
    return {"method": "fallback", "cells": cells}
