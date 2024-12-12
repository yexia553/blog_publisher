#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, date
import frontmatter
from pathlib import Path
import logging
from typing import List, Dict, Optional
import markdown
from werobot import WeRoBot
import requests
from config import *
import time
import pickle
import hashlib
from dateutil import parser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageCache:
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict[str, str]:
        """加载缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {str(e)}")
        return {}
        
    def _save_cache(self):
        """保存缓存"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            logger.error(f"Error saving cache: {str(e)}")
            
    def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        return self.cache.get(key)
        
    def set(self, key: str, value: str):
        """设置缓存"""
        self.cache[key] = value
        self._save_cache()

class ConfigurationError(Exception):
    """配置错误异常"""
    pass

class WeChatPublisher:
    def __init__(self):
        self._validate_config()
        self.robot = WeRoBot()
        self.robot.config["APP_ID"] = WECHAT_CONFIG["APP_ID"]
        self.robot.config["APP_SECRET"] = WECHAT_CONFIG["APP_SECRET"]
        self.client = self.robot.client
        self.token = self.client.grant_token()
        self.image_cache = ImageCache(CACHE_FILE)
        
    def _validate_config(self):
        """验证配置是否有效"""
        if not WECHAT_CONFIG.get("APP_ID"):
            raise ConfigurationError("WeChat APP_ID is not configured")
        if not WECHAT_CONFIG.get("APP_SECRET"):
            raise ConfigurationError("WeChat APP_SECRET is not configured")
            
        if not os.path.exists(BLOG_DIR):
            raise ConfigurationError(f"Blog directory {BLOG_DIR} does not exist")
            
        if ORIGINAL_LINK_CONFIG["enabled"]:
            if not ORIGINAL_LINK_CONFIG.get("base_url"):
                raise ConfigurationError("Original link base_url is not configured")
            if not ORIGINAL_LINK_CONFIG.get("template"):
                raise ConfigurationError("Original link template is not configured")
                
    def parse_date(self, date_value) -> Optional[datetime]:
        """统一处理日期格式"""
        if not date_value:
            return None
            
        if isinstance(date_value, datetime):
            return date_value
        elif isinstance(date_value, date):
            return datetime.combine(date_value, datetime.min.time())
        elif isinstance(date_value, str):
            try:
                return parser.parse(date_value)
            except Exception as e:
                logger.error(f"Error parsing date {date_value}: {str(e)}")
                return None
        return None

    def is_publish_date(self, post_date: datetime) -> bool:
        """检查是否应该发布这篇文章"""
        if not post_date:
            return False
            
        today = datetime.now().date()
        post_date = post_date.date() if isinstance(post_date, datetime) else post_date
        return post_date == today

    def get_todays_posts(self) -> List[Path]:
        """获取今天需要发布的文章"""
        posts = []
        
        for subdir in BLOG_SUBDIRS:
            blog_path = Path(BLOG_DIR) / subdir
            if not blog_path.exists():
                continue
                
            for post in blog_path.glob('**/*.md'):
                try:
                    post_data = frontmatter.load(post)
                    post_date = self.parse_date(post_data.get('date'))
                    if post_date and self.is_publish_date(post_date):
                        posts.append(post)
                except Exception as e:
                    logger.error(f"Error processing {post}: {str(e)}")
                    
        return posts
    
    def retry_operation(self, operation, max_retries=3, delay=1):
        """重试机制装饰器"""
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return operation(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Operation failed after {max_retries} retries: {str(e)}")
                        raise
                    logger.warning(f"Retry {retries}/{max_retries} after error: {str(e)}")
                    time.sleep(delay * retries)  # 指数退避
            return None
        return wrapper

    def upload_image(self, image_path: str) -> Optional[str]:
        """上传图片到微信，返回media_id"""
        # 检查缓存
        image_hash = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
        cached_url = self.image_cache.get(image_hash)
        if cached_url:
            return cached_url
            
        @self.retry_operation
        def _upload():
            with open(image_path, 'rb') as f:
                response = self.client.upload_media('image', f)
                return response['url']
        
        try:
            url = _upload()
            if url:
                self.image_cache.set(image_hash, url)
            return url
        except Exception as e:
            logger.error(f"Error uploading image {image_path}: {str(e)}")
            return None
            
    def get_original_link(self, post_path: Path, post_date: datetime) -> Optional[str]:
        """生成原文链接"""
        if not ORIGINAL_LINK_CONFIG["enabled"]:
            return None
            
        filename = post_path.stem  # 获取文件名（不含扩展名）
        year = post_date.strftime('%Y')
        
        return ORIGINAL_LINK_CONFIG["template"].format(
            base_url=ORIGINAL_LINK_CONFIG["base_url"],
            year=year,
            filename=filename
        )

    def process_post_images(self, content: str, post_dir: Path) -> tuple:
        """处理文章中的图片，返回处理后的内容和第一张图片的URL"""
        import re
        
        first_image_url = None
        image_mappings = {}
        
        # 使用正则表达式匹配所有可能的Markdown图片语法
        image_patterns = [
            r'!\[([^\]]*)\]\(([^)]+)\)',  # ![alt](url)
            r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>',  # <img src="url" />
        ]
        
        for pattern in image_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                image_path = match.group(2) if '](' in pattern else match.group(1)
                if not image_path.startswith(('http://', 'https://')):
                    absolute_image_path = str(post_dir / image_path)
                    if os.path.exists(absolute_image_path):
                        new_url = self.upload_image(absolute_image_path)
                        if new_url:
                            image_mappings[image_path] = new_url
                            if not first_image_url:
                                first_image_url = new_url
        
        # 替换图片链接
        for old_path, new_url in image_mappings.items():
            content = content.replace(old_path, new_url)
            
        return content, first_image_url or DEFAULT_COVER_IMAGE
        
    def publish_post(self, post_path: Path):
        """发布单篇文章到微信公众号"""
        try:
            post = frontmatter.load(post_path)
            title = post.get('title', post_path.stem)
            content = post.content
            post_date = self.parse_date(post.get('date'))
            
            # 处理图片
            processed_content, cover_image = self.process_post_images(content, post_path.parent)
            
            # 生成原文链接
            original_link = None
            if post_date:
                original_link = self.get_original_link(post_path, post_date)
            
            # 添加页脚
            final_content = processed_content + "\n" + ARTICLE_FOOTER
            
            # 转换为HTML
            html_content = HTML_TEMPLATE.format(
                content=markdown.markdown(final_content, extensions=MARKDOWN_EXTENSIONS)
            )
            
            # 创建图文消息
            articles = [{
                "title": title,
                "thumb_media_id": cover_image,
                "content": html_content,
                "digest": post.get('description', ''),
                "author": post.get('author', ''),
                "content_source_url": original_link if original_link else '',
                "show_cover_pic": 1
            }]
            
            # 上传图文消息
            @self.retry_operation
            def _publish():
                return self.client.upload_news(articles)
                
            media_id = _publish()
            logger.info(f"Successfully published {title}")
            if original_link:
                logger.info(f"Original link: {original_link}")
            
        except Exception as e:
            logger.error(f"Error publishing {post_path}: {str(e)}")
            raise
            
    def run(self):
        """运行发布程序"""
        posts = self.get_todays_posts()
        if not posts:
            logger.info("No posts to publish today")
            return
            
        for post in posts:
            logger.info(f"Publishing {post}")
            self.publish_post(post)
            
if __name__ == "__main__":
    publisher = WeChatPublisher()
    publisher.run()
