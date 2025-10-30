"""
数据库配置和连接管理
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 数据库配置 - Docker环境使用PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/campus_db")
# 如果URL以postgres://开头，替换为postgresql://（Render兼容性）
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

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
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="发布者用户ID")
    owner = relationship("User", back_populates="lost_items")


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
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="发布者用户ID")
    owner = relationship("User", back_populates="found_items")


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # user/admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lost_items = relationship("LostItem", back_populates="owner")
    found_items = relationship("FoundItem", back_populates="owner")


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
    # 轻量迁移：为已有表补充 owner_id 字段
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE lost_items ADD COLUMN IF NOT EXISTS owner_id INTEGER"))
        except Exception:
            pass

    # 初始化默认管理员账户（仅本地开发使用）
    try:
        from sqlalchemy.orm import Session
        import hashlib
        db: Session = SessionLocal()
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=hashlib.sha256("123456".encode("utf-8")).hexdigest(),
                role="admin",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(admin)
            db.commit()
    except Exception:
        pass
        try:
            conn.execute(text("ALTER TABLE found_items ADD COLUMN IF NOT EXISTS owner_id INTEGER"))
        except Exception:
            pass
