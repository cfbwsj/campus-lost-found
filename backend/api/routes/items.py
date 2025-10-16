"""
ʧ�����API·��
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db, LostItem as DBLostItem, FoundItem as DBFoundItem
from models.schemas import LostItem, FoundItem, ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.post("/lost", response_model=LostItem)
async def create_lost_item(item: ItemCreate, db: Session = Depends(get_db)):
    """����ʧ����Ϣ"""
    db_item = DBLostItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.post("/found", response_model=FoundItem)
async def create_found_item(item: ItemCreate, db: Session = Depends(get_db)):
    """����������Ϣ"""
    db_item = DBFoundItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/lost", response_model=List[ItemResponse])
async def get_lost_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """��ȡʧ���б�"""
    query = db.query(DBLostItem).filter(DBLostItem.is_active == True)
    
    if category:
        query = query.filter(DBLostItem.category == category)
    if status:
        query = query.filter(DBLostItem.status == status)
    
    items = query.offset(skip).limit(limit).all()
    return items


@router.get("/found", response_model=List[ItemResponse])
async def get_found_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """��ȡ�����б�"""
    query = db.query(DBFoundItem).filter(DBFoundItem.is_active == True)
    
    if category:
        query = query.filter(DBFoundItem.category == category)
    if status:
        query = query.filter(DBFoundItem.status == status)
    
    items = query.offset(skip).limit(limit).all()
    return items


@router.get("/lost/{item_id}", response_model=ItemResponse)
async def get_lost_item(item_id: int, db: Session = Depends(get_db)):
    """��ȡʧ������"""
    item = db.query(DBLostItem).filter(
        DBLostItem.id == item_id,
        DBLostItem.is_active == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="ʧ����Ϣ������")
    
    return item


@router.get("/found/{item_id}", response_model=ItemResponse)
async def get_found_item(item_id: int, db: Session = Depends(get_db)):
    """��ȡ��������"""
    item = db.query(DBFoundItem).filter(
        DBFoundItem.id == item_id,
        DBFoundItem.is_active == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="������Ϣ������")
    
    return item


@router.put("/lost/{item_id}", response_model=LostItem)
async def update_lost_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db)
):
    """����ʧ����Ϣ"""
    db_item = db.query(DBLostItem).filter(DBLostItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="ʧ����Ϣ������")
    
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
    db: Session = Depends(get_db)
):
    """����������Ϣ"""
    db_item = db.query(DBFoundItem).filter(DBFoundItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="������Ϣ������")
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/lost/{item_id}")
async def delete_lost_item(item_id: int, db: Session = Depends(get_db)):
    """ɾ��ʧ����Ϣ"""
    db_item = db.query(DBLostItem).filter(DBLostItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="ʧ����Ϣ������")
    
    db_item.is_active = False
    db.commit()
    return {"message": "ʧ����Ϣ��ɾ��"}


@router.delete("/found/{item_id}")
async def delete_found_item(item_id: int, db: Session = Depends(get_db)):
    """ɾ��������Ϣ"""
    db_item = db.query(DBFoundItem).filter(DBFoundItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="������Ϣ������")
    
    db_item.is_active = False
    db.commit()
    return {"message": "������Ϣ��ɾ��"}


@router.get("/categories")
async def get_categories():
    """��ȡ��Ʒ�����б�"""
    categories = [
        "�ֻ�/�����Ʒ",
        "Ǯ��/֤��",
        "Կ��/�ſ�",
        "�鼮/�ľ�",
        "����/��Ʒ",
        "�۾�/����",
        "�˶���Ʒ",
        "����"
    ]
    return {"categories": categories}
