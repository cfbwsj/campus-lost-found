"""
AI物品分类API路由
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from utils.ai_classifier import item_classifier
from models.schemas import ClassificationResponse

router = APIRouter()


@router.post("/", response_model=ClassificationResponse)
async def classify_image(file: UploadFile = File(...)):
    """对上传的图片进行物品分类"""
    
    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="文件必须是图片格式")
    
    try:
        # 保存上传的文件
        import os
        import shutil
        
        upload_dir = "uploads/classify"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # AI分类
        category, confidence, subcategories = item_classifier.classify_image(file_path)
        
        # 删除临时文件
        os.remove(file_path)
        
        # 获取类别中文名称
        category_name = item_classifier.get_category_name(category)
        
        return ClassificationResponse(
            category=category_name,
            confidence=confidence,
            subcategories=subcategories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI分类失败: {str(e)}")


@router.post("/url", response_model=ClassificationResponse)
async def classify_image_from_url(image_url: str):
    """对URL图片进行物品分类"""
    
    try:
        # AI分类
        category, confidence, subcategories = item_classifier.classify_image_from_url(image_url)
        
        # 获取类别中文名称
        category_name = item_classifier.get_category_name(category)
        
        return ClassificationResponse(
            category=category_name,
            confidence=confidence,
            subcategories=subcategories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI分类失败: {str(e)}")


@router.get("/categories")
async def get_categories():
    """获取所有支持的物品类别"""
    categories = item_classifier.get_all_categories()
    return {"categories": categories}


@router.get("/model-info")
async def get_model_info():
    """获取模型信息"""
    return {
        "model_name": "ResNet50",
        "framework": "PyTorch",
        "device": str(item_classifier.device),
        "categories_count": len(item_classifier.categories)
    }
