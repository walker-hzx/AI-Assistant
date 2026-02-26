#!/usr/bin/env python3
"""
网页内容爬取脚本
使用 Playwright 解决跨域和动态内容问题

支持功能：
- 单页爬取
- 整站爬取（链接发现）
- 深度控制
- 并发爬取
- 错误重试
"""

import argparse
import sys
import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
from collections import deque
from typing import Set, List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import time


# ============ 配置 ============

DEFAULT_CONCURRENCY = 3  # 默认并发数
DEFAULT_DEPTH = 2  # 默认爬取深度
DEFAULT_RETRY = 3  # 默认重试次数
DEFAULT_WAIT = 5  # 默认等待秒数


# ============ 工具函数 ============

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


def normalize_url(url: str, base_url: str = None) -> Optional[str]:
    """URL 归一化：去除锚点、查询参数等"""
    try:
        parsed = urlparse(url)

        # 过滤 javascript:、mailto: 等
        if parsed.scheme and parsed.scheme not in ('http', 'https'):
            return None

        # 去除锚点和查询参数
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            '',  # params
            '',  # query
            ''   # fragment
        ))

        return normalized if normalized else None
    except:
        return None


def is_same_domain(url: str, base_url: str) -> bool:
    """检查 URL 是否与基 URL 同域"""
    try:
        parsed_url = urlparse(url)
        parsed_base = urlparse(base_url)

        # 同域名或子域名
        return parsed_url.netloc == parsed_base.netloc or \
               parsed_url.netloc.endswith('.' + parsed_base.netloc)
    except:
        return False


def is_valid_path(url: str) -> bool:
    """检查 URL 路径是否有效（排除文件下载链接等）"""
    try:
        parsed = urlparse(url)
        path = parsed.path.lower()

        # 排除常见文件类型
        excluded_extensions = ('.pdf', '.zip', '.tar', '.gz', '.rar',
                             '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                             '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
                             '.mp3', '.mp4', '.avi', '.mov', '.woff', '.woff2', '.ttf')

        return not any(path.endswith(ext) for ext in excluded_extensions)
    except:
        return False


# ============ 核心功能 ============

def extract_main_content(page) -> str:
    """提取页面主要内容"""
    selectors = [
        'main', 'article', '.content', '.main-content', '#content',
        '.docs-content', '.documentation', '.prose', 'body'
    ]

    content = None
    for selector in selectors:
        try:
            element = page.locator(selector).first
            if element.count() > 0:
                content = element.inner_text()
                if len(content) > 500:
                    break
        except:
            continue

    if not content:
        content = page.locator('body').inner_text()

    return clean_text(content)


def extract_links(page, base_url: str) -> Set[str]:
    """从页面提取所有相关链接"""
    links = set()

    try:
        # 获取所有 a 标签的 href
        anchor_elements = page.locator('a[href]')

        for i in range(anchor_elements.count()):
            try:
                href = anchor_elements.nth(i).get_attribute('href')
                if not href:
                    continue

                # 跳过锚点链接
                if href.startswith('#'):
                    continue

                # 处理相对路径
                full_url = urljoin(base_url, href)
                normalized = normalize_url(full_url)

                if normalized and is_same_domain(normalized, base_url) and is_valid_path(normalized):
                    links.add(normalized)
            except:
                continue
    except Exception as e:
        print(f"提取链接时出错: {e}")

    return links


def fetch_single_url(url: str, wait_time: int = 5, browser=None) -> Optional[Dict]:
    """获取单个 URL 的内容"""

    if browser is None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            result = _fetch_page(page, url, wait_time)
            browser.close()
            return result
    else:
        context = browser.new_context()
        page = context.new_page()
        result = _fetch_page(page, url, wait_time)
        context.close()
        return result


def _fetch_page(page: Page, url: str, wait_time: int) -> Optional[Dict]:
    """内部方法：爬取单个页面"""
    try:
        print(f"正在访问: {url}")

        response = page.goto(url, wait_until='domcontentloaded', timeout=30000)

        if response is None:
            print(f"错误: 无法获取页面 {url}")
            return None

        if response.status >= 400:
            print(f"错误: HTTP {response.status} - {url}")
            return None

        # 等待动态内容加载
        if wait_time > 0:
            page.wait_for_timeout(wait_time * 1000)

        title = page.title()
        content = extract_main_content(page)

        if not content or len(content) < 100:
            print(f"警告: 页面内容可能为空 - {url}")
            return None

        # 提取页面链接
        base_url = url
        links = extract_links(page, base_url)

        print(f"✓ 成功获取: {title} ({len(content)} 字符, {len(links)} 个链接)")

        return {
            'url': url,
            'title': title,
            'content': content,
            'links': links,
            'status': response.status
        }

    except Exception as e:
        print(f"错误: {e} - {url}")
        return None


def retry_fetch(url: str, wait_time: int = 5, max_retries: int = DEFAULT_RETRY) -> Optional[Dict]:
    """带重试的爬取"""
    for attempt in range(max_retries):
        try:
            result = fetch_single_url(url, wait_time)
            if result:
                return result

            if attempt < max_retries - 1:
                print(f"重试 {attempt + 1}/{max_retries}...")
                time.sleep(2 ** attempt)  # 指数退避
        except Exception as e:
            print(f"爬取失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

    return None


# ============ 站点爬取器 ============

class SiteCrawler:
    """站点爬取器"""

    def __init__(self,
                 base_url: str,
                 max_depth: int = DEFAULT_DEPTH,
                 max_pages: int = 50,
                 concurrency: int = DEFAULT_CONCURRENCY,
                 wait_time: int = DEFAULT_WAIT):
        self.base_url = base_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.concurrency = concurrency
        self.wait_time = wait_time

        self.visited: Set[str] = set()
        self.results: List[Dict] = []
        self.pending: deque = deque()  # (url, depth)

    def should_crawl(self, url: str, depth: int) -> bool:
        """判断是否应该爬取该 URL"""
        if depth > self.max_depth:
            return False
        if len(self.visited) >= self.max_pages:
            return False
        if url in self.visited:
            return False
        if not is_same_domain(url, self.base_url):
            return False
        return True

    def crawl(self) -> List[Dict]:
        """执行站点爬取"""
        print(f"\n{'='*50}")
        print(f"开始站点爬取")
        print(f"入口: {self.base_url}")
        print(f"最大深度: {self.max_depth}")
        print(f"最大页面数: {self.max_pages}")
        print(f"并发数: {self.concurrency}")
        print(f"{'='*50}\n")

        # 初始化队列
        self.pending.append((self.base_url, 0))

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            while self.pending and len(self.visited) < self.max_pages:
                # 批处理：每次处理一批
                batch = []
                while self.pending and len(batch) < self.concurrency:
                    batch.append(self.pending.popleft())

                if not batch:
                    break

                print(f"\n[批次] 处理 {len(batch)} 个页面...")

                # 并发爬取
                for url, depth in batch:
                    if not self.should_crawl(url, depth):
                        continue

                    self.visited.add(url)

                    # 串行爬取（避免被封）
                    result = fetch_single_url(url, self.wait_time, browser)

                    if result:
                        self.results.append(result)

                        # 添加新发现的链接到队列
                        if depth < self.max_depth:
                            for link in result.get('links', []):
                                if self.should_crawl(link, depth + 1):
                                    self.pending.append((link, depth + 1))

                print(f"[进度] 已爬取: {len(self.visited)}, 待处理: {len(self.pending)}")

            browser.close()

        return self.results

    def get_sitemap(self) -> Dict:
        """生成简单的站点结构"""
        sitemap = {
            'base_url': self.base_url,
            'total_pages': len(self.results),
            'pages': []
        }

        for result in self.results:
            sitemap['pages'].append({
                'url': result['url'],
                'title': result['title'],
                'links_count': len(result.get('links', []))
            })

        return sitemap


# ============ 主函数 ============

def crawl_single(url: str, output: str = None, wait: int = DEFAULT_WAIT):
    """单页爬取模式"""
    print(f"模式: 单页爬取")
    print(f"目标: {url}\n")

    result = retry_fetch(url, wait)

    if result:
        content = f"# {result['title']}\n\n"
        content += f"**来源**: {result['url']}\n\n"
        content += "---\n\n"
        content += result['content']

        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding='utf-8')
            print(f"\n内容已保存到: {output}")
        else:
            print("\n" + "="*50)
            print(content)
            print("="*50)
    else:
        print("爬取失败")
        sys.exit(1)


def crawl_site(url: str, output: str = None, depth: int = DEFAULT_DEPTH,
               max_pages: int = 50, concurrency: int = DEFAULT_CONCURRENCY):
    """站点爬取模式"""
    print(f"模式: 站点爬取")
    print(f"目标: {url}")
    print(f"深度: {depth}")
    print(f"最大页面: {max_pages}\n")

    crawler = SiteCrawler(
        base_url=url,
        max_depth=depth,
        max_pages=max_pages,
        concurrency=concurrency
    )

    results = crawler.crawl()

    print(f"\n{'='*50}")
    print(f"爬取完成! 共获取 {len(results)} 个页面")
    print(f"{'='*50}")

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 生成合并内容
        all_content = f"# 站点爬取结果\n\n"
        all_content += f"**入口**: {url}\n"
        all_content += f"**页面数**: {len(results)}\n\n"
        all_content += "---\n\n"

        for i, result in enumerate(results, 1):
            all_content += f"## {i}. {result['title']}\n\n"
            all_content += f"**URL**: {result['url']}\n\n"
            all_content += result['content'][:2000]  # 限制每个页面长度
            all_content += "\n\n---\n\n"

        # 同时保存站点地图
        sitemap = crawler.get_sitemap()
        sitemap_path = output_path.with_suffix('.sitemap.json')
        import json
        sitemap_path.write_text(json.dumps(sitemap, indent=2, ensure_ascii=False), encoding='utf-8')

        output_path.write_text(all_content, encoding='utf-8')
        print(f"\n内容已保存到: {output}")
        print(f"站点地图已保存到: {sitemap_path}")
    else:
        for result in results[:5]:  # 只显示前5个
            print(f"\n--- {result['title']} ---")
            print(result['content'][:500])


def main():
    parser = argparse.ArgumentParser(description='网页内容爬取工具')

    # 主参数
    parser.add_argument('url', nargs='?', help='要爬取的 URL')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-w', '--wait', type=int, default=DEFAULT_WAIT,
                        help=f'等待页面渲染的秒数 (默认: {DEFAULT_WAIT})')
    parser.add_argument('-d', '--depth', type=int, default=1,
                        help='爬取深度 (1=单页, 2+=站点)')
    parser.add_argument('-m', '--max-pages', type=int, default=50,
                        help='最大页面数 (默认: 50)')
    parser.add_argument('-c', '--concurrency', type=int, default=DEFAULT_CONCURRENCY,
                        help=f'并发数 (默认: {DEFAULT_CONCURRENCY})')
    parser.add_argument('--crawl', action='store_true',
                        help='启用站点爬取模式')

    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        sys.exit(1)

    # 根据参数决定模式
    if args.crawl or args.depth > 1:
        crawl_site(args.url, args.output, args.depth, args.max_pages, args.concurrency)
    else:
        # 单页爬取
        crawl_single(args.url, args.output, args.wait)


if __name__ == "__main__":
    main()
