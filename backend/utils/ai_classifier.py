"""
AI物品分类工具
使用预训练模型进行物品识别和分类
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
import requests
from io import BytesIO
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class ItemClassifier:
    """物品分类器"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.categories = {
            "phone": "手机/数码产品",
            "wallet": "钱包/证件",
            "keys": "钥匙/门卡",
            "book": "书籍/文具",
            "clothes": "衣物/饰品",
            "glasses": "眼镜/配饰",
            "sports": "运动用品",
            "other": "其他"
        }
        self._load_model()
    
    def _load_model(self):
        """加载预训练模型"""
        try:
            # 检查是否安装了torch
            import torch
            import torchvision.transforms as transforms
            
            # 使用ResNet作为基础模型
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
            self.model.eval()
            self.model.to(self.device)
            
            # 图像预处理
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            logger.info("AI分类模型加载成功")
            
        except ImportError:
            logger.warning("AI功能未启用（torch未安装），使用基础分类")
            self.model = None
        except Exception as e:
            logger.warning(f"AI模型未加载: {str(e)}")
            self.model = None
    
    def classify_image(self, image_path: str) -> Tuple[str, float, List[str]]:
        """
        对图片进行物品分类
        
        Args:
            image_path: 图片路径
            
        Returns:
            (主要类别, 置信度, 所有可能的类别)
        """
        if not self.model:
            return "other", 0.0, ["其他"]
        
        try:
            # 加载和预处理图片
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # 推理
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # 获取预测结果
            top5_prob, top5_indices = torch.topk(probabilities, 5)
            
            # 将ImageNet类别映射到我们的类别
            predicted_category = self._map_imagenet_to_category(top5_indices[0].item())
            confidence = top5_prob[0].item()
            
            # 获取所有可能的类别
            all_categories = []
            for idx, prob in zip(top5_indices, top5_prob):
                category = self._map_imagenet_to_category(idx.item())
                all_categories.append(f"{category} ({prob.item():.2f})")
            
            return predicted_category, confidence, all_categories
            
        except Exception as e:
            logger.error(f"图片分类失败: {str(e)}")
            return "other", 0.0, ["其他"]
    
    def classify_image_from_url(self, image_url: str) -> Tuple[str, float, List[str]]:
        """
        从URL图片进行物品分类
        
        Args:
            image_url: 图片URL
            
        Returns:
            (主要类别, 置信度, 所有可能的类别)
        """
        if not self.model:
            return "other", 0.0, ["其他"]
        
        try:
            # 下载图片
            response = requests.get(image_url)
            response.raise_for_status()
            
            # 转换为PIL Image
            image = Image.open(BytesIO(response.content)).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # 推理
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # 获取预测结果
            top5_prob, top5_indices = torch.topk(probabilities, 5)
            
            # 映射类别
            predicted_category = self._map_imagenet_to_category(top5_indices[0].item())
            confidence = top5_prob[0].item()
            
            # 获取所有可能的类别
            all_categories = []
            for idx, prob in zip(top5_indices, top5_prob):
                category = self._map_imagenet_to_category(idx.item())
                all_categories.append(f"{category} ({prob.item():.2f})")
            
            return predicted_category, confidence, all_categories
            
        except Exception as e:
            logger.error(f"从URL分类图片失败: {str(e)}")
            return "other", 0.0, ["其他"]
    
    def _map_imagenet_to_category(self, imagenet_class_id: int) -> str:
        """
        将ImageNet类别ID映射到我们的物品类别
        
        Args:
            imagenet_class_id: ImageNet类别ID
            
        Returns:
            映射后的类别名称
        """
        # ImageNet类别映射规则（简化版）
        mapping_rules = {
            # 手机/数码产品
            range(0, 100): "phone",      # 各种电子设备
            range(400, 500): "phone",    # 计算机设备
            range(700, 800): "phone",    # 电子设备
            
            # 钱包/证件
            range(200, 250): "wallet",   # 钱包相关
            
            # 钥匙/门卡
            range(800, 850): "keys",     # 工具类
            
            # 书籍/文具
            range(600, 650): "book",     # 书籍文具
            
            # 衣物/饰品
            range(100, 200): "clothes",  # 服装配饰
            range(300, 350): "clothes",  # 服装
            
            # 眼镜/配饰
            range(350, 400): "glasses",  # 眼镜配饰
            
            # 运动用品
            range(500, 600): "sports",   # 运动器材
            
            # 其他
        }
        
        for class_range, category in mapping_rules.items():
            if imagenet_class_id in class_range:
                return self.categories.get(category, "其他")
        
        return "其他"
    
    def get_category_name(self, category_key: str) -> str:
        """获取类别中文名称"""
        return self.categories.get(category_key, "其他")
    
    def get_all_categories(self) -> Dict[str, str]:
        """获取所有类别"""
        return self.categories.copy()


# 全局分类器实例
item_classifier = ItemClassifier()
