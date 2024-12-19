#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration Module

Contains configuration settings for:
1. Common settings (blog directories, cache)
2. Markdown processing (image handling, formatting)
3. WeChat publishing (API credentials, templates)
"""

import os
from pathlib import Path

# =====================
# Common Configuration
# =====================
# Blog directory configuration
BLOG_DIR = os.path.expanduser("/Users/felix/workspace/working-notes")
BLOG_SUBDIRS = ["myNotes"]

# Cache configuration
CACHE_FILE = "cache.bin"

# Base URL for blog and images
BLOG_BASE_URL = "https://panzhixiang.cn"
IMAGE_BASE_URL = "https://blog.panzhixiang.cn"

# =====================
# WeChat Configuration
# =====================
# WeChat API credentials
WECHAT_CONFIG = {
    "APP_ID": os.getenv("WECHAT_APP_ID"),
    "APP_SECRET": os.getenv("WECHAT_APP_SECRET"),
}

# Default cover image if no image in the post
DEFAULT_COVER_IMAGE = "https://blog.panzhixiang.cn/images/%E6%9E%B8%E6%9D%9E%E5%B2%9B%E7%9A%84%E6%97%A5%E5%87%BA.jpg"

# Original article link configuration
ORIGINAL_LINK_CONFIG = {
    "enabled": True,
    "base_url": BLOG_BASE_URL,
    "template": "{base_url}/{year}/{filename}",
    "link_text": "阅读原文",
}

# ===========================
# Markdown Processing Config
# ===========================
# Image processing configuration
IMAGE_CONFIG = {
    "base_url": IMAGE_BASE_URL,
    "local_patterns": ["../images/", "./images/", "images/"],
}

# Article footer template
ARTICLE_FOOTER = """
---
欢迎关注我的公众号：**潘智祥**
如果您喜欢使用电脑看文章，也可以关注我的博客：[https://panzhixiang.cn](https://panzhixiang.cn)
"""

# Markdown extensions for processing
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.toc'
]

# HTML template for rendering
HTML_TEMPLATE = """
<div class="article-content">
    {content}
</div>
<style>
    .article-content {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 100%;
        margin: 0 auto;
        padding: 15px;
    }
    .article-content img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1em auto;
    }
    .article-content pre {
        background-color: #f6f8fa;
        border-radius: 3px;
        padding: 16px;
        overflow: auto;
    }
    .article-content code {
        font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
        background-color: #f6f8fa;
        padding: 2px 4px;
        border-radius: 3px;
    }
    .article-content h1,
    .article-content h2,
    .article-content h3,
    .article-content h4,
    .article-content h5,
    .article-content h6 {
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.25;
    }
    .article-content p {
        margin-bottom: 16px;
    }
    .article-content ul,
    .article-content ol {
        margin-bottom: 16px;
        padding-left: 2em;
    }
    .article-content blockquote {
        padding: 0 1em;
        color: #6a737d;
        border-left: 0.25em solid #dfe2e5;
        margin: 0 0 16px 0;
    }
    .article-content table {
        border-spacing: 0;
        border-collapse: collapse;
        margin-bottom: 16px;
        width: 100%;
    }
    .article-content table th,
    .article-content table td {
        padding: 6px 13px;
        border: 1px solid #dfe2e5;
    }
    .article-content table tr:nth-child(2n) {
        background-color: #f6f8fa;
    }
</style>
"""