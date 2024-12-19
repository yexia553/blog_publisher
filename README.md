# Blog Publisher

一个自动将 Markdown 博客发布到微信公众号的工具。

## 功能特点

- 自动检测并发布当天的博客文章
- 自动处理和上传文章中的图片
- 支持自定义文章页脚
- 支持多个博客子目录
- 自动使用文章第一张图片作为封面图

## 安装

1. 克隆仓库：

```bash
git clone [your-repo-url]
cd blog_publisher
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：

```bash
export WECHAT_APP_ID="your_app_id"
export WECHAT_APP_SECRET="your_app_secret"
```

## 配置

编辑 `config.py` 文件：

1. 设置博客目录路径
2. 配置博客子目录列表
3. 设置默认封面图片
4. 自定义文章页脚
5. 配置原文链接（可选）：
   ```python
   ORIGINAL_LINK_CONFIG = {
       "enabled": True,  # 是否启用原文链接
       "base_url": "https://example.com",  # 原文链接的基础URL
       "template": "{base_url}/{year}/{filename}",  # 原文链接的模板
       "link_text": "阅读原文"  # 原文链接的显示文本
   }
   ```

## 使用方法

直接运行脚本：

```bash
python publisher.py
```

## Markdown 文章格式要求

每篇文章需要包含以下 frontmatter：

```yaml
---
title: 文章标题
date: 2024-12-12
description: 文章描述（可选）
author: 作者名称（可选）
tags: [标签1, 标签2]（可选）
---
```

## 注意事项

1. 确保文章的 frontmatter 中的 date 格式正确
2. 图片路径使用相对路径
3. 确保微信公众号的 API 权限已开启
