#!/usr/bin/env python3
"""
Claude Code 文档获取脚本 (优化版)
用于获取官方文档并转换为 Markdown 格式
"""

import urllib.request
import urllib.error
import re
import os
import sys
import json

# 尝试导入 markdownify，如果不存在则使用备用方案
try:
    from markdownify import markdownify as md
    HAS_MARKDOWNIFY = True
except ImportError:
    HAS_MARKDOWNIFY = False
    # 备用简单转换函数
    def simple_html_to_md(html):
        """简单的 HTML 到 Markdown 转换"""
        if not html:
            return ""

        # 保留代码块
        text = re.sub(r'<pre><code[^>]*>(.*?)</code></pre>',
                      lambda m: '```\n' + m.group(1) + '\n```', html, flags=re.DOTALL)

        # 保留内联代码
        text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text)

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

        # 移除剩余标签
        text = re.sub(r'<[^>]+>', '', text)

        # 解码 HTML 实体
        from html import unescape
        text = unescape(text)

        # 清理
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        return text

# 要获取的核心文档列表
CORE_DOCS = [
    "skills",
    "hooks",
    "sub-agents",
    "plugins",
    "settings",
]

# 备用文档列表
EXTRA_DOCS = [
    "commands",
    "permissions",
]

BASE_URL = "https://code.claude.com/docs/zh-CN"
OUTPUT_DIR = "/Users/huangzhixin/Desktop/Code/AI/AI-Assistant/docs/claude-code"


def fetch_page(url):
    """获取页面内容"""
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} fetching {url}: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_main_content(html):
    """提取主要内容和元数据"""
    if not html:
        return {"title": "", "content": "", "toc": ""}

    # 提取标题
    title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else ""

    # 尝试提取 main 内容区域
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
    content = main_match.group(1) if main_match else html

    # 如果没有 main，尝试 article
    if not main_match:
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
        if article_match:
            content = article_match.group(1)

    # 提取目录 (如果有)
    toc_match = re.search(r'<nav[^>]*class="[^"]*toc[^"]*"[^>]*>(.*?)</nav>', html, re.DOTALL | re.IGNORECASE)
    toc = toc_match.group(1) if toc_match else ""

    return {
        "title": title,
        "content": content,
        "toc": toc
    }


def convert_to_markdown(data):
    """将 HTML 内容转换为 Markdown"""
    content = data.get("content", "")

    if HAS_MARKDOWNIFY:
        # 使用 markdownify 转换
        md_content = md(content, heading_style="ATX")
    else:
        # 使用备用方案
        md_content = simple_html_to_md(content)

    return md_content


def clean_markdown(md_text):
    """清理 Markdown 内容"""
    # 移除多余空行
    md_text = re.sub(r'\n{4,}', '\n\n', md_text)

    # 修复代码块格式
    md_text = re.sub(r'```\n```', '```\n', md_text)

    # 移除可能的残留
    md_text = re.sub(r'^\s+$', '', md_text, flags=re.MULTILINE)

    return md_text.strip()


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


def main():
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Using markdownify: {HAS_MARKDOWNIFY}")
    print(f"Fetching {len(CORE_DOCS)} core documents...\n")

    success_count = 0
    failed_docs = []

    for i, doc in enumerate(CORE_DOCS):
        url = f"{BASE_URL}/{doc}"
        print(f"[{i+1}/{len(CORE_DOCS)}] Fetching: {doc}")

        html = fetch_page(url)
        if html:
            data = extract_main_content(html)
            md_content = convert_to_markdown(data)
            md_content = clean_markdown(md_content)

            if md_content:
                save_doc(doc, md_content, data.get("title", doc), url)
                print(f"  -> Title: {data.get('title', 'N/A')}")
                success_count += 1
            else:
                print(f"  -> No content extracted")
                failed_docs.append(doc)
        else:
            print(f"  -> Failed to fetch")
            failed_docs.append(doc)

        # 避免请求过快
        import time
        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"Completed: {success_count}/{len(CORE_DOCS)} successful")

    if failed_docs:
        print(f"Failed: {', '.join(failed_docs)}")

    # 输出安装 markdownify 的说明
    if not HAS_MARKDOWNIFY:
        print("\n" + "="*50)
        print("Tip: Install markdownify for better conversion:")
        print("  pip install markdownify")


if __name__ == "__main__":
    main()
