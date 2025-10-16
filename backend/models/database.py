"""
���ݿ����ú����ӹ���
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# ���ݿ�����
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/campus_lost_found")

# �������ݿ�����
engine = create_engine(DATABASE_URL)

# �����Ự����
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ��������ģ����
Base = declarative_base()


class LostItem(Base):
    """ʧ��ģ��"""
    __tablename__ = "lost_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="ʧ�����")
    description = Column(Text, comment="ʧ������")
    category = Column(String(50), comment="��Ʒ���")
    location = Column(String(200), comment="���ֵص�")
    contact_info = Column(String(200), comment="��ϵ��ʽ")
    image_url = Column(String(500), comment="ͼƬURL")
    ocr_text = Column(Text, comment="OCRʶ�������")
    ai_category = Column(String(50), comment="AIʶ������")
    confidence = Column(Float, comment="AIʶ�����Ŷ�")
    status = Column(String(20), default="lost", comment="״̬��lost/found/claimed")
    created_at = Column(DateTime, default=datetime.utcnow, comment="����ʱ��")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="����ʱ��")
    is_active = Column(Boolean, default=True, comment="�Ƿ���Ч")


class FoundItem(Base):
    """����ģ��"""
    __tablename__ = "found_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="�������")
    description = Column(Text, comment="��������")
    category = Column(String(50), comment="��Ʒ���")
    location = Column(String(200), comment="���ֵص�")
    contact_info = Column(String(200), comment="��ϵ��ʽ")
    image_url = Column(String(500), comment="ͼƬURL")
    ocr_text = Column(Text, comment="OCRʶ�������")
    ai_category = Column(String(50), comment="AIʶ������")
    confidence = Column(Float, comment="AIʶ�����Ŷ�")
    status = Column(String(20), default="found", comment="״̬��found/claimed")
    created_at = Column(DateTime, default=datetime.utcnow, comment="����ʱ��")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="����ʱ��")
    is_active = Column(Boolean, default=True, comment="�Ƿ���Ч")


def get_db():
    """��ȡ���ݿ�Ự"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """��ʼ�����ݿ�"""
    Base.metadata.create_all(bind=engine)
