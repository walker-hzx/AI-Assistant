# 文档爬取工具

用于从官网爬取前端框架/组件库文档，生成结构化的 Markdown 参考文档。

## 目录结构

```
scripts/
├── web/                      # 通用爬虫（web-researcher 使用）
│   └── fetch-url.py          # 主爬取脚本
│
└── fetch-docs/               # 专用框架爬虫（docs-sync 使用）
    ├── fetch-claude-code-docs.py   # Claude Code 文档
    ├── fetch-radix-vue.py          # Radix Vue
    ├── fetch-headlessui.py         # Headless UI
    ├── analyze-*.py               # 分析脚本
    ├── split-*.py                 # 拆分脚本
    └── extract-*.py              # 提取脚本
```

## 使用方式

### 1. 通用爬虫（web-researcher）

适用于任意网站的临时研究。

```bash
# 单页爬取
python3 scripts/web/fetch-url.py https://example.com

# 整站爬取
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 2

# 批量爬取
python3 scripts/web/fetch-url.py --list urls.txt
```

### 2. 专用框架爬虫

适用于需要生成标准化文档的场景。

```bash
# Claude Code 文档
python3 scripts/fetch-docs/fetch-claude-code-docs.py

# Radix Vue
python3 scripts/fetch-docs/fetch-radix-vue.py

# Headless UI
python3 scripts/fetch-docs/fetch-headlessui.py
```

### 3. docs-sync Skill

通过 Skill 自动执行框架文档爬取。

```
用户: /docs-sync
AI: 请输入框架名称和官网地址
```

## 输出位置

| 爬取方式 | 输出位置 |
|----------|----------|
| 通用爬虫 | 指定目录或 stdout |
| 专用爬虫 | `docs/frameworks/{name}.md` |
| docs-sync | `docs/frameworks/{name}/` |

## 添加新的框架爬虫

1. 在 `fetch-docs/` 创建 `fetch-{framework}.py`
2. 参考现有脚本的结构（fetch-headlessui.py）
3. 定义组件列表和选择器规则
4. 运行测试并调整

## 注意事项

- 爬取脚本仅用于 AI-Assistant 项目内部维护
- 官网结构变化时可能需要更新选择器
- 尊重网站的 robots.txt 和访问频率限制
