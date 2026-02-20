#!/usr/bin/env python3
"""
Claude Code 文档爬取脚本 (使用 Playwright)
用于获取官方文档并转换为 Markdown 格式
"""

import os
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# 要获取的核心文档列表
CORE_DOCS = [
    "skills",
    "hooks",
    "sub-agents",
    "plugins",
    "settings",
    "commands",
    "permissions",
]

BASE_URL = "https://code.claude.com/docs/zh-CN"
OUTPUT_DIR = "/Users/huangzhixin/Desktop/Code/AI/AI-Assistant/docs/claude-code"


def clean_html_to_markdown(html_content):
    """将 HTML 内容转换为 Markdown"""
    if not html_content:
        return ""

    import re

    # 移除脚本和样式
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # 移除导航栏、页脚等无关内容
    text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<header[^>]*>.*?</header>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<aside[^>]*>.*?</aside>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # 移除搜索框
    text = re.sub(r'<input[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<button[^>]*>.*?</button>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # 提取 main 内容区域
    main_match = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL | re.IGNORECASE)
    if main_match:
        text = main_match.group(1)
    else:
        # 如果没有 main，尝试 article
        article_match = re.search(r'<article[^>]*>(.*?)</article>', text, re.DOTALL | re.IGNORECASE)
        if article_match:
            text = article_match.group(1)

    # 代码块
    text = re.sub(r'<pre><code[^>]*>', '```\n', text)
    text = re.sub(r'</code></pre>', '\n```', text)
    text = re.sub(r'<code[^>]*>', '`', text)
    text = re.sub(r'</code>', '`', text)

    # 标题
    for i in range(6, 0, -1):
        text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', r'\n' + '#' * i + r' \1\n', text)

    # 粗体和斜体
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text)

    # 链接
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text)

    # 列表
    text = re.sub(r'<li>(.*?)</li>', r'- \1\n', text)
    text = re.sub(r'<ul[^>]*>', '\n', text)
    text = re.sub(r'</ul>', '\n', text)
    text = re.sub(r'<ol[^>]*>', '\n', text)
    text = re.sub(r'</ol>', '\n', text)

    # 段落和换行
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*>(.*?)</div>', r'\1\n', text, flags=re.DOTALL)

    # 表格 - 简单处理
    text = re.sub(r'<table[^>]*>', '\n', text)
    text = re.sub(r'</table>', '\n', text)
    text = re.sub(r'<tr[^>]*>', '| ', text)
    text = re.sub(r'</tr>', '\n', text)
    text = re.sub(r'<td[^>]*>(.*?)</td>', r'\1 | ', text)
    text = re.sub(r'<th[^>]*>(.*?)</th>', r'\1 | ', text)

    # 移除剩余标签
    text = re.sub(r'<[^>]+>', '', text)

    # 解码 HTML 实体
    from html import unescape
    text = unescape(text)

    # 清理
    text = re.sub(r'\n{4,}', '\n\n', text)
    text = text.strip()

    return text


def fetch_page(url, playwright):
    """获取页面内容"""
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
        # 等待页面加载完成
        time.sleep(2)

        # 获取渲染后的 HTML
        html = page.content()
        return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    finally:
        browser.close()


def save_doc(doc_name, content, title, source_url):
    """保存文档内容"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = os.path.join(OUTPUT_DIR, f"{doc_name}.md")

    # 构建完整的 Markdown 文件
    md_content = f"""---
title: {title}
source: {source_url}
---

# {title}

{content}
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Saved: {filename} ({len(content)} chars)")
    return filename


def extract_title(html):
    """从 HTML 提取标题"""
    import re
    title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()

    title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()

    return ""


def main():
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Fetching {len(CORE_DOCS)} core documents with Playwright...\n")

    with sync_playwright() as playwright:
        success_count = 0
        failed_docs = []

        for i, doc in enumerate(CORE_DOCS):
            url = f"{BASE_URL}/{doc}"
            print(f"[{i+1}/{len(CORE_DOCS)}] Fetching: {doc}")

            html = fetch_page(url, playwright)
            if html:
                # 提取标题
                title = extract_title(html)

                # 转换为 Markdown
                content = clean_html_to_markdown(html)

                if content:
                    save_doc(doc, content, title, url)
                    print(f"  -> Title: {title}")
                    success_count += 1
                else:
                    print(f"  -> No content extracted")
                    failed_docs.append(doc)
            else:
                print(f"  -> Failed to fetch")
                failed_docs.append(doc)

            time.sleep(1)  # 避免请求过快

    print(f"\n{'='*50}")
    print(f"Completed: {success_count}/{len(CORE_DOCS)} successful")

    if failed_docs:
        print(f"Failed: {', '.join(failed_docs)}")


if __name__ == "__main__":
    main()
