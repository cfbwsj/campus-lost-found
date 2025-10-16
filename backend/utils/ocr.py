"""
OCR����ʶ�𹤾�
ʹ��Tesseract����ͼƬ����ʶ��
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class OCRProcessor:
    """OCR������"""
    
    def __init__(self):
        # ����Tesseract·����Windows��Ҫָ��·����
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """ͼ��Ԥ�������OCRʶ��׼ȷ��"""
        # ��ȡͼ��
        image = cv2.imread(image_path)
        
        # ת��Ϊ�Ҷ�ͼ
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # ����
        denoised = cv2.medianBlur(gray, 3)
        
        # ��ֵ��
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # ��̬ѧ������ȥ�����
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text(self, image_path: str, language: str = "chi_sim+eng") -> Tuple[str, float]:
        """
        ��ͼƬ����ȡ����
        
        Args:
            image_path: ͼƬ·��
            language: �������ã�Ĭ����Ӣ��
            
        Returns:
            (ʶ�������, ���Ŷ�)
        """
        try:
            # Ԥ����ͼ��
            processed_image = self.preprocess_image(image_path)
            
            # OCRʶ��
            # ��ȡ��ϸ��Ϣ���������Ŷ�
            data = pytesseract.image_to_data(
                processed_image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # ��ȡ����
            text = pytesseract.image_to_string(processed_image, lang=language)
            
            # ����ƽ�����Ŷ�
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # ��������
            cleaned_text = self._clean_text(text)
            
            logger.info(f"OCRʶ�����: {len(cleaned_text)}���ַ�, ���Ŷ�: {avg_confidence:.2f}")
            
            return cleaned_text, avg_confidence
            
        except Exception as e:
            logger.error(f"OCRʶ��ʧ��: {str(e)}")
            return "", 0.0
    
    def _clean_text(self, text: str) -> str:
        """����ʶ�������"""
        if not text:
            return ""
        
        # �Ƴ�����Ŀհ��ַ�
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        # �Ƴ������ַ�����ѡ��
        # cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', cleaned_text)
        
        return cleaned_text
    
    def extract_text_from_url(self, image_url: str, language: str = "chi_sim+eng") -> Tuple[str, float]:
        """
        ��URLͼƬ����ȡ����
        
        Args:
            image_url: ͼƬURL
            language: ��������
            
        Returns:
            (ʶ�������, ���Ŷ�)
        """
        import requests
        from io import BytesIO
        
        try:
            # ����ͼƬ
            response = requests.get(image_url)
            response.raise_for_status()
            
            # ת��ΪPIL Image
            image = Image.open(BytesIO(response.content))
            
            # ת��ΪOpenCV��ʽ
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Ԥ����
            processed_image = self._preprocess_cv_image(cv_image)
            
            # OCRʶ��
            data = pytesseract.image_to_data(
                processed_image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # ��ȡ����
            text = pytesseract.image_to_string(processed_image, lang=language)
            
            # �������Ŷ�
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            cleaned_text = self._clean_text(text)
            
            return cleaned_text, avg_confidence
            
        except Exception as e:
            logger.error(f"��URLʶ��OCRʧ��: {str(e)}")
            return "", 0.0
    
    def _preprocess_cv_image(self, image: np.ndarray) -> np.ndarray:
        """Ԥ����OpenCVͼ��"""
        # ת��Ϊ�Ҷ�ͼ
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # ����
        denoised = cv2.medianBlur(gray, 3)
        
        # ��ֵ��
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary


# ȫ��OCR������ʵ��
ocr_processor = OCRProcessor()
