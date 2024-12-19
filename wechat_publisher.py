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
from wechat_config import *
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

    def process_post_images(self, content: str, post_dir: Path) -> tuple:
        """Process article images and return processed content and first image's media_id"""
        import re
        
        first_image_media_id = None
        image_mappings = {}
        
        # Match all possible Markdown image syntax
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
                        # Upload image and get media_id for WeChat
                        with open(absolute_image_path, 'rb') as f:
                            try:
                                response = self.client.upload_media('image', f)
                                if not first_image_media_id:
                                    first_image_media_id = response['media_id']
                                # Get permanent URL for article content
                                image_url = response.get('url')
                                if image_url:
                                    image_mappings[image_path] = image_url
                            except Exception as e:
                                logger.error(f"Error uploading image {absolute_image_path}: {str(e)}")
        
        # Replace image links in content
        for old_path, new_url in image_mappings.items():
            content = content.replace(old_path, new_url)
        
        # If no cover image found, upload default cover
        if not first_image_media_id:
            try:
                response = requests.get(DEFAULT_COVER_IMAGE)
                if response.status_code == 200:
                    from tempfile import NamedTemporaryFile
                    with NamedTemporaryFile(suffix='.jpg') as temp_file:
                        temp_file.write(response.content)
                        temp_file.flush()
                        with open(temp_file.name, 'rb') as f:
                            response = self.client.upload_media('image', f)
                            first_image_media_id = response['media_id']
            except Exception as e:
                logger.error(f"Error uploading default cover image: {str(e)}")
        
        return content, first_image_media_id

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

    def publish_post(self, post_path: Path):
        """Publish a single article to WeChat Official Account"""
        try:
            post = frontmatter.load(post_path)
            title = post.get('title', post_path.stem)
            content = post.content
            post_date = self.parse_date(post.get('date'))
            
            # Process images and get cover image media_id
            processed_content, cover_media_id = self.process_post_images(content, post_path.parent)
            
            # Generate original link
            original_link = None
            if post_date:
                original_link = self.get_original_link(post_path, post_date)
            
            # Add footer
            final_content = processed_content + "\n" + ARTICLE_FOOTER
            
            # Convert to HTML with code highlighting
            html_content = HTML_TEMPLATE.format(
                content=markdown.markdown(
                    final_content,
                    extensions=MARKDOWN_EXTENSIONS,
                    extension_configs=MARKDOWN_EXTENSION_CONFIGS
                )
            )
            
            # Create article message
            articles = [{
                "title": title,
                "thumb_media_id": cover_media_id,
                "content": html_content,
                "digest": post.get('description', ''),
                "author": post.get('author', ''),
                "content_source_url": original_link if original_link else '',
                "show_cover_pic": 1
            }]
            
            # Upload article
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
