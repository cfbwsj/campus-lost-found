"""
AI��Ʒ���๤��
ʹ��Ԥѵ��ģ�ͽ�����Ʒʶ��ͷ���
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
    """��Ʒ������"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.categories = {
            "phone": "�ֻ�/�����Ʒ",
            "wallet": "Ǯ��/֤��",
            "keys": "Կ��/�ſ�",
            "book": "�鼮/�ľ�",
            "clothes": "����/��Ʒ",
            "glasses": "�۾�/����",
            "sports": "�˶���Ʒ",
            "other": "����"
        }
        self._load_model()
    
    def _load_model(self):
        """����Ԥѵ��ģ��"""
        try:
            # ʹ��ResNet��Ϊ����ģ��
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
            self.model.eval()
            self.model.to(self.device)
            
            # ͼ��Ԥ����
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            logger.info("AI����ģ�ͼ��سɹ�")
            
        except Exception as e:
            logger.error(f"ģ�ͼ���ʧ��: {str(e)}")
            self.model = None
    
    def classify_image(self, image_path: str) -> Tuple[str, float, List[str]]:
        """
        ��ͼƬ������Ʒ����
        
        Args:
            image_path: ͼƬ·��
            
        Returns:
            (��Ҫ���, ���Ŷ�, ���п��ܵ����)
        """
        if not self.model:
            return "other", 0.0, ["����"]
        
        try:
            # ���غ�Ԥ����ͼƬ
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # ����
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # ��ȡԤ����
            top5_prob, top5_indices = torch.topk(probabilities, 5)
            
            # ��ImageNet���ӳ�䵽���ǵ����
            predicted_category = self._map_imagenet_to_category(top5_indices[0].item())
            confidence = top5_prob[0].item()
            
            # ��ȡ���п��ܵ����
            all_categories = []
            for idx, prob in zip(top5_indices, top5_prob):
                category = self._map_imagenet_to_category(idx.item())
                all_categories.append(f"{category} ({prob.item():.2f})")
            
            return predicted_category, confidence, all_categories
            
        except Exception as e:
            logger.error(f"ͼƬ����ʧ��: {str(e)}")
            return "other", 0.0, ["����"]
    
    def classify_image_from_url(self, image_url: str) -> Tuple[str, float, List[str]]:
        """
        ��URLͼƬ������Ʒ����
        
        Args:
            image_url: ͼƬURL
            
        Returns:
            (��Ҫ���, ���Ŷ�, ���п��ܵ����)
        """
        if not self.model:
            return "other", 0.0, ["����"]
        
        try:
            # ����ͼƬ
            response = requests.get(image_url)
            response.raise_for_status()
            
            # ת��ΪPIL Image
            image = Image.open(BytesIO(response.content)).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # ����
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # ��ȡԤ����
            top5_prob, top5_indices = torch.topk(probabilities, 5)
            
            # ӳ�����
            predicted_category = self._map_imagenet_to_category(top5_indices[0].item())
            confidence = top5_prob[0].item()
            
            # ��ȡ���п��ܵ����
            all_categories = []
            for idx, prob in zip(top5_indices, top5_prob):
                category = self._map_imagenet_to_category(idx.item())
                all_categories.append(f"{category} ({prob.item():.2f})")
            
            return predicted_category, confidence, all_categories
            
        except Exception as e:
            logger.error(f"��URL����ͼƬʧ��: {str(e)}")
            return "other", 0.0, ["����"]
    
    def _map_imagenet_to_category(self, imagenet_class_id: int) -> str:
        """
        ��ImageNet���IDӳ�䵽���ǵ���Ʒ���
        
        Args:
            imagenet_class_id: ImageNet���ID
            
        Returns:
            ӳ�����������
        """
        # ImageNet���ӳ����򣨼򻯰棩
        mapping_rules = {
            # �ֻ�/�����Ʒ
            range(0, 100): "phone",      # ���ֵ����豸
            range(400, 500): "phone",    # ������豸
            range(700, 800): "phone",    # �����豸
            
            # Ǯ��/֤��
            range(200, 250): "wallet",   # Ǯ�����
            
            # Կ��/�ſ�
            range(800, 850): "keys",     # ������
            
            # �鼮/�ľ�
            range(600, 650): "book",     # �鼮�ľ�
            
            # ����/��Ʒ
            range(100, 200): "clothes",  # ��װ����
            range(300, 350): "clothes",  # ��װ
            
            # �۾�/����
            range(350, 400): "glasses",  # �۾�����
            
            # �˶���Ʒ
            range(500, 600): "sports",   # �˶�����
            
            # ����
        }
        
        for class_range, category in mapping_rules.items():
            if imagenet_class_id in class_range:
                return self.categories.get(category, "����")
        
        return "����"
    
    def get_category_name(self, category_key: str) -> str:
        """��ȡ�����������"""
        return self.categories.get(category_key, "����")
    
    def get_all_categories(self) -> Dict[str, str]:
        """��ȡ�������"""
        return self.categories.copy()


# ȫ�ַ�����ʵ��
item_classifier = ItemClassifier()
