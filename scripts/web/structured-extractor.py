#!/usr/bin/env python3
"""
结构化提取器
从网页内容中提取结构化数据

功能：
- 提取代码块
- 提取 API 表格
- 提取示例代码
- 提取标题层级
"""

import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ExtractedCode:
    """提取的代码"""
    language: str
    code: str
    context: str  # 代码前后的上下文


@dataclass
class ExtractedTable:
    """提取的表格"""
    headers: List[str]
    rows: List[List[str]]
    caption: str


@dataclass
class ExtractedAPI:
    """提取的 API"""
    name: str
    type: str  # props, events, methods, slots
    description: str
    params: List[Dict]


class StructuredExtractor:
    """结构化提取器"""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')

    def extract_code_blocks(self) -> List[ExtractedCode]:
        """提取代码块"""
        code_blocks = []
        in_code = False
        code_lines = []
        language = ''
        context_lines = []

        for i, line in enumerate(self.lines):
            # 检测代码块开始
            if line.strip().startswith('```'):
                if not in_code:
                    # 代码块开始
                    in_code = True
                    language = line.strip()[3:].strip() or 'text'
                    code_lines = []
                    # 获取前面的上下文
                    context_lines = self.lines[max(0, i-2):i]
                else:
                    # 代码块结束
                    in_code = False
                    if code_lines:
                        code_blocks.append(ExtractedCode(
                            language=language,
                            code='\n'.join(code_lines),
                            context='\n'.join(context_lines)
                        ))
                    language = ''
                    code_lines = []
            elif in_code:
                code_lines.append(line)

        return code_blocks

    def extract_tables(self) -> List[ExtractedTable]:
        """提取表格"""
        tables = []
        in_table = False
        headers = []
        rows = []
        caption = ''

        # 简单的 Markdown 表格检测
        table_pattern = re.compile(r'^\|.*\|$')
        separator_pattern = re.compile(r'^\|[\s\-:\|]+\|$')

        for i, line in enumerate(self.lines):
            if table_pattern.match(line):
                if not in_table:
                    # 可能开始表格
                    in_table = True
                    cells = [c.strip() for c in line.split('|')[1:-1]]
                    # 检查是否是分隔行
                    if separator_pattern.match(line):
                        continue
                    headers = cells
                    rows = []
                else:
                    cells = [c.strip() for c in line.split('|')[1:-1]]
                    rows.append(cells)
            else:
                if in_table and rows:
                    tables.append(ExtractedTable(
                        headers=headers,
                        rows=rows,
                        caption=caption
                    ))
                in_table = False
                headers = []
                rows = []
                caption = ''

        # 处理最后一个表格
        if in_table and rows:
            tables.append(ExtractedTable(
                headers=headers,
                rows=rows,
                caption=caption
            ))

        return tables

    def extract_api(self) -> List[ExtractedAPI]:
        """提取 API 信息"""
        apis = []

        # 常见的 API 标题模式
        api_patterns = [
            r'^###?\s*([Pp]rops?)\s*$',
            r'^###?\s*([Ee]vents?)\s*$',
            r'^###?\s*([Mm]ethods?)\s*$',
            r'^###?\s*([Ss]lots?)\s*$',
            r'^###?\s*([Aa]ttributes?)\s*$',
            r'^###?\s*([Pp]arameters?)\s*$',
        ]

        in_api_section = False
        current_type = ''
        current_api = None

        for i, line in enumerate(self.lines):
            matched = False

            for pattern in api_patterns:
                match = re.match(pattern, line.strip())
                if match:
                    # 保存之前的 API
                    if current_api and current_api['params']:
                        apis.append(ExtractedAPI(
                            name=current_api.get('name', ''),
                            type=current_type,
                            description=current_api.get('description', ''),
                            params=current_api['params']
                        ))

                    current_type = match.group(1).lower()
                    in_api_section = True
                    matched = True
                    current_api = {
                        'name': '',
                        'description': '',
                        'params': []
                    }
                    break

            if matched:
                continue

            # 在 API 段落中，提取参数信息
            if in_api_section:
                # 检测参数行 (如: `name` - description 或 name | type | description)
                param_match = re.match(r'`?([^`|]+)`?\s*[-|]\s*(.+)', line.strip())
                if param_match:
                    param_name = param_match.group(1).strip()
                    param_desc = param_match.group(2).strip()

                    # 尝试分离类型
                    type_match = re.match(r'(.+?)\s*\(([^)]+)\)', param_desc)
                    if type_match:
                        param_desc = type_match.group(1).strip()
                        param_type = type_match.group(2).strip()
                    else:
                        param_type = 'string'

                    current_api['params'].append({
                        'name': param_name,
                        'type': param_type,
                        'description': param_desc
                    })

                # 检测小节标题（如属性名）
                if line.strip().startswith('####'):
                    current_api['name'] = line.strip().replace('####', '').strip()
                elif line.strip().startswith('**') and ':' in line:
                    # 检测到新属性
                    name_match = re.match(r'\*\*([^*]+)\*\*[:\s]*(.+)', line.strip())
                    if name_match:
                        current_api['params'].append({
                            'name': name_match.group(1).strip(),
                            'type': 'string',
                            'description': name_match.group(2).strip()
                        })

        # 保存最后一个
        if current_api and current_api['params']:
            apis.append(ExtractedAPI(
                name=current_api.get('name', ''),
                type=current_type,
                description=current_api.get('description', ''),
                params=current_api['params']
            ))

        return apis

    def extract_headings(self) -> List[Dict]:
        """提取标题层级"""
        headings = []

        for i, line in enumerate(self.lines):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': text,
                    'line': i + 1
                })

        return headings

    def extract_links(self) -> List[Dict]:
        """提取链接"""
        links = []

        # Markdown 链接模式: [text](url)
        md_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

        for line in self.lines:
            for match in md_pattern.finditer(line):
                links.append({
                    'text': match.group(1),
                    'url': match.group(2)
                })

        return links

    def extract_summary(self, max_length: int = 500) -> str:
        """提取摘要"""
        # 获取前几段非空内容
        paragraphs = []
        current = []

        for line in self.lines:
            line = line.strip()
            if line:
                current.append(line)
            else:
                if current:
                    paragraphs.append(' '.join(current))
                    current = []

        if current:
            paragraphs.append(' '.join(current))

        # 合并并截断
        summary = ' '.join(paragraphs[:3])
        if len(summary) > max_length:
            summary = summary[:max_length] + '...'

        return summary

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'code_blocks': [asdict(c) for c in self.extract_code_blocks()],
            'tables': [asdict(t) for t in self.extract_tables()],
            'apis': [asdict(a) for a in self.extract_api()],
            'headings': self.extract_headings(),
            'links': self.extract_links(),
            'summary': self.extract_summary()
        }

    def to_markdown(self) -> str:
        """生成 Markdown 格式"""
        md = "# 结构化提取结果\n\n"

        # 摘要
        md += "## 摘要\n\n"
        md += self.extract_summary() + "\n\n"

        # 代码块统计
        code_blocks = self.extract_code_blocks()
        md += f"## 代码块 (共 {len(code_blocks)} 个)\n\n"
        for cb in code_blocks[:10]:
            md += f"### {cb.language}\n\n"
            md += f"```\n{cb.code[:200]}\n```\n\n"

        # 表格统计
        tables = self.extract_tables()
        md += f"## 表格 (共 {len(tables)} 个)\n\n"

        # API 统计
        apis = self.extract_api()
        md += f"## API (共 {len(apis)} 个)\n\n"
        for api in apis:
            md += f"### {api.type}\n\n"
            if api.params:
                md += "| 参数 | 类型 | 说明 |\n"
                md += "|------|------|------|\n"
                for p in api.params[:10]:
                    md += f"| {p['name']} | {p['type']} | {p['description']} |\n"
                md += "\n"

        # 链接
        links = self.extract_links()
        md += f"## 链接 (共 {len(links)} 个)\n\n"
        for link in links[:20]:
            md += f"- [{link['text']}]({link['url']})\n"

        return md


def extract_from_file(filepath: str) -> Dict:
    """从文件提取"""
    with open(filepath, 'r') as f:
        content = f.read()

    extractor = StructuredExtractor(content)
    return extractor.to_dict()


def extract_from_text(text: str) -> Dict:
    """从文本提取"""
    extractor = StructuredExtractor(text)
    return extractor.to_dict()


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='结构化提取器')
    parser.add_argument('file', help='要提取的文件')
    parser.add_argument('-o', '--output', help='输出文件')
    parser.add_argument('-j', '--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        content = f.read()

    extractor = StructuredExtractor(content)

    if args.json:
        result = extractor.to_dict()
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = extractor.to_markdown()

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"已保存到: {args.output}")
    else:
        print(output)
