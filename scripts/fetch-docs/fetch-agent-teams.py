#!/usr/bin/env python3
"""
Claude Code Agent Teams 文档爬取脚本
"""

from playwright.sync_api import sync_playwright
import json

URL = "https://code.claude.com/docs/zh-CN/agent-teams"

def fetch_docs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"正在访问: {URL}")
        page.goto(URL, wait_until="networkidle")

        # 获取页面标题
        title = page.title()
        print(f"页面标题: {title}")

        # 获取所有文本内容
        content = page.content()

        # 尝试获取主要的文档内容
        # 查找 article 或 main 内容区域
        article = page.locator("article, main, .content, #content").first
        if article.count() > 0:
            text_content = article.text_content()
            print(f"\n=== 文档内容 ===")
            print(text_content[:5000])

        # 获取所有标题
        print(f"\n=== 页面结构 ===")
        headings = page.locator("h1, h2, h3, h4").all()
        for h in headings:
            print(f"- {h.text_content()}")

        # 获取链接
        print(f"\n=== 相关链接 ===")
        links = page.locator("a").all()
        for link in links[:20]:
            href = link.get_attribute("href")
            text = link.text_content()
            if href and text:
                print(f"- {text}: {href}")

        browser.close()

if __name__ == "__main__":
    fetch_docs()
