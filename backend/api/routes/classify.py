"""
AI��Ʒ����API·��
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from utils.ai_classifier import item_classifier
from models.schemas import ClassificationResponse

router = APIRouter()


@router.post("/", response_model=ClassificationResponse)
async def classify_image(file: UploadFile = File(...)):
    """���ϴ���ͼƬ������Ʒ����"""
    
    # ��֤�ļ�����
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="�ļ�������ͼƬ��ʽ")
    
    try:
        # �����ϴ����ļ�
        import os
        import shutil
        
        upload_dir = "uploads/classify"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # AI����
        category, confidence, subcategories = item_classifier.classify_image(file_path)
        
        # ɾ����ʱ�ļ�
        os.remove(file_path)
        
        # ��ȡ�����������
        category_name = item_classifier.get_category_name(category)
        
        return ClassificationResponse(
            category=category_name,
            confidence=confidence,
            subcategories=subcategories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI����ʧ��: {str(e)}")


@router.post("/url", response_model=ClassificationResponse)
async def classify_image_from_url(image_url: str):
    """��URLͼƬ������Ʒ����"""
    
    try:
        # AI����
        category, confidence, subcategories = item_classifier.classify_image_from_url(image_url)
        
        # ��ȡ�����������
        category_name = item_classifier.get_category_name(category)
        
        return ClassificationResponse(
            category=category_name,
            confidence=confidence,
            subcategories=subcategories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI����ʧ��: {str(e)}")


@router.get("/categories")
async def get_categories():
    """��ȡ����֧�ֵ���Ʒ���"""
    categories = item_classifier.get_all_categories()
    return {"categories": categories}


@router.get("/model-info")
async def get_model_info():
    """��ȡģ����Ϣ"""
    return {
        "model_name": "ResNet50",
        "framework": "PyTorch",
        "device": str(item_classifier.device),
        "categories_count": len(item_classifier.categories)
    }
