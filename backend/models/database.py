"""
数据库配置和连接管理
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/campus_lost_found")

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


class LostItem(Base):
    """失物模型"""
    __tablename__ = "lost_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="失物标题")
    description = Column(Text, comment="失物描述")
    category = Column(String(50), comment="物品类别")
    location = Column(String(200), comment="发现地点")
    contact_info = Column(String(200), comment="联系方式")
    image_url = Column(String(500), comment="图片URL")
    ocr_text = Column(Text, comment="OCR识别的文字")
    ai_category = Column(String(50), comment="AI识别的类别")
    confidence = Column(Float, comment="AI识别置信度")
    status = Column(String(20), default="lost", comment="状态：lost/found/claimed")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否有效")


class FoundItem(Base):
    """招领模型"""
    __tablename__ = "found_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="招领标题")
    description = Column(Text, comment="招领描述")
    category = Column(String(50), comment="物品类别")
    location = Column(String(200), comment="发现地点")
    contact_info = Column(String(200), comment="联系方式")
    image_url = Column(String(500), comment="图片URL")
    ocr_text = Column(Text, comment="OCR识别的文字")
    ai_category = Column(String(50), comment="AI识别的类别")
    confidence = Column(Float, comment="AI识别置信度")
    status = Column(String(20), default="found", comment="状态：found/claimed")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否有效")


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)
