# -*- coding: utf-8 -*-
"""
Campus Lost & Found System - Main Application Entry
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
    """Application lifecycle management"""
    # Create upload directories first
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/images", exist_ok=True)
    os.makedirs("uploads/ocr", exist_ok=True)
    os.makedirs("uploads/classify", exist_ok=True)
    # Execute on startup
    init_db()
    yield
    # Execute on shutdown


# Ensure upload directories exist before app initialization
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/images", exist_ok=True)
os.makedirs("uploads/ocr", exist_ok=True)
os.makedirs("uploads/classify", exist_ok=True)

# Create FastAPI application
app = FastAPI(
    title="Campus Lost & Found System",
    description="AI-powered campus lost and found platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file service
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register routes
app.include_router(items.router, prefix="/api/items", tags=["Lost Items Management"])
app.include_router(search.router, prefix="/api/search", tags=["Search Functions"])
app.include_router(upload.router, prefix="/api/upload", tags=["File Upload"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["OCR Recognition"])
app.include_router(classify.router, prefix="/api/classify", tags=["AI Classification"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Campus Lost & Found System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "message": "Service is running normally"}


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
