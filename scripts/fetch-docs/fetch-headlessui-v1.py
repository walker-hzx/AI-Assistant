#!/usr/bin/env python3
"""
Headless UI (v1/vue) 文档爬取脚本
自动生成，针对 https://headlessui.com/v1/vue 的结构
"""

import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent.parent / "docs" / "frameworks"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Headless UI v1 Vue 组件列表
COMPONENTS = [
    {"name": "Menu", "path": "/v1/vue/menu"},
    {"name": "Listbox", "path": "/v1/vue/listbox"},
    {"name": "Combobox", "path": "/v1/vue/combobox"},
    {"name": "Switch", "path": "/v1/vue/switch"},
    {"name": "Disclosure", "path": "/v1/vue/disclosure"},
    {"name": "Dialog", "path": "/v1/vue/dialog"},
    {"name": "Popover", "path": "/v1/vue/popover"},
    {"name": "Radio Group", "path": "/v1/vue/radio-group"},
    {"name": "Tabs", "path": "/v1/vue/tabs"},
    {"name": "Transition", "path": "/v1/vue/transition"},
]


def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def extract_component_docs(page, component):
    """提取单个组件的文档"""
    name = component["name"]
    path = component["path"]
    url = f"https://headlessui.com{path}"

    print(f"\n  📦 {name}")
    print(f"     URL: {url}")

    try:
        page.goto(url, wait_until="networkidle", timeout=30000)

        # 等待内容加载
        page.wait_for_selector("article, main", timeout=10000)

        docs = {
            "name": name,
            "path": path,
            "url": url,
            "description": "",
            "examples": [],
            "api": {"props": [], "events": [], "slots": []},
        }

        # 提取描述（第一个段落）
        try:
            # Headless UI v1 的描述通常在 h1 后的第一个 p
            paragraphs = page.locator("article p, main p").all()
            for p in paragraphs[:3]:  # 检查前3个段落
                text = p.inner_text()
                if text and len(text) > 30 and not text.startswith("import"):
                    docs["description"] = clean_text(text)
                    break
        except Exception as e:
            print(f"     ⚠ 描述提取失败: {e}")

        # 提取代码示例
        try:
            code_blocks = page.locator("pre code").all()
            for i, block in enumerate(code_blocks[:5]):  # 限制前5个
                try:
                    code = block.inner_text()
                    if code and len(code) > 50:
                        # 检测代码类型
                        lang = "vue" if "template" in code or "script" in code else "typescript"
                        docs["examples"].append({
                            "index": i,
                            "language": lang,
                            "code": code[:3000],  # 限制长度
                        })
                except:
                    continue
        except Exception as e:
            print(f"     ⚠ 代码示例提取失败: {e}")

        # 提取 API 表格
        try:
            tables = page.locator("table").all()
            for table in tables:
                try:
                    # 获取表头
                    headers = table.locator("th").all_inner_texts()
                    header_text = " ".join(headers).lower()

                    # 判断表格类型
                    rows = table.locator("tbody tr").all()

                    if "prop" in header_text or "name" in header_text:
                        # Props 表格
                        for row in rows[:15]:  # 限制数量
                            cells = row.locator("td").all_inner_texts()
                            if len(cells) >= 2:
                                docs["api"]["props"].append({
                                    "name": clean_text(cells[0]),
                                    "type": clean_text(cells[1]) if len(cells) > 1 else "",
                                    "description": clean_text(cells[2]) if len(cells) > 2 else "",
                                })

                    elif "event" in header_text or "slot" in header_text:
                        # Events 或 Slots 表格
                        for row in rows[:10]:
                            cells = row.locator("td").all_inner_texts()
                            if len(cells) >= 2:
                                docs["api"]["events"].append({
                                    "name": clean_text(cells[0]),
                                    "description": clean_text(cells[1]) if len(cells) > 1 else "",
                                })

                except:
                    continue
        except Exception as e:
            print(f"     ⚠ API 表格提取失败: {e}")

        print(f"     ✓ {len(docs['examples'])} 个示例, {len(docs['api']['props'])} 个 Props")
        return docs

    except Exception as e:
        print(f"     ✗ 获取失败: {e}")
        return {
            "name": name,
            "path": path,
            "url": url,
            "description": "",
            "examples": [],
            "api": {"props": [], "events": [], "slots": []},
        }


def generate_markdown(all_docs):
    """生成 Markdown 文档"""
    md = """# Headless UI (v1/vue) 使用指南

> 本文档由 docs-sync 自动生成
> 官网：https://headlessui.com/v1/vue

## 元信息

- **框架**: Headless UI
- **版本**: v1.x
- **官网**: https://headlessui.com/v1/vue
- **包名**: `@headlessui/vue`
- **技术栈**: Vue 3
- **特点**: 完全无样式、无障碍支持、Renderless 组件

## 安装

```bash
npm install @headlessui/vue
```

## 组件列表

"""

    # 生成目录
    for doc in all_docs:
        name = doc["name"]
        anchor = name.lower().replace(" ", "-")
        md += f"- [{name}](#{anchor})\n"

    md += "\n---\n\n"

    # 生成每个组件的文档
    for doc in all_docs:
        name = doc["name"]
        anchor = name.lower().replace(" ", "-")

        md += f"## {name}\n\n"

        if doc["description"]:
            md += f"{doc['description']}\n\n"

        md += f"📖 [官方文档]({doc['url']})\n\n"

        # 代码示例
        if doc["examples"]:
            md += "### 示例\n\n"
            for i, example in enumerate(doc["examples"][:3]):  # 只显示前3个
                lang = example["language"]
                md += f"```vue\n{example['code']}\n```\n\n"

        # Props
        if doc["api"]["props"]:
            md += "### Props\n\n"
            md += "| 属性 | 类型 | 说明 |\n"
            md += "|------|------|------|\n"
            for prop in doc["api"]["props"][:20]:  # 限制数量
                name = prop["name"].replace("|", "\\|")
                type_ = prop["type"].replace("|", "\\|")[:50]
                desc = prop["description"].replace("|", "\\|")[:100]
                md += f"| `{name}` | {type_} | {desc} |\n"
            md += "\n"

        # Events
        if doc["api"]["events"]:
            md += "### Events / Slots\n\n"
            md += "| 名称 | 说明 |\n"
            md += "|------|------|\n"
            for event in doc["api"]["events"][:10]:
                name = event["name"].replace("|", "\\|")
                desc = event["description"].replace("|", "\\|")[:100]
                md += f"| `{name}` | {desc} |\n"
            md += "\n"

        md += "---\n\n"

    # 添加最佳实践
    md += """## 最佳实践

### 通用原则
1. **完全无样式** - Headless UI 只提供行为和逻辑，样式完全由你控制
2. **无障碍支持** - 自动处理 ARIA 属性、键盘导航、焦点管理
3. **Renderless Pattern** - 通过 v-slot 获取组件状态和逻辑
4. **组合式 API** - 组件设计为可组合使用

### 常见组合
```vue
<!-- Dialog + Transition -->
<TransitionRoot appear :show="isOpen">
  <Dialog @close="isOpen = false">
    <TransitionChild>
      <div class="fixed inset-0 bg-black/30" />
    </TransitionChild>
    <TransitionChild>
      <DialogPanel class="bg-white rounded-lg">
        <!-- 内容 -->
      </DialogPanel>
    </TransitionChild>
  </Dialog>
</TransitionRoot>
```

### 注意事项
- Vue 版本要求：3.0+
- 需要配合 CSS 框架使用（推荐 Tailwind CSS）
- 过渡动画需要使用 Transition 组件
- 组件默认使用 ` Disclosure`, `Menu` 等标签名，可通过 `as` 属性自定义

---

*本文档由 AI-Assistant docs-sync 技能自动生成*
*生成时间：自动更新*
"""

    return md


def main():
    """主函数"""
    print("🚀 开始爬取 Headless UI (v1) 文档...")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📦 共 {len(COMPONENTS)} 个组件")

    all_docs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        # 设置请求拦截，阻止图片和字体加载（加速）
        page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf}", lambda route: route.abort())

        try:
            for component in COMPONENTS:
                doc = extract_component_docs(page, component)
                all_docs.append(doc)

        finally:
            browser.close()

    # 生成 Markdown
    print("\n📝 生成 Markdown 文档...")
    markdown = generate_markdown(all_docs)

    # 保存文件
    output_file = OUTPUT_DIR / "headlessui-v1.md"
    output_file.write_text(markdown, encoding="utf-8")

    # 统计信息
    total_examples = sum(len(d["examples"]) for d in all_docs)
    total_props = sum(len(d["api"]["props"]) for d in all_docs)

    print("\n" + "="*50)
    print("✅ 爬取完成！")
    print("="*50)
    print(f"📄 文档保存: {output_file}")
    print(f"📊 统计:")
    print(f"   - 组件数: {len(all_docs)}")
    print(f"   - 代码示例: {total_examples}")
    print(f"   - API 条目: {total_props}")
    print(f"   - 文档大小: {len(markdown) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
