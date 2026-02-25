#!/usr/bin/env python3
"""
Claude Code 官方文档爬取脚本 (Playwright版)
增加等待机制，处理网络慢的情况
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import re

# 目标文档
DOCS = {
    "sub-agents": "https://docs.anthropic.com/en/docs/claude-code/sub-agents",
    "skills": "https://docs.anthropic.com/en/docs/claude-code/skills",
    "slash-commands": "https://docs.anthropic.com/en/docs/claude-code/slash-commands",
    "hooks": "https://docs.anthropic.com/en/docs/claude-code/hooks",
    "plugins": "https://docs.anthropic.com/en/docs/claude-code/plugins",
    "settings": "https://docs.anthropic.com/en/docs/claude-code/settings",
    "agent-teams": "https://docs.anthropic.com/en/docs/claude-code/agent-teams",
    # 额外文档
    "overview": "https://docs.anthropic.com/en/docs/claude-code/overview",
    "quickstart": "https://docs.anthropic.com/en/docs/claude-code/quickstart",
    "best-practices": "https://docs.anthropic.com/en/docs/claude-code/best-practices",
    "features": "https://docs.anthropic.com/en/docs/claude-code/features-overview",
}

OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "claude-code"


def clean_html_to_markdown(html_content: str) -> str:
    """清理 HTML，提取纯文本并转换为 Markdown"""
    if not html_content:
        return None

    # 移除 script 和 style 标签及内容
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # 移除 HTML 注释
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

    # 移除导航和页脚
    html_content = re.sub(r'<nav[^>]*>.*?</nav>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<footer[^>]*>.*?</footer>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<header[^>]*>.*?</header>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # 移除 sidebar
    html_content = re.sub(r'<aside[^>]*>.*?</aside>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # 提取 main 内容
    main_content = re.search(r'<main[^>]*>(.*?)</main>', html_content, re.DOTALL | re.IGNORECASE)
    if main_content:
        html_content = main_content.group(1)
    else:
        # 尝试 article
        article = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL | re.IGNORECASE)
        if article:
            html_content = article.group(1)

    # 替换常见的 HTML 标签为 Markdown
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
        (r'<ul[^>]*>', r'\n'),
        (r'</ul[^>]*>', r'\n'),
        (r'<ol[^>]*>', r'\n'),
        (r'</ol[^>]*>', r'\n'),
        (r'<br\s*/?>', r'\n'),
        (r'<div[^>]*>', r'\n'),
        (r'</div[^>]*>', r'\n'),
        (r'<span[^>]*>', r''),
        (r'</span[^>]*>', r''),
        (r'<table[^>]*>', r'\n| '),
        (r'</table[^>]*>', r'\n'),
        (r'<tr[^>]*>', r'| '),
        (r'</tr[^>]*>', r'\n'),
        (r'<td[^>]*>(.*?)</td>', r'\1 | '),
        (r'<th[^>]*>(.*?)</th>', r'\1 | '),
    ]

    for pattern, replacement in replacements:
        html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL | re.IGNORECASE)

    # 移除剩余的 HTML 标签
    html_content = re.sub(r'<[^>]+>', '', html_content)

    # 解码 HTML 实体
    entities = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&mdash;': '—',
        '&ndash;': '–',
        '&copy;': '©',
        '&reg;': '®',
        '&trade;': '™',
    }
    for entity, char in entities.items():
        html_content = html_content.replace(entity, char)

    # 清理多余空白和换行
    lines = html_content.split('\n')
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned_lines.append('')
            prev_empty = True

    html_content = '\n'.join(cleaned_lines)
    return html_content


def wait_for_page_load(page, timeout=45000):
    """
    等待页面加载完成
    策略：
    1. 等待 networkidle
    2. 检测主要内容出现
    3. 最多等待 timeout 秒
    """
    print("  等待页面加载...")

    # 策略1: 等待网络空闲（最可靠）
    try:
        page.wait_for_load_state("networkidle", timeout=30000)
        print("  ✓ 网络空闲")
    except Exception as e:
        print(f"  ⚠ 网络idle超时: {e}")

    # 策略2: 等待 body 内容开始渲染
    try:
        page.wait_for_selector('body', state='visible', timeout=15000)
        print("  ✓ Body 可见")
    except Exception as e:
        print(f"  ⚠ Body超时: {e}")

    # 策略3: 额外等待确保 JavaScript 执行
    print("  等待 JavaScript 渲染...")
    for i in range(9):  # 9 * 5s = 45s
        page.wait_for_timeout(5000)

        # 检测是否有主要内容
        content = page.content()
        if len(content) > 5000 and 'Page not found' not in content:
            # 检查是否有实际内容
            text = page.locator('body').text_content()
            if text and len(text) > 500:
                print(f"  ✓ 页面已渲染完成 ({len(text)} 字符)")
                return True

        print(f"  等待中... {(i+1)*5}s")

    print("  ⚠ 等待超时，但尝试获取内容")
    return True


def fetch_doc(name: str, url: str) -> str:
    """爬取单个文档"""
    print(f"\n{'='*50}")
    print(f"正在爬取: {name}")
    print(f"URL: {url}")
    print('='*50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 访问页面
            print("  正在访问页面...")
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            print(f"  ✓ DOM 加载完成")

            # 等待页面加载
            wait_for_page_load(page, timeout=45000)

            # 获取页面标题
            title = page.title()
            print(f"  ✓ 页面标题: {title}")

            # 获取渲染后的 HTML
            html_content = page.content()
            print(f"  ✓ 获取 HTML 内容: {len(html_content)} 字符")

            # 检查是否有效 - 只要有足够内容且标题正确就认为成功
            if len(html_content) < 5000:
                print(f"  ✗ 内容太少: {len(html_content)} 字符")
                browser.close()
                return None

            # 检查标题是否包含 "Page not found"
            if 'Page not found' in title:
                print(f"  ✗ 页面不存在: {title}")
                browser.close()
                return None

            print(f"  ✓ 页面有效: {len(html_content)} 字符")

            # 转换为 Markdown
            markdown_content = clean_html_to_markdown(html_content)
            if not markdown_content or len(markdown_content) < 500:
                print(f"  ✗ 转换失败或内容太少")
                browser.close()
                return None

            print(f"  ✓ 转换为 Markdown: {len(markdown_content)} 字符")

            # 提取标题
            title_match = re.search(r'# (.+)', markdown_content)
            if title_match:
                print(f"  ✓ 文档标题: {title_match.group(1)}")

            browser.close()
            return markdown_content

        except Exception as e:
            print(f"  ✗ 错误: {e}")
            browser.close()
            return None


def main():
    """主函数"""
    print("Claude Code 官方文档爬取工具")
    print("="*50)
    print(f"目标: {len(DOCS)} 个文档")
    print("每个文档最长等待: 45秒")
    print("="*50)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    for name, url in DOCS.items():
        content = fetch_doc(name, url)
        if content and len(content) > 500:
            # 保存文件
            output_file = OUTPUT_DIR / f"{name}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {name.replace('-', ' ').title()} 官方文档\n\n")
                f.write(f"> 来源: {url}\n\n")
                f.write(f"> 爬取时间: 自动生成\n\n")
                f.write("---\n\n")
                f.write(content)

            print(f"✓ 已保存: {output_file} ({len(content)} 字符)")
            results[name] = "成功"
        else:
            results[name] = "失败"
            print(f"✗ 跳过: {name}")

    # 打印总结
    print("\n" + "="*50)
    print("爬取完成!")
    print("="*50)
    success = sum(1 for s in results.values() if s == "成功")
    print(f"成功: {success}/{len(results)}")
    for name, status in results.items():
        print(f"- {name}: {status}")


if __name__ == "__main__":
    main()
