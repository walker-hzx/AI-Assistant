#!/usr/bin/env python3
"""
报告生成器
从爬取的内容生成结构化报告

功能：
- 自动生成摘要
- 提取关键信息
- 生成目录结构
- 整理页面关系
"""

import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class PageSummary:
    """页面摘要"""
    url: str
    title: str
    summary: str
    word_count: int
    code_blocks: int
    tables: int
    links: int
    key_topics: List[str]


class ReportGenerator:
    """报告生成器"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url
        self.pages: List[Dict] = []

    def add_page(self, page_data: Dict):
        """添加页面"""
        self.pages.append(page_data)

    def generate_summary(self) -> str:
        """生成总体摘要"""
        total_pages = len(self.pages)
        total_words = sum(p.get('word_count', 0) for p in self.pages)
        total_code = sum(p.get('code_blocks', 0) for p in self.pages)
        total_tables = sum(p.get('tables', 0) for p in self.pages)

        summary = f"# 网站爬取报告\n\n"
        summary += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        if self.base_url:
            summary += f"**入口 URL**: {self.base_url}\n\n"

        summary += f"## 统计信息\n\n"
        summary += f"- 页面总数: {total_pages}\n"
        summary += f"- 总字数: {total_words:,}\n"
        summary += f"- 代码块: {total_code}\n"
        summary += f"- 表格: {total_tables}\n\n"

        return summary

    def generate_toc(self) -> str:
        """生成目录"""
        toc = "## 目录\n\n"

        # 按标题组织
        headings_map = {}
        for page in self.pages:
            url = page.get('url', '')
            headings = page.get('headings', [])

            if headings:
                # 取第一个一级标题作为分类
                first_h1 = next((h for h in headings if h.get('level') == 1), None)
                if first_h1:
                    category = first_h1.get('text', '未分类')
                else:
                    category = '未分类'

                if category not in headings_map:
                    headings_map[category] = []

                headings_map[category].append({
                    'title': page.get('title', 'Untitled'),
                    'url': url,
                    'headings': headings[:5]  # 只取前5个标题
                })

        # 生成目录
        for category, pages in headings_map.items():
            toc += f"### {category}\n\n"
            for p in pages[:10]:
                # 提取标题中的锚点
                if p['headings']:
                    anchor = p['headings'][0].get('text', '').lower().replace(' ', '-')
                    url = f"{p['url']}#{anchor}"
                else:
                    url = p['url']
                toc += f"- [{p['title']}]({url})\n"
            toc += "\n"

        return toc

    def generate_page_list(self) -> str:
        """生成页面列表"""
        page_list = "## 页面列表\n\n"

        # 按字数排序
        sorted_pages = sorted(
            self.pages,
            key=lambda x: x.get('word_count', 0),
            reverse=True
        )

        for i, page in enumerate(sorted_pages, 1):
            title = page.get('title', 'Untitled')
            url = page.get('url', '')
            word_count = page.get('word_count', 0)
            code_blocks = page.get('code_blocks', 0)
            summary = page.get('summary', '')[:100]

            page_list += f"### {i}. {title}\n\n"
            page_list += f"- URL: {url}\n"
            page_list += f"- 字数: {word_count:,}\n"
            page_list += f"- 代码块: {code_blocks}\n"
            page_list += f"- 摘要: {summary}...\n\n"

        return page_list

    def generate_key_topics(self) -> str:
        """生成关键主题"""
        topics_text = "## 关键主题\n\n"

        # 收集所有标题
        all_headings = []
        for page in self.pages:
            headings = page.get('headings', [])
            for h in headings:
                if h.get('level', 0) <= 2:  # 只取一级和二级标题
                    all_headings.append(h.get('text', ''))

        # 统计主题频率
        topic_counts = {}
        for heading in all_headings:
            # 简化标题
            topic = heading.lower().strip()
            if len(topic) > 3:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1

        # 获取最常见的主题
        top_topics = sorted(topic_counts.items(), key=lambda x: -x[1])[:20]

        for topic, count in top_topics:
            topics_text += f"- **{topic}** (出现 {count} 次)\n"

        return topics_text + "\n"

    def generate_code_summary(self) -> str:
        """生成代码汇总"""
        code_summary = "## 代码汇总\n\n"

        # 按语言分组
        languages = {}
        for page in self.pages:
            code_blocks = page.get('code_blocks_detail', [])
            for block in code_blocks:
                lang = block.get('language', 'text')
                if lang not in languages:
                    languages[lang] = {
                        'count': 0,
                        'pages': []
                    }
                languages[lang]['count'] += 1
                languages[lang]['pages'].append(page.get('title', ''))

        if not languages:
            return ""

        for lang, info in sorted(languages.items(), key=lambda x: -x[1]['count']):
            code_summary += f"### {lang}\n\n"
            code_summary += f"- 数量: {info['count']} 个代码块\n"
            code_summary += f"- 出现在: {', '.join(info['pages'][:5])}\n\n"

        return code_summary

    def generate_api_summary(self) -> str:
        """生成 API 汇总"""
        api_summary = "## API 参考\n\n"

        all_apis = []
        for page in self.pages:
            apis = page.get('apis', [])
            for api in apis:
                api['page_title'] = page.get('title', '')
                all_apis.append(api)

        if not all_apis:
            return ""

        # 按类型分组
        by_type = {}
        for api in all_apis:
            api_type = api.get('type', 'unknown')
            if api_type not in by_type:
                by_type[api_type] = []
            by_type[api_type].append(api)

        for api_type, apis in sorted(by_type.items()):
            api_summary += f"### {api_type}\n\n"
            api_summary += f"共 {len(apis)} 个定义\n\n"

            for api in apis[:10]:
                name = api.get('name', '')
                params = api.get('params', [])
                page_title = api.get('page_title', '')

                if name:
                    api_summary += f"- **{name}**"
                    if params:
                        param_names = [p.get('name', '') for p in params[:3]]
                        api_summary += f"({', '.join(param_names)})"
                    api_summary += f" - {page_title}\n"
                elif params:
                    # 没有名称的参数列表
                    for p in params[:5]:
                        api_summary += f"- {p.get('name', '')}: {p.get('description', '')}\n"

            api_summary += "\n"

        return api_summary

    def generate_full_report(self) -> str:
        """生成完整报告"""
        report = self.generate_summary()
        report += self.generate_toc()
        report += self.generate_key_topics()
        report += self.generate_code_summary()
        report += self.generate_api_summary()
        report += self.generate_page_list()

        return report

    def to_json(self) -> Dict:
        """转换为 JSON"""
        return {
            'base_url': self.base_url,
            'generated_at': datetime.now().isoformat(),
            'stats': {
                'total_pages': len(self.pages),
                'total_words': sum(p.get('word_count', 0) for p in self.pages),
                'total_code_blocks': sum(p.get('code_blocks', 0) for p in self.pages),
            },
            'pages': self.pages
        }


def generate_from_crawl_results(results_file: str, output_file: str = None) -> str:
    """从爬取结果生成报告"""
    # 加载结果
    with open(results_file, 'r') as f:
        data = json.load(f)

    # 如果是列表格式
    if isinstance(data, list):
        pages = data
    elif isinstance(data, dict) and 'pages' in data:
        pages = data['pages']
        base_url = data.get('base_url', '')
    else:
        pages = [data]
        base_url = ''

    # 创建报告生成器
    generator = ReportGenerator(base_url)

    # 添加页面
    for page in pages:
        if isinstance(page, dict):
            result = page.get('result', {})

            # 提取标题
            title = result.get('title', 'Untitled')

            # 提取内容
            content = result.get('content', '')

            # 基本统计
            word_count = len(content)
            code_blocks = content.count('```')
            links = len(result.get('links', []))

            # 简单摘要
            summary = ' '.join(content.split()[:50])

            generator.add_page({
                'url': page.get('url', ''),
                'title': title,
                'content': content,
                'word_count': word_count,
                'code_blocks': code_blocks // 2,  # 每个代码块有两个 ```
                'tables': 0,
                'links': links,
                'summary': summary,
                'headings': [],  # 可以进一步解析
                'apis': [],  # 可以进一步解析
            })

    # 生成报告
    report = generator.generate_full_report()

    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"报告已保存到: {output_file}")

    return report


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='报告生成器')
    parser.add_argument('results', help='爬取结果文件 (JSON)')
    parser.add_argument('-o', '--output', help='输出文件')

    args = parser.parse_args()

    report = generate_from_crawl_results(args.results, args.output)

    if not args.output:
        print(report)
