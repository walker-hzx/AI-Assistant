#!/usr/bin/env python3
"""
Headless UI 文档爬取脚本
使用 Playwright 访问官网并提取组件文档
"""

import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent.parent / "docs" / "frameworks"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Headless UI Vue 组件列表（官网结构）
COMPONENTS = [
    "dialog",
    "disclosure",
    "focus-trap",
    "listbox",
    "menu",
    "popover",
    "radio-group",
    "switch",
    "tabs",
    "transition",
    "combobox",
]


def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def extract_component_docs(page, component_name):
    """提取单个组件的文档"""
    url = f"https://headlessui.com/vue/{component_name}"
    print(f"  正在获取: {url}")

    page.goto(url, wait_until="networkidle")

    # 等待内容加载
    page.wait_for_selector("article", timeout=10000)

    # 提取组件基本信息
    title = page.title()

    # 提取主要文档内容
    # Headless UI 使用特定的文档结构
    docs = {
        "name": component_name,
        "title": title,
        "url": url,
        "description": "",
        "examples": [],
        "api": {"props": [], "events": [], "slots": []},
    }

    # 尝试提取描述（通常在 h1 后面的第一段）
    try:
        description = page.locator("article > div > p").first.inner_text(timeout=5000)
        docs["description"] = clean_text(description)
    except:
        pass

    # 提取代码示例（pre 或 code 块）
    try:
        code_blocks = page.locator("pre code").all()
        for i, block in enumerate(code_blocks[:5]):  # 限制前5个示例
            try:
                code = block.inner_text()
                if code and len(code) > 50:  # 过滤掉太短的片段
                    docs["examples"].append({
                        "index": i,
                        "code": code[:2000],  # 限制长度
                    })
            except:
                continue
    except:
        pass

    # 提取 API 表格（如果有）
    try:
        tables = page.locator("table").all()
        for table in tables:
            try:
                headers = table.locator("th").all_inner_texts()
                rows = table.locator("tr").all()

                if "prop" in " ".join(headers).lower() or "name" in " ".join(headers).lower():
                    for row in rows[1:]:  # 跳过表头
                        cells = row.locator("td").all_inner_texts()
                        if len(cells) >= 2:
                            docs["api"]["props"].append({
                                "name": clean_text(cells[0]),
                                "type": clean_text(cells[1]) if len(cells) > 1 else "",
                                "description": clean_text(cells[2]) if len(cells) > 2 else "",
                            })
            except:
                continue
    except:
        pass

    return docs


def generate_markdown(all_docs):
    """生成 Markdown 文档"""
    md = """# Headless UI (Vue) 使用指南

## 元信息
- 官网：https://headlessui.com/vue
- 包名：`@headlessui/vue`
- 语言：Vue 3
- 特点：完全无样式、无障碍支持、Composition API

## 安装

```bash
npm install @headlessui/vue
```

## 组件列表

"""

    # 生成目录
    for doc in all_docs:
        name = doc["name"].replace("-", " ").title()
        md += f"- [{name}](#{doc['name']})\n"

    md += "\n---\n\n"

    # 生成每个组件的文档
    for doc in all_docs:
        name = doc["name"].replace("-", " ").title()
        md += f"## {name}\n\n"
        md += f"**文档链接**: [{doc['url']}]({doc['url']})\n\n"

        if doc["description"]:
            md += f"{doc['description']}\n\n"

        # 代码示例
        if doc["examples"]:
            md += "### 示例\n\n"
            for i, example in enumerate(doc["examples"][:2]):  # 只显示前2个示例
                md += f"```vue\n{example['code']}\n```\n\n"

        # API
        if doc["api"]["props"]:
            md += "### Props\n\n"
            md += "| 属性 | 类型 | 说明 |\n"
            md += "|------|------|------|\n"
            for prop in doc["api"]["props"][:10]:  # 限制数量
                md += f"| {prop['name']} | {prop['type']} | {prop['description']} |\n"
            md += "\n"

        md += "---\n\n"

    # 添加最佳实践
    md += """## 最佳实践

### 通用原则
1. **完全无样式** - 所有组件都没有默认样式，需要使用 Tailwind CSS 等自行添加
2. **无障碍支持** - 自动处理 ARIA 属性、键盘导航
3. **Renderless Pattern** - 通过 v-slot 获取组件状态

### 常见组合
```vue
<!-- Dialog + Transition -->
<TransitionRoot appear :show="isOpen">
  <Dialog @close="isOpen = false">
    <TransitionChild>
      <div class="fixed inset-0 bg-black/30" />
    </TransitionChild>
    <TransitionChild>
      <DialogPanel>内容</DialogPanel>
    </TransitionChild>
  </Dialog>
</TransitionRoot>
```

### 注意事项
- Vue 版本要求：3.0+
- 需要配合 CSS 框架使用（推荐 Tailwind CSS）
- 过渡动画需要使用 Transition 组件包裹

---

*本文档由 fetch-headlessui.py 自动生成*
*生成时间：自动更新*
"""

    return md


def main():
    """主函数"""
    print("🚀 开始爬取 Headless UI 文档...")
    print(f"📁 输出目录: {OUTPUT_DIR}")

    all_docs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 设置视窗大小
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            for component in COMPONENTS:
                print(f"\n📦 处理组件: {component}")
                try:
                    doc = extract_component_docs(page, component)
                    all_docs.append(doc)
                    print(f"  ✓ 获取成功: {len(doc['examples'])} 个示例")
                except Exception as e:
                    print(f"  ✗ 获取失败: {e}")
                    # 添加空文档占位
                    all_docs.append({
                        "name": component,
                        "title": component,
                        "url": f"https://headlessui.com/vue/{component}",
                        "description": "",
                        "examples": [],
                        "api": {"props": [], "events": [], "slots": []},
                    })

        finally:
            browser.close()

    # 生成 Markdown
    print("\n📝 生成 Markdown 文档...")
    markdown = generate_markdown(all_docs)

    # 保存文件
    output_file = OUTPUT_DIR / "headlessui.md"
    output_file.write_text(markdown, encoding="utf-8")

    print(f"\n✅ 完成！文档已保存到: {output_file}")
    print(f"📊 共处理 {len(all_docs)} 个组件")


if __name__ == "__main__":
    main()
