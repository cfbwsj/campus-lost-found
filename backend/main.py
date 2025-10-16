"""
校园失物招领系统 - 主应用入口
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
    """应用生命周期管理"""
    # 启动时执行
    init_db()
    # 创建上传目录
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/images", exist_ok=True)
    yield
    # 关闭时执行


# 创建FastAPI应用
app = FastAPI(
    title="校园失物招领系统",
    description="基于AI技术的智能校园失物招领平台",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 注册路由
app.include_router(items.router, prefix="/api/items", tags=["失物管理"])
app.include_router(search.router, prefix="/api/search", tags=["搜索功能"])
app.include_router(upload.router, prefix="/api/upload", tags=["文件上传"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["OCR识别"])
app.include_router(classify.router, prefix="/api/classify", tags=["AI分类"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "校园失物招领系统API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "服务运行正常"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
