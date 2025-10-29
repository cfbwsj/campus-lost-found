#!/bin/bash
# Render启动脚本

echo "正在预加载AI模型..."
python download_models.py

echo "启动FastAPI服务..."
uvicorn main:app --host 0.0.0.0 --port $PORT

