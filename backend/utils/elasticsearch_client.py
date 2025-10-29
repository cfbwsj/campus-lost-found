"""
ElasticSearch客户端工具
用于实现模糊搜索和语义搜索功能
"""

from elasticsearch import Elasticsearch
from typing import Dict, List, Optional, Any
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class ElasticSearchClient:
    """ElasticSearch客户端"""
    
    def __init__(self):
        # ElasticSearch连接配置
        self.es_host = os.getenv("ELASTICSEARCH_HOST", "localhost")
        self.es_port = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
        self.es_url = f"http://{self.es_host}:{self.es_port}"
        
        # 索引名称
        self.lost_items_index = "lost_items"
        self.found_items_index = "found_items"
        
        # 初始化客户端
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化ElasticSearch客户端"""
        try:
            self.client = Elasticsearch([self.es_url])
            
            # 测试连接
            if self.client.ping():
                logger.info("ElasticSearch连接成功")
                self._create_indices()
            else:
                logger.warning("ElasticSearch连接失败")
                self.client = None
                
        except Exception as e:
            logger.error(f"ElasticSearch初始化失败: {str(e)}")
            self.client = None
    
    def _create_indices(self):
        """创建索引和映射"""
        try:
            # 失物索引映射
            lost_items_mapping = {
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "description": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "category": {"type": "keyword"},
                        "location": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "contact_info": {"type": "text"},
                        "ocr_text": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "ai_category": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "is_active": {"type": "boolean"}
                    }
                }
            }
            
            # 招领索引映射
            found_items_mapping = {
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "description": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "category": {"type": "keyword"},
                        "location": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "contact_info": {"type": "text"},
                        "ocr_text": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "ai_category": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "is_active": {"type": "boolean"}
                    }
                }
            }
            
            # 创建失物索引
            if not self.client.indices.exists(index=self.lost_items_index):
                self.client.indices.create(index=self.lost_items_index, body=lost_items_mapping)
                logger.info(f"创建失物索引: {self.lost_items_index}")
            
            # 创建招领索引
            if not self.client.indices.exists(index=self.found_items_index):
                self.client.indices.create(index=self.found_items_index, body=found_items_mapping)
                logger.info(f"创建招领索引: {self.found_items_index}")
                
        except Exception as e:
            logger.error(f"创建索引失败: {str(e)}")
    
    def index_lost_item(self, item_data: Dict[str, Any]) -> bool:
        """索引失物数据"""
        if not self.client:
            return False
        
        try:
            doc_id = item_data.get('id')
            self.client.index(
                index=self.lost_items_index,
                id=doc_id,
                body=item_data
            )
            logger.info(f"失物数据已索引: ID {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"索引失物数据失败: {str(e)}")
            return False
    
    def index_found_item(self, item_data: Dict[str, Any]) -> bool:
        """索引招领数据"""
        if not self.client:
            return False
        
        try:
            doc_id = item_data.get('id')
            self.client.index(
                index=self.found_items_index,
                id=doc_id,
                body=item_data
            )
            logger.info(f"招领数据已索引: ID {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"索引招领数据失败: {str(e)}")
            return False
    
    def search_lost_items(self, query: str, filters: Optional[Dict] = None, 
                         size: int = 20, from_: int = 0) -> Dict[str, Any]:
        """搜索失物"""
        if not self.client:
            return {"hits": [], "total": 0}
        
        try:
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["title^3", "description^2", "location^2", "ocr_text"],
                                    "fuzziness": "AUTO"
                                }
                            }
                        ],
                        "filter": [
                            {"term": {"is_active": True}}
                        ]
                    }
                },
                "sort": [
                    {"created_at": {"order": "desc"}},
                    "_score"
                ],
                "size": size,
                "from": from_
            }
            
            # 添加过滤器
            if filters:
                if filters.get('category'):
                    search_body["query"]["bool"]["filter"].append({
                        "term": {"category": filters['category']}
                    })
                if filters.get('location'):
                    search_body["query"]["bool"]["must"].append({
                        "match": {"location": filters['location']}
                    })
                if filters.get('status'):
                    search_body["query"]["bool"]["filter"].append({
                        "term": {"status": filters['status']}
                    })
            
            response = self.client.search(
                index=self.lost_items_index,
                body=search_body
            )
            
            return {
                "hits": [hit["_source"] for hit in response["hits"]["hits"]],
                "total": response["hits"]["total"]["value"]
            }
            
        except Exception as e:
            logger.error(f"搜索失物失败: {str(e)}")
            return {"hits": [], "total": 0}
    
    def search_found_items(self, query: str, filters: Optional[Dict] = None,
                          size: int = 20, from_: int = 0) -> Dict[str, Any]:
        """搜索招领"""
        if not self.client:
            return {"hits": [], "total": 0}
        
        try:
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["title^3", "description^2", "location^2", "ocr_text"],
                                    "fuzziness": "AUTO"
                                }
                            }
                        ],
                        "filter": [
                            {"term": {"is_active": True}}
                        ]
                    }
                },
                "sort": [
                    {"created_at": {"order": "desc"}},
                    "_score"
                ],
                "size": size,
                "from": from_
            }
            
            # 添加过滤器
            if filters:
                if filters.get('category'):
                    search_body["query"]["bool"]["filter"].append({
                        "term": {"category": filters['category']}
                    })
                if filters.get('location'):
                    search_body["query"]["bool"]["must"].append({
                        "match": {"location": filters['location']}
                    })
                if filters.get('status'):
                    search_body["query"]["bool"]["filter"].append({
                        "term": {"status": filters['status']}
                    })
            
            response = self.client.search(
                index=self.found_items_index,
                body=search_body
            )
            
            return {
                "hits": [hit["_source"] for hit in response["hits"]["hits"]],
                "total": response["hits"]["total"]["value"]
            }
            
        except Exception as e:
            logger.error(f"搜索招领失败: {str(e)}")
            return {"hits": [], "total": 0}
    
    def delete_document(self, index: str, doc_id: str) -> bool:
        """删除文档"""
        if not self.client:
            return False
        
        try:
            self.client.delete(index=index, id=doc_id)
            logger.info(f"文档已删除: {index}/{doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除文档失败: {str(e)}")
            return False
    
    def get_suggestions(self, query: str, field: str = "title") -> List[str]:
        """获取搜索建议"""
        if not self.client:
            return []
        
        try:
            search_body = {
                "suggest": {
                    "item_suggest": {
                        "prefix": query,
                        "completion": {
                            "field": f"{field}.suggest"
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.lost_items_index,
                body=search_body
            )
            
            suggestions = []
            if "suggest" in response and "item_suggest" in response["suggest"]:
                for option in response["suggest"]["item_suggest"][0]["options"]:
                    suggestions.append(option["text"])
            
            return suggestions
            
        except Exception as e:
            logger.error(f"获取搜索建议失败: {str(e)}")
            return []


# 全局ElasticSearch客户端实例
es_client = ElasticSearchClient()
