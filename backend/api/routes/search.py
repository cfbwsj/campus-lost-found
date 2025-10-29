"""
搜索功能API路由
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from models.database import get_db, LostItem as DBLostItem, FoundItem as DBFoundItem
from models.schemas import SearchRequest, SearchResponse, ItemResponse
from utils.elasticsearch_client import es_client

router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def search_items(
    q: str = Query(..., description="搜索关键词"),
    category: Optional[str] = Query(None, description="物品类别"),
    location: Optional[str] = Query(None, description="地点"),
    item_type: str = Query("all", description="物品类型：lost/found/all"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    """综合搜索失物和招领信息"""
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    try:
        filters = {}
        if category:
            filters['category'] = category
        if location:
            filters['location'] = location
        
        all_results = []
        total_count = 0
        
        # 如果ES不可用，使用SQL搜索
        if not es_client.client:
            # 使用数据库直接搜索作为降级方案
            query = db.query(DBLostItem if item_type == "lost" else DBFoundItem if item_type == "found" else DBLostItem)
            query = query.filter(
                (DBLostItem.title.contains(q)) | 
                (DBLostItem.description.contains(q))
            )
            if category:
                query = query.filter(DBLostItem.category == category)
            if location:
                query = query.filter(DBLostItem.location.contains(location))
            
            total_count = query.count()
            results = query.offset(offset).limit(limit).all()
            
            for item in results:
                item_dict = {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "category": item.category,
                    "location": item.location,
                    "image_url": item.image_url,
                    "status": item.status,
                    "created_at": item.created_at.isoformat() if item.created_at else "",
                    "item_type": item_type
                }
                all_results.append(item_dict)
        else:
            # 搜索失物
            if item_type in ["lost", "all"]:
                lost_results = es_client.search_lost_items(
                    query=q,
                    filters=filters,
                    size=limit,
                    from_=offset
                )
                for item in lost_results["hits"]:
                    item["item_type"] = "lost"
                    all_results.append(item)
                total_count += lost_results["total"]
            
            # 搜索招领
            if item_type in ["found", "all"]:
                found_results = es_client.search_found_items(
                    query=q,
                    filters=filters,
                    size=limit,
                    from_=offset
                )
                for item in found_results["hits"]:
                    item["item_type"] = "found"
                    all_results.append(item)
                total_count += found_results["total"]
        
        # 按时间排序
        all_results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        page = offset // limit + 1
        paginated_results = all_results[:limit]
        
        return SearchResponse(
            items=paginated_results,
            total=total_count,
            page=page,
            size=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.get("/lost", response_model=SearchResponse)
async def search_lost_items(
    q: str = Query(..., description="搜索关键词"),
    category: Optional[str] = Query(None, description="物品类别"),
    location: Optional[str] = Query(None, description="地点"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量")
):
    """搜索失物信息"""
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    try:
        filters = {}
        if category:
            filters['category'] = category
        if location:
            filters['location'] = location
        
        results = es_client.search_lost_items(
            query=q,
            filters=filters,
            size=limit,
            from_=offset
        )
        
        page = offset // limit + 1
        
        return SearchResponse(
            items=results["hits"],
            total=results["total"],
            page=page,
            size=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失物失败: {str(e)}")


@router.get("/found", response_model=SearchResponse)
async def search_found_items(
    q: str = Query(..., description="搜索关键词"),
    category: Optional[str] = Query(None, description="物品类别"),
    location: Optional[str] = Query(None, description="地点"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量")
):
    """搜索招领信息"""
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    try:
        filters = {}
        if category:
            filters['category'] = category
        if location:
            filters['location'] = location
        
        results = es_client.search_found_items(
            query=q,
            filters=filters,
            size=limit,
            from_=offset
        )
        
        page = offset // limit + 1
        
        return SearchResponse(
            items=results["hits"],
            total=results["total"],
            page=page,
            size=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索招领失败: {str(e)}")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="搜索前缀"),
    field: str = Query("title", description="建议字段")
):
    """获取搜索建议"""
    
    if not q.strip():
        return {"suggestions": []}
    
    try:
        suggestions = es_client.get_suggestions(q, field)
        return {"suggestions": suggestions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取搜索建议失败: {str(e)}")


@router.get("/hot-keywords")
async def get_hot_keywords():
    """获取热门搜索关键词"""
    
    # 模拟热门关键词数据
    hot_keywords = [
        "手机", "钱包", "钥匙", "身份证", "学生卡",
        "眼镜", "书包", "水杯", "充电器", "耳机"
    ]
    
    return {"keywords": hot_keywords}


@router.get("/categories")
async def get_search_categories():
    """获取搜索分类"""
    
    categories = [
        {"key": "手机/数码产品", "count": 156},
        {"key": "钱包/证件", "count": 89},
        {"key": "钥匙/门卡", "count": 67},
        {"key": "书籍/文具", "count": 234},
        {"key": "衣物/饰品", "count": 45},
        {"key": "眼镜/配饰", "count": 23},
        {"key": "运动用品", "count": 34},
        {"key": "其他", "count": 78}
    ]
    
    return {"categories": categories}


@router.get("/locations")
async def get_search_locations():
    """获取热门搜索地点"""
    
    locations = [
        {"key": "图书馆", "count": 45},
        {"key": "食堂", "count": 32},
        {"key": "教学楼", "count": 28},
        {"key": "宿舍楼", "count": 23},
        {"key": "操场", "count": 19},
        {"key": "实验室", "count": 15},
        {"key": "行政楼", "count": 12},
        {"key": "校门口", "count": 8}
    ]
    
    return {"locations": locations}
