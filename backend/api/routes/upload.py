"""
文件上传API路由
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import os
import shutil
import uuid
from datetime import datetime
from models.schemas import UploadResponse

# 关闭该子路由自动斜杠重定向，避免 /api/upload → /api/upload/ 产生307导致CORS丢失
router = APIRouter(redirect_slashes=False)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """上传单个文件"""
    
    # 读取文件内容以获取大小（UploadFile无 size 属性）
    contents = await file.read()
    size_bytes = len(contents)
    # 重置指针以便后续写入使用（非必须，但更安全）
    file.file.seek(0)
    # 验证文件大小
    if size_bytes > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="文件大小不能超过10MB")
    
    # 验证文件类型
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不支持的文件格式")
    
    try:
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # 创建上传目录（按日期分类）
        date_dir = datetime.now().strftime("%Y/%m/%d")
        upload_dir = os.path.join("uploads", "images", date_dir)
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        # 生成访问URL（使用完整URL以支持跨域访问）
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        file_url = f"{base_url}/uploads/images/{date_dir}/{unique_filename}"
        
        return UploadResponse(
            filename=unique_filename,
            url=file_url,
            size=size_bytes,
            content_type=file.content_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


# 兼容无斜杠路径，避免浏览器重定向导致的CORS丢失
@router.post("")
async def upload_file_no_slash(file: UploadFile = File(...)):
    return await upload_file(file)


@router.post("/multiple", response_model=List[UploadResponse])
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """上传多个文件"""
    
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="最多只能上传5个文件")
    
    results = []
    
    for file in files:
        try:
            # 读取文件以获取大小
            contents = await file.read()
            size_bytes = len(contents)
            file.file.seek(0)
            # 验证文件大小
            if size_bytes > MAX_FILE_SIZE:
                results.append({
                    "error": f"文件 {file.filename} 大小超过限制",
                    "filename": file.filename
                })
                continue
            
            # 验证文件类型
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                results.append({
                    "error": f"文件 {file.filename} 格式不支持",
                    "filename": file.filename
                })
                continue
            
            # 生成唯一文件名
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # 创建上传目录
            date_dir = datetime.now().strftime("%Y/%m/%d")
            upload_dir = os.path.join("uploads", "images", date_dir)
            os.makedirs(upload_dir, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(upload_dir, unique_filename)
            
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
            
            # 生成访问URL（使用完整URL）
            base_url = os.getenv("BASE_URL", "http://localhost:8000")
            file_url = f"{base_url}/uploads/images/{date_dir}/{unique_filename}"
            
            results.append(UploadResponse(
                filename=unique_filename,
                url=file_url,
                size=size_bytes,
                content_type=file.content_type
            ))
            
        except Exception as e:
            results.append({
                "error": f"文件 {file.filename} 上传失败: {str(e)}",
                "filename": file.filename
            })
    
    return results


@router.delete("/{filename}")
async def delete_file(filename: str):
    """删除上传的文件"""
    
    try:
        # 查找文件
        upload_dir = "uploads/images"
        for root, dirs, files in os.walk(upload_dir):
            if filename in files:
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                return {"message": "文件删除成功"}
        
        raise HTTPException(status_code=404, detail="文件不存在")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")


@router.get("/info")
async def get_upload_info():
    """获取上传信息"""
    return {
        "max_file_size": MAX_FILE_SIZE,
        "allowed_extensions": list(ALLOWED_EXTENSIONS),
        "max_files": 5
    }
