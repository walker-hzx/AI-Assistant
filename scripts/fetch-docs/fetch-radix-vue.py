#!/usr/bin/env python3
"""
Radix Vue 文档爬取脚本
https://www.radix-vue.com/
"""

import re
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path(__file__).parent.parent.parent / "docs" / "frameworks"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:500] if len(text) > 500 else text


def extract_component_docs(page, component):
    """提取单个组件的文档"""
    name = component["name"]
    path = component["href"]
    url = f"https://www.radix-vue.com{path}" if not path.startswith("http") else path

    print(f"\n  📦 {name}")

    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        docs = {
            "name": name,
            "path": path,
            "url": url,
            "description": "",
            "examples": [],
            "api": {"props": [], "events": [], "slots": [], "data_attributes": []},
        }

        # 提取描述 - 通常在第一个 h1 后的段落
        try:
            h1 = page.locator("h1").first
            if h1:
                h1_text = h1.inner_text()
                # 查找 h1 后的第一个段落
                next_p = page.locator("h1 + p, h1 ~ p").first
                if next_p:
                    desc = next_p.inner_text()
                    if desc and len(desc) > 10:
                        docs["description"] = clean_text(desc)
        except Exception as e:
            print(f"     ⚠ 描述提取失败: {e}")

        # 提取代码示例
        try:
            # Radix Vue 使用 shiki 高亮
            code_blocks = page.locator("pre code").all()
            for i, block in enumerate(code_blocks[:6]):  # 限制数量
                try:
                    code = block.inner_text()
                    if code and len(code) > 30:
                        # 检测语言
                        lang = "vue"
                        if "<script" in code:
                            lang = "vue"
                        elif "import {" in code and "<" not in code:
                            lang = "typescript"

                        # 去重
                        if not any(ex["code"][:100] == code[:100] for ex in docs["examples"]):
                            docs["examples"].append({
                                "index": i,
                                "language": lang,
                                "code": code[:3500],
                            })
                except:
                    continue
        except Exception as e:
            print(f"     ⚠ 代码示例提取失败: {e}")

        # 提取 API 表格 - Radix Vue 通常有多个表格
        try:
            tables = page.locator("table").all()
            for table_idx, table in enumerate(tables):
                try:
                    # 获取表头
                    headers = table.locator("th").all_inner_texts()
                    header_text = " ".join(headers).lower()

                    # 获取表格标题（通常在表格前的 h2/h3）
                    table_title = ""
                    try:
                        # 尝试找到表格前的标题
                        table_elem = table.element_handle()
                        if table_elem:
                            # 通过 JS 获取前一个兄弟元素
                            prev = table_elem.evaluate(
                                "el => { let prev = el.previousElementSibling; "
                                "while(prev && !prev.matches('h2, h3, h4')) prev = prev.previousElementSibling; "
                                "return prev ? prev.textContent : ''; }"
                            )
                            if prev:
                                table_title = prev.strip().lower()
                    except:
                        pass

                    rows = table.locator("tbody tr").all()

                    # 判断表格类型
                    is_props = (
                        "attribute" in header_text
                        or "prop" in header_text
                        or "property" in table_title
                        or "props" in table_title
                    )
                    is_events = "event" in header_text or "event" in table_title
                    is_data_attr = "data attribute" in header_text or "css" in table_title

                    for row in rows[:20]:  # 限制数量
                        cells = row.locator("td").all_inner_texts()
                        if len(cells) >= 2:
                            item = {
                                "name": clean_text(cells[0]),
                                "type": clean_text(cells[1]) if len(cells) > 1 else "",
                                "description": clean_text(cells[2]) if len(cells) > 2 else "",
                            }

                            if is_data_attr:
                                docs["api"]["data_attributes"].append(item)
                            elif is_events:
                                docs["api"]["events"].append(item)
                            elif is_props or table_idx < 3:  # 默认前3个表格是 props
                                docs["api"]["props"].append(item)

                except Exception as e:
                    continue
        except Exception as e:
            print(f"     ⚠ API 表格提取失败: {e}")

        total_api = len(docs["api"]["props"]) + len(docs["api"]["events"]) + len(docs["api"]["data_attributes"])
        print(f"     ✓ {len(docs['examples'])} 个示例, {total_api} 个 API 条目")
        return docs

    except Exception as e:
        print(f"     ✗ 获取失败: {e}")
        return {
            "name": name,
            "path": path,
            "url": url,
            "description": "",
            "examples": [],
            "api": {"props": [], "events": [], "slots": [], "data_attributes": []},
        }


def generate_markdown(all_docs):
    """生成 Markdown 文档"""
    md = """# Radix Vue 使用指南

> 本文档由 docs-sync 自动生成
> 官网：https://www.radix-vue.com/

## 元信息

- **框架**: Radix Vue
- **官网**: https://www.radix-vue.com/
- **包名**: `radix-vue`
- **技术栈**: Vue 3
- **特点**: 无障碍 UI 组件原语、Headless、完全可定制

## 安装

```bash
npm install radix-vue
```

## 核心概念

Radix Vue 提供的是**无头组件原语（Headless Component Primitives）**：
- ✅ 完全可访问性支持（ARIA、键盘导航）
- ✅ 无默认样式，完全由你控制
- ✅ 通过插槽和事件暴露状态和逻辑
- ✅ 支持自定义元素（as 属性）

## 组件列表

"""

    # 生成分类列表
    for doc in all_docs:
        name = doc["name"]
        anchor = name.lower().replace(" ", "-").replace(".", "")
        md += f"- [{name}](#{anchor})\n"

    md += "\n---\n\n"

    # 生成每个组件的文档
    for doc in all_docs:
        name = doc["name"]
        anchor = name.lower().replace(" ", "-").replace(".", "")

        md += f"## {name}\n\n"

        if doc["description"]:
            md += f"{doc['description']}\n\n"

        md += f"📖 [官方文档]({doc['url']})\n\n"

        # 代码示例
        if doc["examples"]:
            md += "### 示例\n\n"
            for i, example in enumerate(doc["examples"][:3]):
                lang = example["language"]
                md += f"```{lang}\n{example['code']}\n```\n\n"

        # Props
        if doc["api"]["props"]:
            md += "### Props / Attributes\n\n"
            md += "| 属性 | 类型 | 说明 |\n"
            md += "|------|------|------|\n"
            for prop in doc["api"]["props"][:25]:
                name = prop["name"].replace("|", "\\|")[:30]
                type_ = prop["type"].replace("|", "\\|")[:40]
                desc = prop["description"].replace("|", "\\|")[:80]
                md += f"| `{name}` | `{type_}` | {desc} |\n"
            md += "\n"

        # Events
        if doc["api"]["events"]:
            md += "### Events\n\n"
            md += "| 事件 | 说明 |\n"
            md += "|------|------|\n"
            for event in doc["api"]["events"][:15]:
                name = event["name"].replace("|", "\\|")[:30]
                desc = event["description"].replace("|", "\\|")[:100]
                md += f"| `{name}` | {desc} |\n"
            md += "\n"

        # Data Attributes / CSS Variables
        if doc["api"]["data_attributes"]:
            md += "### Data Attributes / CSS Variables\n\n"
            md += "| 属性 | 说明 |\n"
            md += "|------|------|\n"
            for attr in doc["api"]["data_attributes"][:10]:
                name = attr["name"].replace("|", "\\|")[:30]
                desc = attr["description"].replace("|", "\\|")[:100]
                md += f"| `{name}` | {desc} |\n"
            md += "\n"

        md += "---\n\n"

    # 添加最佳实践
    md += """## 最佳实践

### 组合使用模式

Radix Vue 的组件设计为可以组合使用：

```vue
<script setup>
import {
  AccordionRoot,
  AccordionItem,
  AccordionHeader,
  AccordionTrigger,
  AccordionContent,
} from 'radix-vue'
</script>

<template>
  <AccordionRoot type="single" default-value="item-1">
    <AccordionItem value="item-1">
      <AccordionHeader>
        <AccordionTrigger>标题</AccordionTrigger>
      </AccordionHeader>
      <AccordionContent>内容</AccordionContent>
    </AccordionItem>
  </AccordionRoot>
</template>
```

### 无障碍支持

Radix Vue 自动处理：
- ARIA 属性
- 键盘导航
- 焦点管理
- 屏幕阅读器支持

### 样式建议

配合 Tailwind CSS 或 UnoCSS 使用：

```vue
<AccordionTrigger class="flex w-full items-center justify-between py-2 px-4 hover:bg-gray-100">
  <span>标题</span>
  <ChevronDownIcon class="h-4 w-4 transition-transform duration-300" />
</AccordionTrigger>
```

### 注意事项

1. **必须使用完整的组件组合** - 如 Accordion 需要 Root/Item/Header/Trigger/Content
2. **value 属性** - 用于标识和状态管理
3. **as 属性** - 可以自定义渲染元素，如 `<AccordionTrigger as="button">`
4. ** forwardedRef** - 通过 `asChild` 或模板 ref 获取底层元素

---

*本文档由 AI-Assistant docs-sync 技能自动生成*
"""

    return md


def main():
    """主函数"""
    print("🚀 开始爬取 Radix Vue 文档...")
    print(f"📁 输出目录: {OUTPUT_DIR}")

    # 组件列表 - 只爬取核心组件避免时间过长
    CORE_COMPONENTS = [
        {"name": "Accordion", "href": "/components/accordion.html"},
        {"name": "Alert Dialog", "href": "/components/alert-dialog.html"},
        {"name": "Aspect Ratio", "href": "/components/aspect-ratio.html"},
        {"name": "Avatar", "href": "/components/avatar.html"},
        {"name": "Checkbox", "href": "/components/checkbox.html"},
        {"name": "Collapsible", "href": "/components/collapsible.html"},
        {"name": "Combobox", "href": "/components/combobox.html"},
        {"name": "Context Menu", "href": "/components/context-menu.html"},
        {"name": "Dialog", "href": "/components/dialog.html"},
        {"name": "Dropdown Menu", "href": "/components/dropdown-menu.html"},
        {"name": "Hover Card", "href": "/components/hover-card.html"},
        {"name": "Label", "href": "/components/label.html"},
        {"name": "Menubar", "href": "/components/menubar.html"},
        {"name": "Navigation Menu", "href": "/components/navigation-menu.html"},
        {"name": "Popover", "href": "/components/popover.html"},
        {"name": "Progress", "href": "/components/progress.html"},
        {"name": "Radio Group", "href": "/components/radio-group.html"},
        {"name": "Scroll Area", "href": "/components/scroll-area.html"},
        {"name": "Select", "href": "/components/select.html"},
        {"name": "Separator", "href": "/components/separator.html"},
        {"name": "Slider", "href": "/components/slider.html"},
        {"name": "Switch", "href": "/components/switch.html"},
        {"name": "Tabs", "href": "/components/tabs.html"},
        {"name": "Toast", "href": "/components/toast.html"},
        {"name": "Toggle", "href": "/components/toggle.html"},
        {"name": "Toggle Group", "href": "/components/toggle-group.html"},
        {"name": "Toolbar", "href": "/components/toolbar.html"},
        {"name": "Tooltip", "href": "/components/tooltip.html"},
    ]

    print(f"📦 共 {len(CORE_COMPONENTS)} 个核心组件")

    all_docs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        # 阻止图片和字体加载（加速）
        page.route(
            "**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,eot}",
            lambda route: route.abort(),
        )

        try:
            for component in CORE_COMPONENTS:
                doc = extract_component_docs(page, component)
                all_docs.append(doc)

        finally:
            browser.close()

    # 生成 Markdown
    print("\n📝 生成 Markdown 文档...")
    markdown = generate_markdown(all_docs)

    # 保存文件
    output_file = OUTPUT_DIR / "radix-vue.md"
    output_file.write_text(markdown, encoding="utf-8")

    # 统计信息
    total_examples = sum(len(d["examples"]) for d in all_docs)
    total_props = sum(len(d["api"]["props"]) for d in all_docs)
    total_events = sum(len(d["api"]["events"]) for d in all_docs)

    print("\n" + "=" * 50)
    print("✅ 爬取完成！")
    print("=" * 50)
    print(f"📄 文档保存: {output_file}")
    print(f"📊 统计:")
    print(f"   - 组件数: {len(all_docs)}")
    print(f"   - 代码示例: {total_examples}")
    print(f"   - Props: {total_props}")
    print(f"   - Events: {total_events}")
    print(f"   - 文档大小: {len(markdown) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
