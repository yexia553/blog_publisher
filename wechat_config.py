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

BLOG_DIR = os.path.expanduser("/Users/felix/workspace/working-notes")
BLOG_SUBDIRS = ["myNotes"]

# Cache configuration
CACHE_FILE = "cache.bin"

# Base URL for blog and images
BLOG_BASE_URL = "https://panzhixiang.cn"
IMAGE_BASE_URL = "https://blog.panzhixiang.cn"

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

# Article footer template
ARTICLE_FOOTER = """
---
欢迎关注我的公众号：**潘智祥**
"""

# Markdown extensions for processing
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.toc',
    'markdown.extensions.fenced_code'
]

# Markdown extension configurations
MARKDOWN_EXTENSION_CONFIGS = {
    'codehilite': {
        'css_class': 'highlight',
        'linenums': False,
        'guess_lang': False
    }
}

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
        margin: 1em 0;
    }
    .article-content code {
        font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
        background-color: #f6f8fa;
        padding: 2px 4px;
        border-radius: 3px;
    }
    /* Code highlighting styles */
    .highlight { background-color: #f6f8fa; padding: 1em; border-radius: 3px; }
    .highlight .hll { background-color: #ffc; }
    .highlight .c { color: #999988; font-style: italic } /* Comment */
    .highlight .k { color: #000000; font-weight: bold } /* Keyword */
    .highlight .o { color: #000000; font-weight: bold } /* Operator */
    .highlight .cm { color: #999988; font-style: italic } /* Comment.Multiline */
    .highlight .cp { color: #999999; font-weight: bold; font-style: italic } /* Comment.Preproc */
    .highlight .c1 { color: #999988; font-style: italic } /* Comment.Single */
    .highlight .cs { color: #999999; font-weight: bold; font-style: italic } /* Comment.Special */
    .highlight .gd { color: #000000; background-color: #ffdddd } /* Generic.Deleted */
    .highlight .ge { color: #000000; font-style: italic } /* Generic.Emph */
    .highlight .gr { color: #aa0000 } /* Generic.Error */
    .highlight .gh { color: #999999 } /* Generic.Heading */
    .highlight .gi { color: #000000; background-color: #ddffdd } /* Generic.Inserted */
    .highlight .go { color: #888888 } /* Generic.Output */
    .highlight .gp { color: #555555 } /* Generic.Prompt */
    .highlight .gs { font-weight: bold } /* Generic.Strong */
    .highlight .gu { color: #aaaaaa } /* Generic.Subheading */
    .highlight .gt { color: #aa0000 } /* Generic.Traceback */
    .highlight .kc { color: #000000; font-weight: bold } /* Keyword.Constant */
    .highlight .kd { color: #000000; font-weight: bold } /* Keyword.Declaration */
    .highlight .kn { color: #000000; font-weight: bold } /* Keyword.Namespace */
    .highlight .kp { color: #000000; font-weight: bold } /* Keyword.Pseudo */
    .highlight .kr { color: #000000; font-weight: bold } /* Keyword.Reserved */
    .highlight .kt { color: #445588; font-weight: bold } /* Keyword.Type */
    .highlight .m { color: #009999 } /* Literal.Number */
    .highlight .s { color: #d01040 } /* Literal.String */
    .highlight .na { color: #008080 } /* Name.Attribute */
    .highlight .nb { color: #0086B3 } /* Name.Builtin */
    .highlight .nc { color: #445588; font-weight: bold } /* Name.Class */
    .highlight .no { color: #008080 } /* Name.Constant */
    .highlight .nd { color: #3c5d5d; font-weight: bold } /* Name.Decorator */
    .highlight .ni { color: #800080 } /* Name.Entity */
    .highlight .ne { color: #990000; font-weight: bold } /* Name.Exception */
    .highlight .nf { color: #990000; font-weight: bold } /* Name.Function */
    .highlight .nl { color: #990000; font-weight: bold } /* Name.Label */
    .highlight .nn { color: #555555 } /* Name.Namespace */
    .highlight .nt { color: #000080 } /* Name.Tag */
    .highlight .nv { color: #008080 } /* Name.Variable */
    .highlight .ow { color: #000000; font-weight: bold } /* Operator.Word */
    .highlight .w { color: #bbbbbb } /* Text.Whitespace */
    .highlight .mf { color: #009999 } /* Literal.Number.Float */
    .highlight .mh { color: #009999 } /* Literal.Number.Hex */
    .highlight .mi { color: #009999 } /* Literal.Number.Integer */
    .highlight .mo { color: #009999 } /* Literal.Number.Oct */
    .highlight .sb { color: #d01040 } /* Literal.String.Backtick */
    .highlight .sc { color: #d01040 } /* Literal.String.Char */
    .highlight .sd { color: #d01040 } /* Literal.String.Doc */
    .highlight .s2 { color: #d01040 } /* Literal.String.Double */
    .highlight .se { color: #d01040 } /* Literal.String.Escape */
    .highlight .sh { color: #d01040 } /* Literal.String.Heredoc */
    .highlight .si { color: #d01040 } /* Literal.String.Interpol */
    .highlight .sx { color: #d01040 } /* Literal.String.Other */
    .highlight .sr { color: #009926 } /* Literal.String.Regex */
    .highlight .s1 { color: #d01040 } /* Literal.String.Single */
    .highlight .ss { color: #990073 } /* Literal.String.Symbol */
    .highlight .bp { color: #999999 } /* Name.Builtin.Pseudo */
    .highlight .vc { color: #008080 } /* Name.Variable.Class */
    .highlight .vg { color: #008080 } /* Name.Variable.Global */
    .highlight .vi { color: #008080 } /* Name.Variable.Instance */
    .highlight .il { color: #009999 } /* Literal.Number.Integer.Long */
</style>
"""