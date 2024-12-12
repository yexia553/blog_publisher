#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# Blog directory configuration
BLOG_DIR = os.path.expanduser("~/blog")  # Change this to your blog directory
BLOG_SUBDIRS = ["tech", "invest", "reading"]  # Your blog subdirectories

# WeChat configuration
WECHAT_CONFIG = {
    "APP_ID": os.getenv("WECHAT_APP_ID"),
    "APP_SECRET": os.getenv("WECHAT_APP_SECRET"),
}

# Default cover image if no image in the post
DEFAULT_COVER_IMAGE = "https://your-default-cover-image-url.jpg"

# 原文链接配置
ORIGINAL_LINK_CONFIG = {
    "enabled": True,  # 是否启用原文链接
    "base_url": "https://example.com",  # 原文链接的基础URL
    "template": "{base_url}/{year}/{filename}",  # 原文链接的模板
    "link_text": "阅读原文",  # 原文链接的显示文本
}

# Article footer template
ARTICLE_FOOTER = """
---
欢迎关注我的公众号
如果觉得文章对你有帮助，欢迎点赞、在看、分享~
"""

# Cache configuration
CACHE_FILE = "cache.bin"

# Markdown extensions
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.toc'
]
