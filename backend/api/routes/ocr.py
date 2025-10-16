"""
OCR识别API路由
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
    """从上传的图片中提取文字"""
    
    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="文件必须是图片格式")
    
    try:
        # 保存上传的文件
        upload_dir = "uploads/ocr"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # OCR识别
        text, confidence = ocr_processor.extract_text(file_path, language)
        
        # 删除临时文件
        os.remove(file_path)
        
        return OCRResponse(
            text=text,
            confidence=confidence,
            language=language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")


@router.post("/url", response_model=OCRResponse)
async def extract_text_from_url(
    image_url: str,
    language: str = "chi_sim+eng"
):
    """从URL图片中提取文字"""
    
    try:
        # OCR识别
        text, confidence = ocr_processor.extract_text_from_url(image_url, language)
        
        return OCRResponse(
            text=text,
            confidence=confidence,
            language=language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")


@router.get("/languages")
async def get_supported_languages():
    """获取支持的OCR语言列表"""
    languages = {
        "chi_sim": "简体中文",
        "chi_tra": "繁体中文",
        "eng": "英文",
        "chi_sim+eng": "简体中文+英文",
        "chi_tra+eng": "繁体中文+英文"
    }
    return {"languages": languages}
