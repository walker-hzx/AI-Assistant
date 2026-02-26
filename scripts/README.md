# Scripts

爬虫脚本集合，为 web-researcher 和 docs-sync 提供底层能力。

## 目录结构

```
scripts/
├── web/                      # 通用爬虫（web-researcher 使用）
│   ├── fetch-url.py          # 主爬取脚本（支持单页/整站/批量）
│   └── README.md             # 使用说明
│
├── fetch-docs/               # 专用框架爬虫（docs-sync 使用）
│   ├── fetch-claude-code-docs.py
│   ├── fetch-radix-vue.py
│   ├── fetch-headlessui.py
│   └── README.md
│
├── fetch_claude_docs_playwright.py  # Claude Code 文档（旧版，保留兼容）
│
└── generate-team-prompt.py   # 团队提示生成
```

## 选择正确的爬虫

| 场景 | 推荐工具 |
|------|----------|
| 临时研究任意网站 | `web/fetch-url.py` |
| 整站备份/批量爬取 | `web/fetch-url.py --crawl` |
| 框架文档标准化 | `docs-sync` skill |
| 特定框架文档更新 | `fetch-docs/fetch-{name}.py` |

## 快速开始

### 通用爬虫

```bash
# 单页爬取
python3 scripts/web/fetch-url.py https://example.com -o result.md

# 整站爬取（自动发现所有页面）
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 2 -o docs/

# 查看帮助
python3 scripts/web/fetch-url.py --help
```

### 框架文档

```bash
# 使用 docs-sync skill（推荐）
/docs-sync

# 或直接运行脚本
python3 scripts/fetch-docs/fetch-claude-code-docs.py
```
