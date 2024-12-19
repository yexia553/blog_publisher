#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Blog Processor Module

This module processes markdown blog files by:
1. Processing blogs for a specific date (defaults to today)
2. Removing markdown frontmatter
3. Adding custom footer
4. Generating new markdown files with processed content
5. Converting local image paths to online URLs
"""

import os
from datetime import datetime
from pathlib import Path
import re
from typing import Optional, List
import frontmatter
from config import (
    BLOG_DIR,
    BLOG_SUBDIRS,
    ARTICLE_FOOTER,
    IMAGE_CONFIG
)

class BlogProcessor:
    """Process markdown blog files according to specified requirements"""
    
    def __init__(self, target_date: Optional[str] = None, output_dir: Optional[str] = None):
        """
        Initialize the blog processor
        
        Args:
            target_date: Optional date string in 'YYYY-MM-DD' format
            output_dir: Optional output directory path for processed files
        """
        self.target_date = (datetime.strptime(target_date, '%Y-%m-%d').date() 
                           if target_date else datetime.now().date())
        self.default_output_dir = os.path.join(os.getcwd(), 'processed_blogs')
        self.output_dir = output_dir or self.default_output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Clean up default output directory if using default path
        if self.output_dir == self.default_output_dir:
            self._cleanup_default_output_dir()

    def _cleanup_default_output_dir(self):
        """Clean up existing files in the default output directory"""
        if not os.path.exists(self.default_output_dir):
            return
            
        for file in os.listdir(self.default_output_dir):
            if file.endswith('.md'):
                file_path = os.path.join(self.default_output_dir, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error removing file {file}: {e}")

    def get_blog_files(self) -> List[Path]:
        """Get all blog files from configured directories matching target date"""
        blog_files = []
        for subdir in BLOG_SUBDIRS:
            blog_path = Path(BLOG_DIR) / subdir
            if not blog_path.exists():
                continue
            
            for file in blog_path.glob('**/*.md'):
                post = frontmatter.load(file)
                post_date = post.get('date')
                if post_date:
                    if isinstance(post_date, str):
                        post_date = datetime.strptime(post_date, '%Y-%m-%d').date()
                    if post_date == self.target_date:
                        blog_files.append(file)
        
        return blog_files

    def process_images(self, content: str, file_path: Path) -> str:
        """
        Process local image links in markdown content to online URLs
        
        Args:
            content: Markdown content
            file_path: Path to the blog file for resolving relative paths
            
        Returns:
            Content with processed image links
        """
        def replace_image_path(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Check if path matches any local pattern
            for pattern in IMAGE_CONFIG['local_patterns']:
                if image_path.startswith(pattern):
                    # Extract image name and create online URL
                    image_name = image_path.split('/')[-1]
                    online_path = f"{IMAGE_CONFIG['base_url']}/images/{image_name}"
                    return f"![{alt_text}]({online_path})"
            
            # Return original if not a local image
            return match.group(0)
        
        # Match markdown image syntax: ![alt text](image path)
        image_pattern = r'!\[(.*?)\]\((.*?)\)'
        processed_content = re.sub(image_pattern, replace_image_path, content)
        return processed_content

    def process_blog(self, file_path: Path) -> str:
        """
        Process a single blog file
        
        Args:
            file_path: Path to the blog file
            
        Returns:
            Processed content as string
        """
        post = frontmatter.load(file_path)
        content = post.content
        
        # Process images
        content = self.process_images(content, file_path)
        
        # Add footer
        processed_content = f"{content}\n\n{ARTICLE_FOOTER}"
        return processed_content

    def save_processed_blog(self, original_path: Path, processed_content: str):
        """
        Save processed blog content to new file
        
        Args:
            original_path: Original blog file path
            processed_content: Processed blog content
        """
        output_filename = f"processed_{original_path.stem}_{self.target_date}.md"
        output_path = Path(self.output_dir) / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        return output_path

    def process_blogs(self):
        """Process all matching blog files"""
        blog_files = self.get_blog_files()
        
        if not blog_files:
            print(f"No blog files found for date: {self.target_date}")
            return
        
        for file_path in blog_files:
            processed_content = self.process_blog(file_path)
            output_path = self.save_processed_blog(file_path, processed_content)
            print(f"Processed {file_path.name} -> {output_path}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process markdown blog files')
    parser.add_argument('--date', help='Target date in YYYY-MM-DD format')
    parser.add_argument('--output-dir', help='Output directory for processed files')
    
    args = parser.parse_args()
    
    processor = BlogProcessor(args.date, args.output_dir)
    processor.process_blogs()

if __name__ == '__main__':
    main()
