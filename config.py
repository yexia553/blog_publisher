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

# HTML template
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
