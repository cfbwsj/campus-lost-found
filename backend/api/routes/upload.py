"""
�ļ��ϴ�API·��
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import os
import shutil
import uuid
from datetime import datetime
from models.schemas import UploadResponse

router = APIRouter()

# ������ļ�����
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """�ϴ������ļ�"""
    
    # ��֤�ļ���С
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="�ļ���С���ܳ���10MB")
    
    # ��֤�ļ�����
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="��֧�ֵ��ļ���ʽ")
    
    try:
        # ����Ψһ�ļ���
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # �����ϴ�Ŀ¼�������ڷ��ࣩ
        date_dir = datetime.now().strftime("%Y/%m/%d")
        upload_dir = os.path.join("uploads", "images", date_dir)
        os.makedirs(upload_dir, exist_ok=True)
        
        # �����ļ�
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # ���ɷ���URL
        file_url = f"/uploads/images/{date_dir}/{unique_filename}"
        
        return UploadResponse(
            filename=unique_filename,
            url=file_url,
            size=file.size,
            content_type=file.content_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"�ļ��ϴ�ʧ��: {str(e)}")


@router.post("/multiple", response_model=List[UploadResponse])
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """�ϴ�����ļ�"""
    
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="���ֻ���ϴ�5���ļ�")
    
    results = []
    
    for file in files:
        try:
            # ��֤�ļ���С
            if file.size > MAX_FILE_SIZE:
                results.append({
                    "error": f"�ļ� {file.filename} ��С��������",
                    "filename": file.filename
                })
                continue
            
            # ��֤�ļ�����
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                results.append({
                    "error": f"�ļ� {file.filename} ��ʽ��֧��",
                    "filename": file.filename
                })
                continue
            
            # ����Ψһ�ļ���
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # �����ϴ�Ŀ¼
            date_dir = datetime.now().strftime("%Y/%m/%d")
            upload_dir = os.path.join("uploads", "images", date_dir)
            os.makedirs(upload_dir, exist_ok=True)
            
            # �����ļ�
            file_path = os.path.join(upload_dir, unique_filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # ���ɷ���URL
            file_url = f"/uploads/images/{date_dir}/{unique_filename}"
            
            results.append(UploadResponse(
                filename=unique_filename,
                url=file_url,
                size=file.size,
                content_type=file.content_type
            ))
            
        except Exception as e:
            results.append({
                "error": f"�ļ� {file.filename} �ϴ�ʧ��: {str(e)}",
                "filename": file.filename
            })
    
    return results


@router.delete("/{filename}")
async def delete_file(filename: str):
    """ɾ���ϴ����ļ�"""
    
    try:
        # �����ļ�
        upload_dir = "uploads/images"
        for root, dirs, files in os.walk(upload_dir):
            if filename in files:
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                return {"message": "�ļ�ɾ���ɹ�"}
        
        raise HTTPException(status_code=404, detail="�ļ�������")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"�ļ�ɾ��ʧ��: {str(e)}")


@router.get("/info")
async def get_upload_info():
    """��ȡ�ϴ���Ϣ"""
    return {
        "max_file_size": MAX_FILE_SIZE,
        "allowed_extensions": list(ALLOWED_EXTENSIONS),
        "max_files": 5
    }
