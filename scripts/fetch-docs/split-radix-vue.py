#!/usr/bin/env python3
"""
拆分 Radix Vue 文档为结构化目录
"""

import re
from pathlib import Path

INPUT_FILE = Path("docs/frameworks/radix-vue.md")
OUTPUT_DIR = Path("docs/frameworks/radix-vue")
COMPONENTS_DIR = OUTPUT_DIR / "components"

def split_document():
    """拆分文档"""
    print("🚀 开始拆分 Radix Vue 文档...")

    content = INPUT_FILE.read_text(encoding="utf-8")

    # 提取元信息和前言（## 核心概念 之前的内容）
    meta_match = re.search(r'^(# .*?)## Accordion', content, re.DOTALL)
    if not meta_match:
        print("✗ 无法找到元信息部分")
        return

    meta_content = meta_match.group(1).strip()

    # 提取所有组件部分
    # 模式：## Component Name ... ---
    component_pattern = r'## ([^#\n]+?)\n(.*?)(?=\n## |\n---\n*$)'
    components = re.findall(component_pattern, content[meta_match.end()-10:], re.DOTALL)

    print(f"📦 发现 {len(components)} 个组件")

    # 创建索引文件
    index_content = meta_content + "\n\n## 组件目录\n\n"

    component_list = []
    for comp_name, comp_content in components:
        comp_name = comp_name.strip()
        comp_file = comp_name.lower().replace(" ", "-").replace(".", "") + ".md"

        # 提取描述（第一行）
        desc_match = re.search(r'^([^\n]+)', comp_content.strip())
        description = desc_match.group(1) if desc_match else ""

        component_list.append({
            "name": comp_name,
            "file": comp_file,
            "description": description
        })

    # 生成索引内容
    for comp in component_list:
        index_content += f"- [{comp['name']}](./components/{comp['file']}) - {comp['description'][:60]}...\n"

    index_content += """

## 使用指南

### 查找组件
1. 在上方目录中找到组件名
2. 点击查看详细文档

### 组件文档结构
每个组件文档包含：
- 描述
- 使用示例
- Props / Attributes
- Data Attributes / CSS Variables

---

*本文档由 AI-Assistant 自动生成*
"""

    # 保存索引文件
    index_file = OUTPUT_DIR / "index.md"
    index_file.write_text(index_content, encoding="utf-8")
    print(f"✓ 索引文件: {index_file}")

    # 保存每个组件文件
    for comp_name, comp_content in components:
        comp_name = comp_name.strip()
        comp_file = comp_name.lower().replace(" ", "-").replace(".", "") + ".md"
        comp_path = COMPONENTS_DIR / comp_file

        # 添加组件标题
        full_content = f"# {comp_name}\n\n{comp_content.strip()}\n"

        comp_path.write_text(full_content, encoding="utf-8")
        print(f"  ✓ {comp_name} -> {comp_file}")

    # 统计
    print(f"\n✅ 拆分完成!")
    print(f"   - 索引文件: {index_file}")
    print(f"   - 组件文件: {COMPONENTS_DIR} ({len(components)} 个)")

    # 计算大小
    index_size = len(index_content)
    avg_component_size = sum(len(comp_content) for _, comp_content in components) / len(components)

    print(f"\n📊 文件大小:")
    print(f"   - 索引: {index_size / 1024:.1f} KB")
    print(f"   - 平均组件: {avg_component_size / 1024:.1f} KB")
    print(f"   - 原文件: {len(content) / 1024:.1f} KB")
    print(f"   - 节省上下文: ~{((len(content) - avg_component_size) / len(content) * 100):.0f}% (使用单个组件时)")

if __name__ == "__main__":
    split_document()
