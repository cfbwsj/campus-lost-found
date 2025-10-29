-- 校园失物招领系统 - MySQL数据库表结构
-- 创建时间：2025-01-16

-- 使用aiweb数据库
USE aiweb;

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS `found_items`;
DROP TABLE IF EXISTS `lost_items`;

-- 创建失物信息表
CREATE TABLE `lost_items` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(200) NOT NULL COMMENT '失物标题',
  `description` text COMMENT '失物描述',
  `category` varchar(50) DEFAULT NULL COMMENT '物品类别',
  `location` varchar(200) DEFAULT NULL COMMENT '发现地点',
  `contact_info` varchar(200) DEFAULT NULL COMMENT '联系方式',
  `image_url` varchar(500) DEFAULT NULL COMMENT '图片URL',
  `ocr_text` text COMMENT 'OCR识别的文字',
  `ai_category` varchar(50) DEFAULT NULL COMMENT 'AI识别的类别',
  `confidence` float DEFAULT NULL COMMENT 'AI识别置信度',
  `status` varchar(20) DEFAULT 'lost' COMMENT '状态：lost/found/claimed',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_active` tinyint(1) DEFAULT 1 COMMENT '是否有效',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='失物信息表';

-- 创建招领信息表
CREATE TABLE `found_items` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(200) NOT NULL COMMENT '招领标题',
  `description` text COMMENT '招领描述',
  `category` varchar(50) DEFAULT NULL COMMENT '物品类别',
  `location` varchar(200) DEFAULT NULL COMMENT '发现地点',
  `contact_info` varchar(200) DEFAULT NULL COMMENT '联系方式',
  `image_url` varchar(500) DEFAULT NULL COMMENT '图片URL',
  `ocr_text` text COMMENT 'OCR识别的文字',
  `ai_category` varchar(50) DEFAULT NULL COMMENT 'AI识别的类别',
  `confidence` float DEFAULT NULL COMMENT 'AI识别置信度',
  `status` varchar(20) DEFAULT 'found' COMMENT '状态：found/claimed',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_active` tinyint(1) DEFAULT 1 COMMENT '是否有效',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='招领信息表';

-- 插入一些示例数据
INSERT INTO `lost_items` (`title`, `description`, `category`, `location`, `contact_info`, `status`) VALUES
('丢失黑色iPhone', '在图书馆三楼丢失一部黑色iPhone 13，有蓝色手机壳', '手机/数码产品', '图书馆三楼', '13800138000', 'lost'),
('丢失学生卡', '在食堂丢失学生卡，姓名：张三', '钱包/证件', '第一食堂', '13900139000', 'lost'),
('丢失钥匙串', '在宿舍楼附近丢失一串钥匙，有3把钥匙', '钥匙/门卡', '宿舍楼A栋', '13700137000', 'lost');

INSERT INTO `found_items` (`title`, `description`, `category`, `location`, `contact_info`, `status`) VALUES
('捡到黑色钱包', '在操场捡到一个黑色钱包，内有身份证和现金', '钱包/证件', '操场', '13600136000', 'found'),
('捡到蓝色水杯', '在教室捡到一个蓝色保温水杯', '其他', '教学楼201', '13500135000', 'found'),
('捡到眼镜', '在图书馆捡到一副黑色眼镜', '眼镜/配饰', '图书馆二楼', '13400134000', 'found');

-- 查看创建的表
SHOW TABLES;

-- 查看表结构
DESCRIBE lost_items;
DESCRIBE found_items;
