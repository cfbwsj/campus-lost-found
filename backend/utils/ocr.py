"""
OCR文字识别工具
使用Tesseract进行图片文字识别
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class OCRProcessor:
    """OCR处理器"""
    
    def __init__(self):
        # 设置Tesseract路径（Windows需要指定路径）
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """图像预处理，提高OCR识别准确率"""
        # 读取图像
        image = cv2.imread(image_path)
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 降噪
        denoised = cv2.medianBlur(gray, 3)
        
        # 二值化
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 形态学操作，去除噪点
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text(self, image_path: str, language: str = "chi_sim+eng") -> Tuple[str, float]:
        """
        从图片中提取文字
        
        Args:
            image_path: 图片路径
            language: 语言设置，默认中英文
            
        Returns:
            (识别的文字, 置信度)
        """
        try:
            # 预处理图像
            processed_image = self.preprocess_image(image_path)
            
            # OCR识别
            # 获取详细信息，包括置信度
            data = pytesseract.image_to_data(
                processed_image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # 提取文字
            text = pytesseract.image_to_string(processed_image, lang=language)
            
            # 计算平均置信度
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # 清理文字
            cleaned_text = self._clean_text(text)
            
            logger.info(f"OCR识别完成: {len(cleaned_text)}个字符, 置信度: {avg_confidence:.2f}")
            
            return cleaned_text, avg_confidence
            
        except Exception as e:
            logger.error(f"OCR识别失败: {str(e)}")
            return "", 0.0
    
    def _clean_text(self, text: str) -> str:
        """清理识别的文字"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        # 移除特殊字符（可选）
        # cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', cleaned_text)
        
        return cleaned_text
    
    def extract_text_from_url(self, image_url: str, language: str = "chi_sim+eng") -> Tuple[str, float]:
        """
        从URL图片中提取文字
        
        Args:
            image_url: 图片URL
            language: 语言设置
            
        Returns:
            (识别的文字, 置信度)
        """
        import requests
        from io import BytesIO
        
        try:
            # 下载图片
            response = requests.get(image_url)
            response.raise_for_status()
            
            # 转换为PIL Image
            image = Image.open(BytesIO(response.content))
            
            # 转换为OpenCV格式
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # 预处理
            processed_image = self._preprocess_cv_image(cv_image)
            
            # OCR识别
            data = pytesseract.image_to_data(
                processed_image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # 提取文字
            text = pytesseract.image_to_string(processed_image, lang=language)
            
            # 计算置信度
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            cleaned_text = self._clean_text(text)
            
            return cleaned_text, avg_confidence
            
        except Exception as e:
            logger.error(f"从URL识别OCR失败: {str(e)}")
            return "", 0.0
    
    def _preprocess_cv_image(self, image: np.ndarray) -> np.ndarray:
        """预处理OpenCV图像"""
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 降噪
        denoised = cv2.medianBlur(gray, 3)
        
        # 二值化
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary


# 全局OCR处理器实例
ocr_processor = OCRProcessor()
