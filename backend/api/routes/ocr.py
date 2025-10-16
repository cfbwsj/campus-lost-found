"""
OCRʶ��API·��
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
import os
import shutil
from utils.ocr import ocr_processor
from models.schemas import OCRResponse

router = APIRouter()


@router.post("/", response_model=OCRResponse)
async def extract_text_from_image(
    file: UploadFile = File(...),
    language: str = Form("chi_sim+eng")
):
    """���ϴ���ͼƬ����ȡ����"""
    
    # ��֤�ļ�����
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="�ļ�������ͼƬ��ʽ")
    
    try:
        # �����ϴ����ļ�
        upload_dir = "uploads/ocr"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # OCRʶ��
        text, confidence = ocr_processor.extract_text(file_path, language)
        
        # ɾ����ʱ�ļ�
        os.remove(file_path)
        
        return OCRResponse(
            text=text,
            confidence=confidence,
            language=language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCRʶ��ʧ��: {str(e)}")


@router.post("/url", response_model=OCRResponse)
async def extract_text_from_url(
    image_url: str,
    language: str = "chi_sim+eng"
):
    """��URLͼƬ����ȡ����"""
    
    try:
        # OCRʶ��
        text, confidence = ocr_processor.extract_text_from_url(image_url, language)
        
        return OCRResponse(
            text=text,
            confidence=confidence,
            language=language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCRʶ��ʧ��: {str(e)}")


@router.get("/languages")
async def get_supported_languages():
    """��ȡ֧�ֵ�OCR�����б�"""
    languages = {
        "chi_sim": "��������",
        "chi_tra": "��������",
        "eng": "Ӣ��",
        "chi_sim+eng": "��������+Ӣ��",
        "chi_tra+eng": "��������+Ӣ��"
    }
    return {"languages": languages}
