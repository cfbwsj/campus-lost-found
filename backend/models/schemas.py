"""
Pydantic数据模型
"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class ItemBase(BaseModel):
    """失物基础模型"""
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None


class ItemCreate(ItemBase):
    """创建物品模型（同时用于失物与招领）"""
    image_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_category: Optional[str] = None
    confidence: Optional[float] = None
    status: Optional[str] = None


class ItemUpdate(BaseModel):
    """更新失物模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None
    status: Optional[str] = None


class LostItem(ItemBase):
    """失物模型"""
    id: int
    image_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_category: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "lost"
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class FoundItem(ItemBase):
    """招领模型"""
    id: int
    image_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_category: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "found"
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    """物品响应模型"""
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None
    image_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_category: Optional[str] = None
    confidence: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: datetime
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str
    category: Optional[str] = None
    location: Optional[str] = None
    limit: int = 20
    offset: int = 0


class SearchItem(BaseModel):
    """搜索结果项（包含来源类型）"""
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None
    image_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_category: Optional[str] = None
    confidence: Optional[float] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    item_type: Optional[str] = None

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """搜索响应模型"""
    items: List[SearchItem]
    total: int
    page: int
    size: int


class OCRRequest(BaseModel):
    """OCR请求模型"""
    image_url: str
    language: str = "chi_sim+eng"  # 中文简体+英文


class OCRResponse(BaseModel):
    """OCR响应模型"""
    text: str
    confidence: float
    language: str


class ClassificationRequest(BaseModel):
    """分类请求模型"""
    image_url: str


class ClassificationResponse(BaseModel):
    """分类响应模型"""
    category: str
    confidence: float
    subcategories: Optional[List[str]] = None


class UploadResponse(BaseModel):
    """上传响应模型"""
    filename: str
    url: str
    size: int
    content_type: str
