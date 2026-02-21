---
name: docs-sync
description: 自动从官网爬取框架/组件库文档，生成结构化的使用指南。输入框架名称和官网地址，自动分析网站结构、生成爬虫脚本、整理文档。
model: sonnet
user-invocable: true
---

# 文档同步工具

自动从官网爬取前端框架/组件库文档，生成结构化的 Markdown 使用指南。

## 概述

**功能：**
1. 分析官网结构 - 访问网站，识别组件/API 文档位置
2. 生成爬虫脚本 - 针对该网站结构生成 Python + Playwright 爬虫
3. 执行数据爬取 - 获取组件列表、API、示例代码
4. 生成标准文档 - 整理成 Markdown 格式，保存到 `docs/frameworks/`

**使用场景：**
- 项目使用了新的组件库，需要快速建立参考文档
- 组件库版本升级，需要同步更新文档
- 多个项目共用组件库，统一文档标准

## 使用流程

**用户触发：**
```
用户: /docs-sync
AI: 请输入框架名称和官网地址（格式：名称, URL）
用户: Element Plus, https://element-plus.org
```

**执行步骤：**
1. **分析网站** - 访问官网，识别导航结构、组件列表页
2. **确认范围** - 与用户确认要爬取的组件范围
3. **生成脚本** - 创建针对性的爬虫脚本 `scripts/fetch-docs/fetch-{name}.py`
4. **执行爬取** - 运行脚本获取数据
5. **生成文档** - 整理成标准格式，保存到 `docs/frameworks/{name}.md`
6. **审查确认** - 展示生成的文档结构，用户确认或调整

## 文档标准格式

生成的文档包含：

```markdown
# {框架名} 使用指南

## 元信息
- 官网：{url}
- 包名：`{package}`
- 语言：{lang}
- 生成时间：{date}

## 安装
```bash
npm install {package}
```

## 组件列表
- [组件1](#组件1)
- [组件2](#组件2)
...

## 组件详情

### 组件1
**描述**：{description}

**基础用法**：
```vue
{code example}
```

**Props**：
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| ... | ... | ... | ... |

**Events**：
| 事件 | 参数 | 说明 |
|------|------|------|
| ... | ... | ... |

## 最佳实践
- 注意事项
- 常见用法
```

## 交互步骤

### 步骤 1：接收输入

询问用户：
```
请提供以下信息：
1. 框架名称（如：Element Plus）
2. 官网地址（如：https://element-plus.org）
3. 包名（如：element-plus）
4. 技术栈（Vue 3 / React / 其他）
```

### 步骤 2：分析网站结构

使用 Playwright 访问官网：
- 识别导航菜单结构
- 找到组件列表页面
- 分析组件详情页模板
- 识别代码示例位置

向用户报告发现：
```
网站分析完成：
- 发现 {n} 个组件
- 组件列表页：{url}
- 每个组件包含：Props/Events/Methods/示例
- 预计爬取时间：{time}

是否开始爬取？
```

### 步骤 3：生成爬虫脚本

创建脚本文件：`scripts/fetch-docs/fetch-{framework}.py`

脚本模板：
```python
#!/usr/bin/env python3
"""
{框架名} 文档爬取脚本
自动生成，针对 {url} 的结构
"""

from playwright.sync_api import sync_playwright
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent / "docs" / "frameworks"
COMPONENTS = [
    # 自动填充组件列表
]

def fetch_component(page, name):
    # 针对该网站的爬取逻辑
    pass

def generate_markdown(data):
    # 生成标准格式文档
    pass

if __name__ == "__main__":
    main()
```

### 步骤 4：执行爬取

运行生成的脚本：
```bash
python3 scripts/fetch-docs/fetch-{framework}.py
```

实时监控进度：
```
正在爬取：
✓ Button 完成（3 个示例，12 个 Props）
✓ Input 完成（2 个示例，8 个 Props）
...
```

### 步骤 5：生成并展示文档

保存文档到 `docs/frameworks/{framework}.md`

向用户展示文档结构：
```
文档生成完成！

文件位置：docs/frameworks/{framework}.md
文档大小：{size} KB
包含内容：
- {n} 个组件
- {m} 个代码示例
- {k} 个 API 条目

是否需要：
1. 查看生成的文档
2. 调整内容范围
3. 重新生成
```

### 步骤 6：后续使用

告知用户如何使用生成的文档：
```
文档已准备就绪！

后续开发时，我会自动参考：
docs/frameworks/{framework}.md

生成组件代码时，会使用该框架的正确 API。
```

## 输出要求

**文件位置：**
- 爬虫脚本：`scripts/fetch-docs/fetch-{name}.py`
- 生成文档：`docs/frameworks/{name}.md`

**质量标准：**
- [ ] 文档包含框架基本信息（名称、版本、安装方式）
- [ ] 包含主要组件的 API 说明
- [ ] 包含可运行的代码示例
- [ ] 格式统一，易于阅读

## 注意事项

1. **尊重网站规则** - 遵守 robots.txt，控制访问频率
2. **增量更新** - 支持只更新变更的部分
3. **错误处理** - 网站结构变化时友好提示
4. **人工审查** - 重要文档生成后建议人工检查

## 后续优化

使用后可收集反馈：
- 哪些组件遗漏了？
- API 描述是否准确？
- 示例代码是否可用？

用于持续改进爬取逻辑。
