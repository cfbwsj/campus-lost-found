"""
Pydantic����ģ��
"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class ItemBase(BaseModel):
    """ʧ�����ģ��"""
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None


class ItemCreate(ItemBase):
    """����ʧ��ģ��"""
    pass


class ItemUpdate(BaseModel):
    """����ʧ��ģ��"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None
    status: Optional[str] = None


class LostItem(ItemBase):
    """ʧ��ģ��"""
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
    """����ģ��"""
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
    """��Ʒ��Ӧģ��"""
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

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    """��������ģ��"""
    query: str
    category: Optional[str] = None
    location: Optional[str] = None
    limit: int = 20
    offset: int = 0


class SearchResponse(BaseModel):
    """������Ӧģ��"""
    items: List[ItemResponse]
    total: int
    page: int
    size: int


class OCRRequest(BaseModel):
    """OCR����ģ��"""
    image_url: str
    language: str = "chi_sim+eng"  # ���ļ���+Ӣ��


class OCRResponse(BaseModel):
    """OCR��Ӧģ��"""
    text: str
    confidence: float
    language: str


class ClassificationRequest(BaseModel):
    """��������ģ��"""
    image_url: str


class ClassificationResponse(BaseModel):
    """������Ӧģ��"""
    category: str
    confidence: float
    subcategories: Optional[List[str]] = None


class UploadResponse(BaseModel):
    """�ϴ���Ӧģ��"""
    filename: str
    url: str
    size: int
    content_type: str
