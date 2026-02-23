#!/usr/bin/env python3
"""
概念搜索学习工具
使用 Playwright 搜索并获取概念信息
"""

import sys
import json
from playwright.sync_api import sync_playwright

# 优先搜索的网站配置
PRIORITY_SOURCES = {
    "wikipedia": {
        "url": "https://en.wikipedia.org/wiki/",
        "name": "维基百科",
        "selector": "#mw-content-text .mw-parser-output"
    },
    "mdn": {
        "url": "https://developer.mozilla.org/zh-CN/search?q=",
        "name": "MDN Web Docs",
        "selector": "main.content"
    },
    "zhihu": {
        "url": "https://www.zhihu.com/search?q=",
        "name": "知乎",
        "selector": ".List-item"
    }
}

def search_wikipedia(query):
    """搜索维基百科"""
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    return {"source": "wikipedia", "url": url}

def search_mdn(query):
    """搜索 MDN"""
    url = f"https://developer.mozilla.org/zh-CN/search?q={query}"
    return {"source": "mdn", "url": url}

def search_google(query):
    """用 Google 搜索"""
    url = f"https://www.google.com/search?q={query}"
    return {"source": "google", "url": url}

def search_concept(query, priority="wikipedia"):
    """
    搜索概念

    Args:
        query: 搜索关键词
        priority: 优先搜索源 (wikipedia/mdn/google)

    Returns:
        dict: 搜索结果
    """
    results = {
        "query": query,
        "priority_source": priority,
        "sources": []
    }

    # 根据优先级确定搜索顺序
    search_order = []
    if priority == "wikipedia":
        search_order = ["wikipedia", "mdn", "google"]
    elif priority == "mdn":
        search_order = ["mdn", "wikipedia", "google"]
    else:
        search_order = ["google", "wikipedia", "mdn"]

    for source in search_order:
        if source == "wikipedia":
            results["sources"].append(search_wikipedia(query))
        elif source == "mdn":
            results["sources"].append(search_mdn(query))
        elif source == "google":
            results["sources"].append(search_google(query))

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [priority]")
        sys.exit(1)

    query = sys.argv[1]
    priority = sys.argv[2] if len(sys.argv) > 2 else "wikipedia"

    result = search_concept(query, priority)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
