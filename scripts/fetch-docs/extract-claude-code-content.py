#!/usr/bin/env python3
"""
Claude Code 文档内容提取脚本 v2
改进版：更好的导航过滤和内容提取
"""

import re
from pathlib import Path

INPUT_DIR = Path("docs/claude-code")
OUTPUT_DIR = Path("docs/claude-code-extracted")


def extract_content(html_content: str) -> str:
    """从 HTML 中提取正文内容"""
    if not html_content:
        return None

    # 移除 script 和 style 标签
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

    # 移除导航相关区域
    html_content = re.sub(r'<nav[^>]*>.*?</nav>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<footer[^>]*>.*?</footer>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<header[^>]*>.*?</header>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<aside[^>]*>.*?</aside>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # 提取 main 内容
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html_content, re.DOTALL | re.IGNORECASE)
    if main_match:
        html_content = main_match.group(1)
    else:
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL | re.IGNORECASE)
        if article_match:
            html_content = article_match.group(1)

    # 替换 HTML 标签
    replacements = [
        (r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n'),
        (r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n'),
        (r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n'),
        (r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n'),
        (r'<h5[^>]*>(.*?)</h5>', r'##### \1\n\n'),
        (r'<h6[^>]*>(.*?)</h6>', r'###### \1\n\n'),
        (r'<p[^>]*>(.*?)</p>', r'\1\n\n'),
        (r'<strong[^>]*>(.*?)</strong>', r'**\1**'),
        (r'<b[^>]*>(.*?)</b>', r'**\1**'),
        (r'<em[^>]*>(.*?)</em>', r'*\1*'),
        (r'<i[^>]*>(.*?)</i>', r'*\1*'),
        (r'<code[^>]*>(.*?)</code>', r'`\1`'),
        (r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```\n'),
        (r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)'),
        (r'<li[^>]*>(.*?)</li>', r'- \1\n'),
        (r'<br\s*/?>', r'\n'),
        (r'<div[^>]*>', r'\n'),
        (r'</div[^>]*>', r'\n'),
        (r'<span[^>]*>', r''),
        (r'</span[^>]*>', r''),
    ]

    for pattern, replacement in replacements:
        html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL | re.IGNORECASE)

    # 移除剩余 HTML
    html_content = re.sub(r'<[^>]+>', '', html_content)

    # 解码 HTML 实体
    entities = {
        '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
        '&quot;': '"', '&#39;': "'", '&mdash;': '—', '&ndash;': '–',
        '&copy;': '©', '&reg;': '®', '&trade;': '™',
    }
    for entity, char in entities.items():
        html_content = html_content.replace(entity, char)

    # 清理行
    lines = html_content.split('\n')
    cleaned_lines = []
    skip_patterns = [
        'skip to', 'navigation', 'claude code docs', 'home page',
        'search', 'build with claude code', 'getting started',
        'deployment', 'administration', 'configuration',
        'reference', 'resources', 'legal', 'english',
        'cmd', 'ask ai'
    ]

    for line in lines:
        line = line.strip()
        line_lower = line.lower()

        # 跳过纯导航行
        if not line:
            continue

        # 跳过导航相关行
        if any(p in line_lower for p in skip_patterns) and len(line) < 50:
            continue

        # 跳过链接行
        if re.match(r'^\[.*\]\(.*\)$', line):
            if any(p in line_lower for p in skip_patterns):
                continue

        cleaned_lines.append(line)

    # 合并空行
    result_lines = []
    prev_empty = False
    for line in cleaned_lines:
        if not line:
            if not prev_empty:
                result_lines.append('')
                prev_empty = True
        else:
            result_lines.append(line)
            prev_empty = False

    return '\n'.join(result_lines)


def process_file(input_file: Path, output_file: Path):
    """处理单个文件"""
    print(f"处理: {input_file.name}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    content = extract_content(html_content)

    if not content or len(content) < 100:
        print(f"  ✗ 内容提取失败")
        return False

    # 写入输出
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ 提取完成: {len(content)} 字符")
    return True


def main():
    """主函数"""
    print("Claude Code 文档内容提取工具 v2")
    print("="*50)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    md_files = list(INPUT_DIR.glob("*.md"))
    print(f"找到 {len(md_files)} 个文档")

    results = {}
    for md_file in md_files:
        output_file = OUTPUT_DIR / md_file.name
        success = process_file(md_file, output_file)
        results[md_file.name] = "成功" if success else "失败"

    print("\n" + "="*50)
    print("提取完成!")
    print("="*50)
    success_count = sum(1 for s in results.values() if s == "成功")
    print(f"成功: {success_count}/{len(results)}")


if __name__ == "__main__":
    main()
