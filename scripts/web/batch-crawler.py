#!/usr/bin/env python3
"""
批量爬取器
支持从文件或 URL 模式批量爬取多个页面

功能：
- 从文件读取 URL 列表
- 从 URL 模式批量生成 URL
- 并发爬取
- 进度显示
"""

import argparse
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from fetch_url import retry_fetch, normalize_url, is_same_domain


class BatchCrawler:
    """批量爬取器"""

    def __init__(self,
                 concurrency: int = 3,
                 wait_time: int = 5,
                 max_retries: int = 3,
                 output_dir: str = None):
        self.concurrency = concurrency
        self.wait_time = wait_time
        self.max_retries = max_retries
        self.output_dir = Path(output_dir) if output_dir else None

        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results: List[Dict] = []
        self.failed: List[Dict] = []

    def load_urls_from_file(self, filepath: str) -> List[str]:
        """从文件加载 URL"""
        urls = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if line and not line.startswith('#'):
                    urls.append(line)
        return urls

    def generate_urls_from_pattern(self,
                                   base_url: str,
                                   pattern: str,
                                   values: List[str]) -> List[str]:
        """从模式生成 URL"""
        urls = []
        for value in values:
            url = pattern.replace('{value}', value).replace('{slug}', value)
            urls.append(url)
        return urls

    def crawl_url(self, url: str) -> Dict:
        """爬取单个 URL"""
        start_time = time.time()

        result = retry_fetch(url, self.wait_time, self.max_retries)

        elapsed = time.time() - start_time

        if result:
            return {
                'url': url,
                'success': True,
                'title': result.get('title', ''),
                'content_length': len(result.get('content', '')),
                'elapsed': elapsed,
                'result': result
            }
        else:
            return {
                'url': url,
                'success': False,
                'elapsed': elapsed,
                'error': 'Failed to fetch'
            }

    def crawl(self, urls: List[str], show_progress: bool = True) -> List[Dict]:
        """批量爬取"""
        total = len(urls)
        completed = 0
        results = []

        print(f"\n开始批量爬取: {total} 个 URL")
        print(f"并发数: {self.concurrency}")
        print(f"重试次数: {self.max_retries}")
        print("-" * 50)

        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            future_to_url = {
                executor.submit(self.crawl_url, url): url
                for url in urls
            }

            for future in as_completed(future_to_url):
                completed += 1

                try:
                    result = future.result()
                    results.append(result)

                    if result['success']:
                        if show_progress:
                            print(f"[{completed}/{total}] ✓ {result.get('title', result['url'])[:40]}")
                    else:
                        if show_progress:
                            print(f"[{completed}/{total}] ✗ {result['url'][:50]}")

                except Exception as e:
                    url = future_to_url[future]
                    results.append({
                        'url': url,
                        'success': False,
                        'error': str(e)
                    })
                    if show_progress:
                        print(f"[{completed}/{total}] ✗ {url[:50]} - Error: {e}")

        self.results = [r for r in results if r['success']]
        self.failed = [r for r in results if not r['success']]

        return results

    def save_results(self, prefix: str = "crawl") -> Dict:
        """保存结果"""
        if not self.output_dir:
            return {}

        # 保存成功的结果
        success_file = self.output_dir / f"{prefix}-success.json"
        with open(success_file, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # 保存失败的结果
        failed_file = self.output_dir / f"{prefix}-failed.json"
        with open(failed_file, 'w') as f:
            json.dump(self.failed, f, indent=2, ensure_ascii=False)

        # 保存 Markdown 文件
        md_file = self.output_dir / f"{prefix}.md"
        with open(md_file, 'w') as f:
            f.write(f"# 爬取结果\n\n")
            f.write(f"**成功**: {len(self.results)}\n")
            f.write(f"**失败**: {len(self.failed)}\n\n")
            f.write("---\n\n")

            for i, result in enumerate(self.results, 1):
                f.write(f"## {i}. {result.get('title', 'Untitled')}\n\n")
                f.write(f"**URL**: {result['url']}\n\n")
                content = result.get('result', {}).get('content', '')
                # 限制长度
                if len(content) > 2000:
                    content = content[:2000] + "\n\n... (truncated)"
                f.write(content)
                f.write("\n\n---\n\n")

        print(f"\n结果已保存到: {self.output_dir}")
        print(f"  - {success_file}")
        print(f"  - {failed_file}")
        print(f"  - {md_file}")

        return {
            'success_file': str(success_file),
            'failed_file': str(failed_file),
            'md_file': str(md_file)
        }

    def get_summary(self) -> Dict:
        """获取摘要"""
        total = len(self.results) + len(self.failed)
        success_rate = len(self.results) / total * 100 if total > 0 else 0

        avg_time = sum(r['elapsed'] for r in self.results) / len(self.results) if self.results else 0

        return {
            'total': total,
            'success': len(self.results),
            'failed': len(self.failed),
            'success_rate': f"{success_rate:.1f}%",
            'avg_time': f"{avg_time:.2f}s"
        }


def crawl_from_file(filepath: str,
                    output_dir: str = None,
                    concurrency: int = 3,
                    wait_time: int = 5):
    """从文件批量爬取"""
    crawler = BatchCrawler(
        concurrency=concurrency,
        wait_time=wait_time,
        output_dir=output_dir
    )

    urls = crawler.load_urls_from_file(filepath)
    print(f"加载了 {len(urls)} 个 URL")

    results = crawler.crawl(urls)

    summary = crawler.get_summary()
    print(f"\n{'='*50}")
    print(f"爬取完成!")
    print(f"成功: {summary['success']}/{summary['total']} ({summary['success_rate']})")
    print(f"平均耗时: {summary['avg_time']}")
    print(f"{'='*50}")

    if output_dir:
        crawler.save_results(Path(filepath).stem)

    return crawler


def crawl_from_pattern(base_url: str,
                       pattern: str,
                       values: List[str],
                       output_dir: str = None,
                       concurrency: int = 3):
    """从模式批量爬取"""
    crawler = BatchCrawler(
        concurrency=concurrency,
        output_dir=output_dir
    )

    urls = crawler.generate_urls_from_pattern(base_url, pattern, values)
    print(f"生成了 {len(urls)} 个 URL")

    results = crawler.crawl(urls)

    summary = crawler.get_summary()
    print(f"\n爬取完成: {summary['success']}/{summary['total']} 成功")

    if output_dir:
        crawler.save_results("pattern-crawl")

    return crawler


def main():
    parser = argparse.ArgumentParser(description='批量爬取工具')
    parser.add_argument('-f', '--file', help='URL 列表文件')
    parser.add_argument('-u', '--url', help='单个 URL（可多次使用）', action='append')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-c', '--concurrency', type=int, default=3, help='并发数')
    parser.add_argument('-w', '--wait', type=int, default=5, help='等待秒数')
    parser.add_argument('-r', '--retries', type=int, default=3, help='重试次数')

    args = parser.parse_args()

    urls = []

    if args.file:
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if args.url:
        urls.extend(args.url)

    if not urls:
        parser.print_help()
        sys.exit(1)

    crawler = BatchCrawler(
        concurrency=args.concurrency,
        wait_time=args.wait,
        max_retries=args.retries,
        output_dir=args.output
    )

    results = crawler.crawl(urls)

    summary = crawler.get_summary()

    print(f"\n{'='*50}")
    print(f"爬取完成!")
    print(f"成功: {summary['success']}/{summary['total']} ({summary['success_rate']})")
    print(f"平均耗时: {summary['avg_time']}")
    print(f"{'='*50}")

    if args.output:
        crawler.save_results("batch")


if __name__ == "__main__":
    main()
