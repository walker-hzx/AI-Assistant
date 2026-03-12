#!/usr/bin/env python3
"""
概念搜索学习工具
使用 Playwright 搜索并获取概念信息
"""

import sys
import json
from playwright.sync_api import sync_playwright


def fetch_wikipedia_content(query):
    """获取维基百科内容"""
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=10000)

        # 等待页面加载
        page.wait_for_load_state("domcontentloaded")

        # 获取标题
        title = page.title()

        # 获取主要内容
        try:
            content_elem = page.locator("#mw-content-text")
            paragraphs = content_elem.locator("p").all()[:5]  # 前5段
            content = "\n".join([p.inner_text() for p in paragraphs])
        except:
            content = "无法获取内容"

        browser.close()
        return {
            "source": "wikipedia",
            "name": "维基百科",
            "url": url,
            "title": title,
            "content": content[:2000]  # 限制长度
        }


def fetch_mdn_content(query):
    """获取 MDN 内容"""
    url = f"https://developer.mozilla.org/zh-CN/search?q={query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=10000)

        page.wait_for_load_state("domcontentloaded")

        # 获取标题
        title = page.title()

        # 获取搜索结果
        try:
            results = page.locator("main.content .result").all()[:3]
            content = "\n".join([r.inner_text()[:200] for r in results])
        except:
            content = "无法获取内容"

        browser.close()
        return {
            "source": "mdn",
            "name": "MDN Web Docs",
            "url": url,
            "title": title,
            "content": content[:2000]
        }


def search_and_learn(query, priority="wikipedia"):
    """
    搜索并学习概念

    Args:
        query: 搜索关键词
        priority: 优先搜索源 (wikipedia/mdn)

    Returns:
        dict: 搜索结果和内容
    """
    results = {
        "query": query,
        "priority_source": priority,
        "pages": []
    }

    # 根据优先级确定搜索顺序
    search_order = ["wikipedia", "mdn"] if priority == "wikipedia" else ["mdn", "wikipedia"]

    for source in search_order:
        try:
            if source == "wikipedia":
                page_data = fetch_wikipedia_content(query)
            elif source == "mdn":
                page_data = fetch_mdn_content(query)

            results["pages"].append(page_data)

            # 如果第一个源成功获取到内容，就不再继续
            if page_data.get("content") and "无法获取内容" not in page_data.get("content", ""):
                break

        except Exception as e:
            results["pages"].append({
                "source": source,
                "error": str(e)
            })

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [priority]")
        print("priority: wikipedia (default) or mdn")
        sys.exit(1)

    query = sys.argv[1]
    priority = sys.argv[2] if len(sys.argv) > 2 else "wikipedia"

    result = search_and_learn(query, priority)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
