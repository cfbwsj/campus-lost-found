"""
У԰ʧ������ϵͳ - ��Ӧ�����
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os

from api.routes import items, search, upload, ocr, classify
from models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ӧ���������ڹ���"""
    # ����ʱִ��
    init_db()
    # �����ϴ�Ŀ¼
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/images", exist_ok=True)
    yield
    # �ر�ʱִ��


# ����FastAPIӦ��
app = FastAPI(
    title="У԰ʧ������ϵͳ",
    description="����AI����������У԰ʧ������ƽ̨",
    version="1.0.0",
    lifespan=lifespan
)

# ����CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ��̬�ļ�����
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ע��·��
app.include_router(items.router, prefix="/api/items", tags=["ʧ�����"])
app.include_router(search.router, prefix="/api/search", tags=["��������"])
app.include_router(upload.router, prefix="/api/upload", tags=["�ļ��ϴ�"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["OCRʶ��"])
app.include_router(classify.router, prefix="/api/classify", tags=["AI����"])


@app.get("/")
async def root():
    """��·��"""
    return {
        "message": "У԰ʧ������ϵͳAPI",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """�������"""
    return {"status": "healthy", "message": "������������"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
