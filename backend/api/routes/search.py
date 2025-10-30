"""
搜索功能API路由
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from models.database import get_db, LostItem as DBLostItem, FoundItem as DBFoundItem
from models.schemas import SearchRequest, SearchResponse, SearchItem
from utils.elasticsearch_client import es_client

router = APIRouter(redirect_slashes=False)


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
        
        # 如果ES不可用，使用SQL搜索（合并失物与招领）
        if not es_client.client:
            def build_filters(model_query, Model):
                conditions = []
                # 文本匹配（不区分大小写）
                conditions.append((Model.title.ilike(f"%{q}%")) | (Model.description.ilike(f"%{q}%")))
                if category:
                    conditions.append(Model.category == category)
                if location:
                    conditions.append(Model.location.ilike(f"%{location}%"))
                return model_query.filter(*conditions, Model.is_active == True)

            if item_type in ["lost", "all"]:
                lost_query = build_filters(db.query(DBLostItem), DBLostItem)
                lost_items = lost_query.all()
                for item in lost_items:
                    all_results.append({
                        "id": item.id,
                        "title": item.title,
                        "description": item.description,
                        "category": item.category,
                        "location": item.location,
                        "contact_info": item.contact_info,
                        "image_url": item.image_url,
                        "ocr_text": item.ocr_text,
                        "ai_category": item.ai_category,
                        "confidence": item.confidence,
                        "status": item.status,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                        "item_type": "lost"
                    })

            if item_type in ["found", "all"]:
                found_query = build_filters(db.query(DBFoundItem), DBFoundItem)
                found_items = found_query.all()
                for item in found_items:
                    all_results.append({
                        "id": item.id,
                        "title": item.title,
                        "description": item.description,
                        "category": item.category,
                        "location": item.location,
                        "contact_info": item.contact_info,
                        "image_url": item.image_url,
                        "ocr_text": item.ocr_text,
                        "ai_category": item.ai_category,
                        "confidence": item.confidence,
                        "status": item.status,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                        "item_type": "found"
                    })

            # 排序与分页
            all_results.sort(key=lambda x: x.get("created_at") or 0, reverse=True)
            total_count = len(all_results)
            paginated_results = all_results[offset: offset + limit]
            # 转换 created_at 为 isoformat 字符串
            for r in paginated_results:
                if r["created_at"]:
                    r["created_at"] = r["created_at"].isoformat()
            page = offset // limit + 1
            return SearchResponse(items=paginated_results, total=total_count, page=page, size=limit)
        else:
            try:
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
                # 如果ES无结果，回退到SQL以确保本地也能搜到
                if total_count == 0:
                    raise RuntimeError("Empty results from ES, fallback to SQL")
            except Exception:
                # ES 查询失败时回退到 SQL
                def build_filters(model_query, Model):
                    conditions = []
                    conditions.append((Model.title.ilike(f"%{q}%")) | (Model.description.ilike(f"%{q}%")))
                    if category:
                        conditions.append(Model.category == category)
                    if location:
                        conditions.append(Model.location.ilike(f"%{location}%"))
                    return model_query.filter(*conditions, Model.is_active == True)

                if item_type in ["lost", "all"]:
                    for it in build_filters(db.query(DBLostItem), DBLostItem).all():
                        all_results.append({
                            "id": it.id,
                            "title": it.title,
                            "description": it.description,
                            "category": it.category,
                            "location": it.location,
                            "image_url": it.image_url,
                            "status": it.status,
                            "created_at": it.created_at or None,
                            "item_type": "lost"
                        })
                if item_type in ["found", "all"]:
                    for it in build_filters(db.query(DBFoundItem), DBFoundItem).all():
                        all_results.append({
                            "id": it.id,
                            "title": it.title,
                            "description": it.description,
                            "category": it.category,
                            "location": it.location,
                            "image_url": it.image_url,
                            "status": it.status,
                            "created_at": it.created_at or None,
                            "item_type": "found"
                        })
        
        # 按时间排序（容错：created_at 可能为 None 或 datetime）
        def _sort_key(x):
            v = x.get("created_at")
            try:
                return v.timestamp() if hasattr(v, "timestamp") else 0
            except Exception:
                return 0
        all_results.sort(key=_sort_key, reverse=True)
        
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


# 兼容无斜杠路径，避免 404/307
@router.get("", response_model=SearchResponse)
async def search_items_no_slash(
    q: str = Query(..., description="搜索关键词"),
    category: Optional[str] = Query(None, description="物品类别"),
    location: Optional[str] = Query(None, description="地点"),
    item_type: str = Query("all", description="物品类型：lost/found/all"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    return await search_items(q=q, category=category, location=location, item_type=item_type, limit=limit, offset=offset, db=db)


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
        if not es_client.client:
            query = db.query(DBLostItem).filter(
                (DBLostItem.title.ilike(f"%{q}%")) | (DBLostItem.description.ilike(f"%{q}%")),
                DBLostItem.is_active == True
            )
            if category:
                query = query.filter(DBLostItem.category == category)
            if location:
                query = query.filter(DBLostItem.location.ilike(f"%{location}%"))
            total = query.count()
            items = query.order_by(DBLostItem.created_at.desc()).offset(offset).limit(limit).all()
            page = offset // limit + 1
            mapped = [{
                "id": it.id,
                "title": it.title,
                "description": it.description,
                "category": it.category,
                "location": it.location,
                "contact_info": it.contact_info,
                "image_url": it.image_url,
                "ocr_text": it.ocr_text,
                "ai_category": it.ai_category,
                "confidence": it.confidence,
                "status": it.status,
                "created_at": it.created_at,
                "updated_at": it.updated_at,
                "item_type": "lost"
            } for it in items]
            return SearchResponse(items=mapped, total=total, page=page, size=limit)
        else:
            try:
                filters = {}
                if category:
                    filters['category'] = category
                if location:
                    filters['location'] = location
                results = es_client.search_lost_items(query=q, filters=filters, size=limit, from_=offset)
                page = offset // limit + 1
                if results["total"] == 0:
                    raise RuntimeError("Empty ES result, fallback to SQL")
                return SearchResponse(items=results["hits"], total=results["total"], page=page, size=limit)
            except Exception:
                # 回退到 SQL
                query = db.query(DBLostItem).filter(
                    (DBLostItem.title.ilike(f"%{q}%")) | (DBLostItem.description.ilike(f"%{q}%")),
                    DBLostItem.is_active == True
                )
                if category:
                    query = query.filter(DBLostItem.category == category)
                if location:
                    query = query.filter(DBLostItem.location.ilike(f"%{location}%"))
                total = query.count()
                items = query.order_by(DBLostItem.created_at.desc()).offset(offset).limit(limit).all()
                page = offset // limit + 1
                mapped = [{
                    "id": it.id,
                    "title": it.title,
                    "description": it.description,
                    "category": it.category,
                    "location": it.location,
                    "image_url": it.image_url,
                    "status": it.status,
                    "created_at": it.created_at.isoformat() if it.created_at else "",
                    "item_type": "lost"
                } for it in items]
                return SearchResponse(items=mapped, total=total, page=page, size=limit)
        
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
        if not es_client.client:
            query = db.query(DBFoundItem).filter(
                (DBFoundItem.title.ilike(f"%{q}%")) | (DBFoundItem.description.ilike(f"%{q}%")),
                DBFoundItem.is_active == True
            )
            if category:
                query = query.filter(DBFoundItem.category == category)
            if location:
                query = query.filter(DBFoundItem.location.ilike(f"%{location}%"))
            total = query.count()
            items = query.order_by(DBFoundItem.created_at.desc()).offset(offset).limit(limit).all()
            page = offset // limit + 1
            mapped = [{
                "id": it.id,
                "title": it.title,
                "description": it.description,
                "category": it.category,
                "location": it.location,
                "contact_info": it.contact_info,
                "image_url": it.image_url,
                "ocr_text": it.ocr_text,
                "ai_category": it.ai_category,
                "confidence": it.confidence,
                "status": it.status,
                "created_at": it.created_at,
                "updated_at": it.updated_at,
                "item_type": "found"
            } for it in items]
            return SearchResponse(items=mapped, total=total, page=page, size=limit)
        else:
            try:
                filters = {}
                if category:
                    filters['category'] = category
                if location:
                    filters['location'] = location
                results = es_client.search_found_items(query=q, filters=filters, size=limit, from_=offset)
                page = offset // limit + 1
                if results["total"] == 0:
                    raise RuntimeError("Empty ES result, fallback to SQL")
                return SearchResponse(items=results["hits"], total=results["total"], page=page, size=limit)
            except Exception:
                # 回退到 SQL
                query = db.query(DBFoundItem).filter(
                    (DBFoundItem.title.ilike(f"%{q}%")) | (DBFoundItem.description.ilike(f"%{q}%")),
                    DBFoundItem.is_active == True
                )
                if category:
                    query = query.filter(DBFoundItem.category == category)
                if location:
                    query = query.filter(DBFoundItem.location.ilike(f"%{location}%"))
                total = query.count()
                items = query.order_by(DBFoundItem.created_at.desc()).offset(offset).limit(limit).all()
                page = offset // limit + 1
                mapped = [{
                    "id": it.id,
                    "title": it.title,
                    "description": it.description,
                    "category": it.category,
                    "location": it.location,
                    "image_url": it.image_url,
                    "status": it.status,
                    "created_at": it.created_at.isoformat() if it.created_at else "",
                    "item_type": "found"
                } for it in items]
                return SearchResponse(items=mapped, total=total, page=page, size=limit)
        
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
async def get_hot_keywords(db: Session = Depends(get_db)):
    """从最近发布的标题中动态提取简单关键词（去除长度<2的片段）"""
    titles = [t[0] for t in db.query(DBLostItem.title).order_by(DBLostItem.created_at.desc()).limit(100).all()]
    titles += [t[0] for t in db.query(DBFoundItem.title).order_by(DBFoundItem.created_at.desc()).limit(100).all()]
    freq = {}
    for title in titles:
        if not title:
            continue
        for token in list(title.replace('\n', ' ').replace('\t', ' ').split()):
            tok = token.strip()
            if len(tok) < 2:
                continue
            freq[tok] = freq.get(tok, 0) + 1
    # 取 Top 10
    keywords = [k for k, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]]
    return {"keywords": keywords}


@router.get("/categories")
async def get_search_categories(db: Session = Depends(get_db)):
    """动态统计分类计数（合并失物与招领）"""
    lost_counts = db.query(DBLostItem.category, func.count(DBLostItem.id)).filter(DBLostItem.is_active == True).group_by(DBLostItem.category).all()
    found_counts = db.query(DBFoundItem.category, func.count(DBFoundItem.id)).filter(DBFoundItem.is_active == True).group_by(DBFoundItem.category).all()
    agg = {}
    for cat, cnt in lost_counts:
        if not cat:
            continue
        agg[cat] = agg.get(cat, 0) + cnt
    for cat, cnt in found_counts:
        if not cat:
            continue
        agg[cat] = agg.get(cat, 0) + cnt
    categories = [{"key": k, "count": v} for k, v in sorted(agg.items(), key=lambda x: x[1], reverse=True)]
    return {"categories": categories}


@router.get("/locations")
async def get_search_locations(db: Session = Depends(get_db)):
    """动态统计地点计数（合并失物与招领）"""
    lost_counts = db.query(DBLostItem.location, func.count(DBLostItem.id)).filter(DBLostItem.is_active == True, DBLostItem.location.isnot(None), DBLostItem.location != "").group_by(DBLostItem.location).all()
    found_counts = db.query(DBFoundItem.location, func.count(DBFoundItem.id)).filter(DBFoundItem.is_active == True, DBFoundItem.location.isnot(None), DBFoundItem.location != "").group_by(DBFoundItem.location).all()
    agg = {}
    for loc, cnt in lost_counts:
        agg[loc] = agg.get(loc, 0) + cnt
    for loc, cnt in found_counts:
        agg[loc] = agg.get(loc, 0) + cnt
    locations = [{"key": k, "count": v} for k, v in sorted(agg.items(), key=lambda x: x[1], reverse=True)]
    return {"locations": locations}
