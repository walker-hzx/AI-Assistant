#!/usr/bin/env python3
"""
网页内容爬取脚本
使用 Playwright 解决跨域和动态内容问题
"""

import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def clean_text(text: str) -> str:
    """清理文本，移除多余空白"""
    lines = text.split('\n')
    cleaned = []
    prev_empty = False

    for line in lines:
        line = line.strip()
        if line:
            cleaned.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned.append('')
            prev_empty = True

    return '\n'.join(cleaned)


def extract_main_content(page) -> str:
    """提取页面主要内容"""

    # 尝试多种选择器，提取主要内容区域
    selectors = [
        'main',
        'article',
        '.content',
        '.main-content',
        '#content',
        '.docs-content',
        '.documentation',
        'body'
    ]

    content = None
    for selector in selectors:
        try:
            element = page.locator(selector).first
            if element.count() > 0:
                content = element.inner_text()
                if len(content) > 500:  # 确保内容足够多
                    break
        except:
            continue

    if not content:
        # 最后尝试获取整个 body
        content = page.locator('body').inner_text()

    return clean_text(content)


def fetch_url(url: str, wait_time: int = 5, output: str = None) -> str:
    """获取 URL 内容"""

    print(f"正在访问: {url}")

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 访问页面
            response = page.goto(url, wait_until='domcontentloaded', timeout=30000)

            if response is None:
                print("错误: 无法获取页面")
                return None

            if response.status >= 400:
                print(f"错误: HTTP {response.status}")
                return None

            print(f"页面加载成功，状态码: {response.status}")

            # 等待额外时间让动态内容加载
            if wait_time > 0:
                print(f"等待 {wait_time} 秒让动态内容加载...")
                page.wait_for_timeout(wait_time * 1000)

            # 获取页面标题
            title = page.title()
            print(f"页面标题: {title}")

            # 提取主要内容
            content = extract_main_content(page)

            if not content or len(content) < 100:
                print("警告: 页面内容可能为空或太少")
                return None

            print(f"获取到内容: {len(content)} 字符")

            # 构建输出
            result = f"# {title}\n\n"
            result += f"**来源**: {url}\n\n"
            result += "---\n\n"
            result += content

            # 保存或输出
            if output:
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(result, encoding='utf-8')
                print(f"内容已保存到: {output}")
            else:
                print("\n" + "="*50)
                print(result)
                print("="*50)

            return result

        except Exception as e:
            print(f"错误: {e}")
            return None
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description='网页内容爬取工具')
    parser.add_argument('url', help='要爬取的 URL')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-w', '--wait', type=int, default=5,
                        help='等待页面渲染的秒数 (默认: 5)')

    args = parser.parse_args()

    # 验证 URL
    if not args.url.startswith(('http://', 'https://')):
        print("错误: URL 必须以 http:// 或 https:// 开头")
        sys.exit(1)

    result = fetch_url(args.url, args.wait, args.output)

    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
