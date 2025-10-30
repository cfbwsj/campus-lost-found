"""
失物管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db, LostItem as DBLostItem, FoundItem as DBFoundItem
from models.schemas import LostItem, FoundItem, ItemCreate, ItemUpdate, ItemResponse
from api.routes.auth import get_current_user, require_admin
from models.database import User

router = APIRouter()


@router.post("/lost", response_model=LostItem)
async def create_lost_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """发布失物信息"""
    data = item.dict()
    db_item = DBLostItem(**data)
    db_item.owner_id = current_user.id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.post("/found", response_model=FoundItem)
async def create_found_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """发布招领信息"""
    data = item.dict()
    db_item = DBFoundItem(**data)
    db_item.owner_id = current_user.id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/lost")
async def get_lost_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取失物列表"""
    query = db.query(DBLostItem).filter(DBLostItem.is_active == True)
    
    if category:
        query = query.filter(DBLostItem.category == category)
    if status:
        query = query.filter(DBLostItem.status == status)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/found")
async def get_found_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取招领列表"""
    query = db.query(DBFoundItem).filter(DBFoundItem.is_active == True)
    
    if category:
        query = query.filter(DBFoundItem.category == category)
    if status:
        query = query.filter(DBFoundItem.status == status)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/lost/{item_id}", response_model=ItemResponse)
async def get_lost_item(item_id: int, db: Session = Depends(get_db)):
    """获取失物详情"""
    item = db.query(DBLostItem).filter(
        DBLostItem.id == item_id,
        DBLostItem.is_active == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="失物信息不存在")
    
    return item


@router.get("/found/{item_id}", response_model=ItemResponse)
async def get_found_item(item_id: int, db: Session = Depends(get_db)):
    """获取招领详情"""
    item = db.query(DBFoundItem).filter(
        DBFoundItem.id == item_id,
        DBFoundItem.is_active == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="招领信息不存在")
    
    return item


@router.get("/my")
async def get_my_items(
    item_type: str = Query("all", description="lost/found/all"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户发布的物品列表"""
    results = []
    total = 0
    if item_type in ["lost", "all"]:
        q = db.query(DBLostItem).filter(DBLostItem.is_active == True, DBLostItem.owner_id == current_user.id)
        total += q.count()
        results += q.order_by(DBLostItem.created_at.desc()).offset(skip).limit(limit).all()
    if item_type in ["found", "all"]:
        q = db.query(DBFoundItem).filter(DBFoundItem.is_active == True, DBFoundItem.owner_id == current_user.id)
        total += q.count()
        results += q.order_by(DBFoundItem.created_at.desc()).offset(skip).limit(limit).all()
    # 统一返回
    items = []
    for it in results:
        items.append(it)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.put("/lost/{item_id}", response_model=LostItem)
async def update_lost_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新失物信息"""
    db_item = db.query(DBLostItem).filter(DBLostItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="失物信息不存在")
    # 权限：管理员或本人
    if current_user.role != "admin" and db_item.owner_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="无权限修改该信息")

    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/found/{item_id}", response_model=FoundItem)
async def update_found_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新招领信息"""
    db_item = db.query(DBFoundItem).filter(DBFoundItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="招领信息不存在")
    # 权限：管理员或本人
    if current_user.role != "admin" and db_item.owner_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="无权限修改该信息")
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/lost/{item_id}")
async def delete_lost_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """删除失物信息"""
    db_item = db.query(DBLostItem).filter(DBLostItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="失物信息不存在")
    # 权限：管理员或本人
    if current_user.role != "admin" and db_item.owner_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="无权限删除该信息")

    db_item.is_active = False
    db.commit()
    return {"message": "失物信息已删除"}


@router.delete("/found/{item_id}")
async def delete_found_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """删除招领信息"""
    db_item = db.query(DBFoundItem).filter(DBFoundItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="招领信息不存在")
    # 权限：管理员或本人
    if current_user.role != "admin" and db_item.owner_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="无权限删除该信息")

    db_item.is_active = False
    db.commit()
    return {"message": "招领信息已删除"}


@router.get("/categories")
async def get_categories():
    """获取物品分类列表"""
    categories = [
        "手机/数码产品",
        "钱包/证件",
        "钥匙/门卡",
        "书籍/文具",
        "衣物/饰品",
        "眼镜/配饰",
        "运动用品",
        "其他"
    ]
    return {"categories": categories}
