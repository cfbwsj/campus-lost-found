"""
��������API·��
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
    q: str = Query(..., description="�����ؼ���"),
    category: Optional[str] = Query(None, description="��Ʒ���"),
    location: Optional[str] = Query(None, description="�ص�"),
    item_type: str = Query("all", description="��Ʒ���ͣ�lost/found/all"),
    limit: int = Query(20, ge=1, le=100, description="ÿҳ����"),
    offset: int = Query(0, ge=0, description="ƫ����"),
    db: Session = Depends(get_db)
):
    """�ۺ�����ʧ���������Ϣ"""
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="�����ؼ��ʲ���Ϊ��")
    
    try:
        filters = {}
        if category:
            filters['category'] = category
        if location:
            filters['location'] = location
        
        all_results = []
        total_count = 0
        
        # ����ʧ��
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
        
        # ��������
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
        
        # ��ʱ������
        all_results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # ��ҳ
        page = offset // limit + 1
        paginated_results = all_results[:limit]
        
        return SearchResponse(
            items=paginated_results,
            total=total_count,
            page=page,
            size=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"����ʧ��: {str(e)}")


@router.get("/lost", response_model=SearchResponse)
async def search_lost_items(
    q: str = Query(..., description="�����ؼ���"),
    category: Optional[str] = Query(None, description="��Ʒ���"),
    location: Optional[str] = Query(None, description="�ص�"),
    limit: int = Query(20, ge=1, le=100, description="ÿҳ����"),
    offset: int = Query(0, ge=0, description="ƫ����")
):
    """����ʧ����Ϣ"""
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="�����ؼ��ʲ���Ϊ��")
    
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
        raise HTTPException(status_code=500, detail=f"����ʧ��ʧ��: {str(e)}")


@router.get("/found", response_model=SearchResponse)
async def search_found_items(
    q: str = Query(..., description="�����ؼ���"),
    category: Optional[str] = Query(None, description="��Ʒ���"),
    location: Optional[str] = Query(None, description="�ص�"),
    limit: int = Query(20, ge=1, le=100, description="ÿҳ����"),
    offset: int = Query(0, ge=0, description="ƫ����")
):
    """����������Ϣ"""
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="�����ؼ��ʲ���Ϊ��")
    
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
        raise HTTPException(status_code=500, detail=f"��������ʧ��: {str(e)}")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="����ǰ׺"),
    field: str = Query("title", description="�����ֶ�")
):
    """��ȡ��������"""
    
    if not q.strip():
        return {"suggestions": []}
    
    try:
        suggestions = es_client.get_suggestions(q, field)
        return {"suggestions": suggestions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"��ȡ��������ʧ��: {str(e)}")


@router.get("/hot-keywords")
async def get_hot_keywords():
    """��ȡ���������ؼ���"""
    
    # ģ�����Źؼ�������
    hot_keywords = [
        "�ֻ�", "Ǯ��", "Կ��", "���֤", "ѧ����",
        "�۾�", "���", "ˮ��", "�����", "����"
    ]
    
    return {"keywords": hot_keywords}


@router.get("/categories")
async def get_search_categories():
    """��ȡ��������"""
    
    categories = [
        {"key": "�ֻ�/�����Ʒ", "count": 156},
        {"key": "Ǯ��/֤��", "count": 89},
        {"key": "Կ��/�ſ�", "count": 67},
        {"key": "�鼮/�ľ�", "count": 234},
        {"key": "����/��Ʒ", "count": 45},
        {"key": "�۾�/����", "count": 23},
        {"key": "�˶���Ʒ", "count": 34},
        {"key": "����", "count": 78}
    ]
    
    return {"categories": categories}


@router.get("/locations")
async def get_search_locations():
    """��ȡ���������ص�"""
    
    locations = [
        {"key": "ͼ���", "count": 45},
        {"key": "ʳ��", "count": 32},
        {"key": "��ѧ¥", "count": 28},
        {"key": "����¥", "count": 23},
        {"key": "�ٳ�", "count": 19},
        {"key": "ʵ����", "count": 15},
        {"key": "����¥", "count": 12},
        {"key": "У�ſ�", "count": 8}
    ]
    
    return {"locations": locations}
