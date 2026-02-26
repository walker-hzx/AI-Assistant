#!/usr/bin/env python3
"""
URL 模式分析器
自动分析 URL 列表，发现 URL 规律，识别模块边界

功能：
- 从 URL 列表中发现模式
- 识别模块边界
- 生成 URL 模板
- 推断可能的 URL
"""

import re
import json
from urllib.parse import urlparse, urlunparse
from collections import defaultdict, Counter
from typing import List, Dict, Set, Optional


class URLPatternAnalyzer:
    """URL 模式分析器"""

    def __init__(self, urls: List[str]):
        self.urls = urls
        self.parsed = [urlparse(u) for u in urls]
        self.base_domain = self._get_base_domain()

    def _get_base_domain(self) -> str:
        """获取基础域名"""
        if not self.parsed:
            return ""
        domains = [p.netloc for p in self.parsed]
        # 返回最常见的域名
        return Counter(domains).most_common(1)[0][0]

    def analyze_path_structure(self) -> Dict:
        """分析路径结构"""
        paths = [p.path for p in self.parsed if p.path]

        # 提取路径层级
        levels = []
        for path in paths:
            parts = [p for p in path.split('/') if p]
            levels.append(len(parts))

        # 统计路径前缀
        prefixes = defaultdict(int)
        for path in paths:
            parts = path.split('/')
            if len(parts) >= 2:
                # 提取到第二级
                prefix = '/'.join(parts[:2])
                prefixes[prefix] += 1
            elif len(parts) == 1:
                prefixes['/' + parts[0]] += 1

        return {
            'total_urls': len(self.urls),
            'path_count': len(set(paths)),
            'avg_depth': sum(levels) / len(levels) if levels else 0,
            'min_depth': min(levels) if levels else 0,
            'max_depth': max(levels) if levels else 0,
            'common_prefixes': dict(Counter(prefixes).most_common(10))
        }

    def identify_modules(self) -> List[Dict]:
        """识别模块"""
        # 按第一级路径分组
        modules = defaultdict(list)

        for url, parsed in zip(self.urls, self.parsed):
            path = parsed.path
            parts = [p for p in path.split('/') if p]

            if parts:
                module = parts[0]
                modules[module].append({
                    'url': url,
                    'path': path,
                    'depth': len(parts)
                })

        # 转换为列表并排序
        result = []
        for name, pages in modules.items():
            result.append({
                'name': name,
                'path': '/' + name,
                'page_count': len(pages),
                'pages': sorted(pages, key=lambda x: x['path'])
            })

        return sorted(result, key=lambda x: -x['page_count'])

    def extract_patterns(self) -> List[Dict]:
        """提取 URL 模式"""
        patterns = []
        paths = [p.path for p in self.parsed if p.path]

        # 查找带变量的路径模式
        # 例如: /docs/components/button -> /docs/components/{name}
        variable_pattern = re.compile(r'/([^/]+)')

        for path in paths:
            parts = [p for p in path.split('/') if p]

            # 生成模式（替换变量）
            pattern_parts = []
            for i, part in enumerate(parts):
                # 检查是否是数字
                if part.isdigit():
                    pattern_parts.append('{id}')
                # 检查是否是日期
                elif re.match(r'^\d{4}-\d{2}-\d{2}$', part):
                    pattern_parts.append('{date}')
                # 检查是否是 UUID
                elif re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}', part):
                    pattern_parts.append('{uuid}')
                else:
                    pattern_parts.append(part)

            pattern = '/' + '/'.join(pattern_parts)
            patterns.append(pattern)

        # 统计模式频率
        pattern_counts = Counter(patterns)

        # 返回去重后的模式
        unique_patterns = []
        seen = set()
        for p in patterns:
            if p not in seen:
                seen.add(p)
                unique_patterns.append({
                    'pattern': p,
                    'count': pattern_counts[p]
                })

        return sorted(unique_patterns, key=lambda x: -x['count'])

    def generate_url_templates(self) -> List[str]:
        """生成 URL 模板"""
        templates = set()

        for parsed in self.parsed:
            path = parsed.path
            parts = [p for p in path.split('/') if p]

            # 生成几种模板
            # 1. 只保留模块名
            if len(parts) >= 1:
                templates.add(f"{parsed.scheme}://{parsed.netloc}/{parts[0]}/")

            # 2. 保留两级
            if len(parts) >= 2:
                templates.add(f"{parsed.scheme}://{parsed.netloc}/{parts[0]}/{parts[1]}/")

            # 3. 变量模板
            if len(parts) >= 3:
                var_parts = parts[:2] + ['{slug}']
                templates.add(f"{parsed.scheme}://{parsed.netloc}/" + '/'.join(var_parts) + '/')

        return sorted(templates)

    def infer_possible_urls(self, limit: int = 20) -> List[str]:
        """推断可能的 URL"""
        possible = set()

        # 从模式中推断
        patterns = self.extract_patterns()

        # 获取所有唯一的路径部分
        all_parts = []
        for parsed in self.parsed:
            parts = [p for p in parsed.path.split('/') if p]
            all_parts.extend(parts)

        # 统计各层级最常见的部分
        part_counts = Counter(all_parts)

        # 生成可能的 URL
        for pattern in patterns[:5]:
            parts = pattern['pattern'].split('/')
            # 替换变量为最常见的值
            if '{id}' in pattern['pattern'] or '{slug}' in pattern['pattern']:
                most_common = part_counts.most_common(5)
                for part, _ in most_common:
                    if part.isdigit() or len(part) > 3:
                        new_path = pattern['pattern'].replace('{id}', part).replace('{slug}', part)
                        url = urlunparse((
                            'https',
                            self.base_domain,
                            new_path,
                            '', '', ''
                        ))
                        possible.add(url)
                        if len(possible) >= limit:
                            break
            if len(possible) >= limit:
                break

        return sorted(possible)[:limit]

    def get_module_tree(self) -> Dict:
        """获取模块树形结构"""
        tree = {
            'domain': self.base_domain,
            'modules': {}
        }

        # 按层级组织
        for url, parsed in zip(self.urls, self.parsed):
            path = parsed.path
            parts = [p for p in path.split('/') if p]

            current = tree['modules']
            for i, part in enumerate(parts):
                if part not in current:
                    current[part] = {
                        '_meta': {
                            'path': '/' + '/'.join(parts[:i+1]),
                            'depth': i + 1,
                            'urls': []
                        },
                        '_children': {}
                    }

                if i == len(parts) - 1:
                    current[part]['_meta']['urls'].append(url)

                current = current[part].get('_children', {})

        return tree

    def analyze(self) -> Dict:
        """完整分析"""
        return {
            'base_domain': self.base_domain,
            'path_structure': self.analyze_path_structure(),
            'modules': self.identify_modules(),
            'patterns': self.extract_patterns(),
            'templates': self.generate_url_templates(),
            'possible_urls': self.infer_possible_urls(),
            'module_tree': self.get_module_tree()
        }

    def to_markdown(self) -> str:
        """生成 Markdown 格式报告"""
        analysis = self.analyze()

        md = f"# URL 模式分析报告\n\n"
        md += f"**基础域名**: {analysis['base_domain']}\n"
        md += f"**URL 总数**: {analysis['path_structure']['total_urls']}\n\n"

        md += "## 路径结构\n\n"
        md += f"- 平均深度: {analysis['path_structure']['avg_depth']:.1f}\n"
        md += f"- 深度范围: {analysis['path_structure']['min_depth']} - {analysis['path_structure']['max_depth']}\n\n"

        md += "## 识别到的模块\n\n"
        for module in analysis['modules']:
            md += f"### /{module['name']}\n\n"
            md += f"- 页面数: {module['page_count']}\n"
            md += f"- 路径: {module['path']}\n"
            md += f"- 页面:\n"
            for page in module['pages'][:5]:
                md += f"  - [{page['path']}]({page['url']})\n"
            if len(module['pages']) > 5:
                md += f"  - ... 还有 {len(module['pages']) - 5} 个页面\n"
            md += "\n"

        md += "## URL 模式\n\n"
        for pattern in analysis['patterns'][:10]:
            md += f"- `{pattern['pattern']}` ({pattern['count']} 个)\n"

        md += "\n## URL 模板\n\n"
        for template in analysis['templates'][:5]:
            md += f"- {template}\n"

        md += "\n## 可能的其他页面\n\n"
        for url in analysis['possible_urls'][:10]:
            md += f"- {url}\n"

        return md


def analyze_from_file(filepath: str) -> str:
    """从文件分析 URL"""
    with open(filepath, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    analyzer = URLPatternAnalyzer(urls)
    return analyzer.to_markdown()


def analyze_urls(urls: List[str]) -> Dict:
    """分析 URL 列表"""
    analyzer = URLPatternAnalyzer(urls)
    return analyzer.analyze()


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='URL 模式分析器')
    parser.add_argument('urls', nargs='*', help='URL 列表')
    parser.add_argument('-f', '--file', help='从文件读取 URL')
    parser.add_argument('-o', '--output', help='输出文件')
    parser.add_argument('-j', '--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()

    if args.file:
        urls = []
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    elif args.urls:
        urls = args.urls
    else:
        print("请提供 URL 或文件")
        sys.exit(1)

    analyzer = URLPatternAnalyzer(urls)

    if args.json:
        result = analyzer.analyze()
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = analyzer.to_markdown()

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"已保存到: {args.output}")
    else:
        print(output)
