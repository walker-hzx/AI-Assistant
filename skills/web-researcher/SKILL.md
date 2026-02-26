---
name: web-researcher
description: "网页研究员 - 爬取指定 URL 内容，提取关键信息，理解并分析。支持单页爬取、整站爬取、模块指定爬取。使用 Python + Playwright 解决跨域等问题"
model: sonnet
user-invocable: true
---

# 网页研究员

爬取指定 URL 内容，提取关键信息，理解并分析。

## 核心能力

| 能力 | 说明 | 命令示例 |
|------|------|---------|
| **单页爬取** | 爬取单个页面 | `python fetch-url.py <url>` |
| **整站爬取** | 自动发现并爬取网站所有页面 | `python fetch-url.py <url> --crawl` |
| **深度控制** | 控制爬取层级 | `python fetch-url.py <url> -d 2` |
| **批量爬取** | 批量爬取多个 URL | `python fetch-url.py --list urls.txt` |
| **智能分析** | 结构化提取内容 | 内置分析功能 |

## 使用方式

### 1. 单页爬取

适用于临时研究、一次性需求。

```bash
# 基本用法
python3 scripts/web/fetch-url.py https://example.com

# 指定输出文件
python3 scripts/web/fetch-url.py https://example.com -o output.md

# 等待动态内容加载
python3 scripts/web/fetch-url.py https://example.com --wait 10
```

### 2. 整站爬取

自动发现网站结构，爬取所有相关页面。

```bash
# 站点爬取（默认深度 2，最大 50 页）
python3 scripts/web/fetch-url.py https://docs.example.com --crawl

# 控制爬取深度
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 3

# 最大页面数
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -m 100

# 指定输出
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -o docs-result.md
```

**输出文件**：
- `docs-result.md` - 所有页面内容合并
- `docs-result.sitemap.json` - 站点结构（JSON 格式）

### 3. 模块指定爬取

爬取网站的特定模块。

```bash
# 爬取指定模块（通过 URL 路径）
python3 scripts/web/fetch-url.py https://docs.example.com/components --crawl -d 2
```

### 4. 批量爬取

一次爬取多个指定页面。

```bash
# 从文件读取 URL 列表
python3 scripts/web/fetch-url.py --list urls.txt -o results/
```

## 脚本功能

### 核心功能

| 功能 | 说明 |
|------|------|
| Playwright 引擎 | 处理动态内容和 JavaScript 渲染 |
| 链接自动发现 | 自动提取页面中的内链 |
| URL 归一化 | 去除锚点、查询参数，去重 |
| 深度控制 | 限制爬取层级，避免无限爬取 |
| 并发控制 | 可配置并发数，默认 3 |
| 错误重试 | 失败自动重试，默认 3 次 |
| 速率限制 | 尊重目标网站 |

### 高级功能

| 功能 | 说明 |
|------|------|
| 智能内容提取 | 自动识别 main/article/docs-content 等区域 |
| 文本清洗 | 移除广告、导航等无关内容 |
| 站点地图生成 | 输出 JSON 格式的站点结构 |
| 页面关系分析 | 分析页面间的链接关系 |

### 辅助工具

| 工具 | 用途 | 命令 |
|------|------|------|
| **url-pattern-analyzer.py** | URL 模式分析 | `python url-pattern-analyzer.py urls.txt` |
| **batch-crawler.py** | 批量爬取 | `python batch-crawler.py -f urls.txt` |
| **structured-extractor.py** | 结构化提取 | `python structured-extractor.py file.md` |
| **report-generator.py** | 报告生成 | `python report-generator.py results.json` |

## 常用场景

### 场景 1：单页研究

```
用户：帮我看看这个页面 https://docs.example.com/getting-started
我需要了解安装方式

执行：
python3 scripts/web/fetch-url.py https://docs.example.com/getting-started -o guide.md

产出：
## 安装方式
- npm install xxx
- yarn add xxx
```

### 场景 2：整站文档备份

```
用户：帮我把整个文档站点爬下来
https://docs.example.com

执行：
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 3 -m 100 -o docs/

产出：
docs/
├── all.md              # 所有内容合并
└── sitemap.json        # 站点结构
```

### 场景 3：模块批量爬取

```
用户：帮我爬取"组件"模块的所有文档
https://docs.example.com/components

执行：
python3 scripts/web/fetch-url.py https://docs.example.com/components --crawl -d 2 -o components/

产出：
components/
├── button.md
├── dialog.md
├── input.md
└── sitemap.json
```

### 场景 4：批量研究多个页面

```
用户：我需要了解这几个页面的内容
- https://docs.example.com/api/auth
- https://docs.example.com/api/users
- https://docs.example.com/api/permissions

执行：
# 创建 urls.txt
echo -e "https://docs.example.com/api/auth\nhttps://docs.example.com/api/users\nhttps://docs.example.com/api/permissions" > urls.txt
python3 scripts/web/fetch-url.py --list urls.txt -o api-docs/

产出：
api-docs/
├── auth.md
├── users.md
└── permissions.md
```

### 场景 5：URL 模式分析

分析已爬取的 URL 列表，发现规律和模块结构。

```
# 先爬取一些页面获取 URL
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 1 -m 20

# 分析 URL 模式
python3 scripts/web/url-pattern-analyzer.py -f sitemap.json -o analysis.md

# 或 JSON 格式
python3 scripts/web/url-pattern-analyzer.py -f sitemap.json -j -o analysis.json
```

### 场景 6：批量爬取 + 报告生成

完整的工作流：从 URL 列表到完整报告。

```
# 1. 创建 URL 列表
echo "https://docs.example.com/intro" > urls.txt
echo "https://docs.example.com/install" >> urls.txt

# 2. 批量爬取
python3 scripts/web/batch-crawler.py -f urls.txt -o results/

# 3. 生成报告
python3 scripts/web/report-generator.py results/crawl-success.json -o report.md
```

### 场景 7：结构化提取

从内容中提取结构化数据（代码块、表格、API）。

```
# 提取结构化数据
python3 scripts/web/structured-extractor.py content.md -o structured.json -j

# 或生成 Markdown 报告
python3 scripts/web/structured-extractor.py content.md -o structured-report.md
```

## 参数说明

| 参数 | 短参数 | 说明 | 默认值 |
|------|--------|------|--------|
| `url` | - | 爬取的 URL | - |
| `--crawl` | - | 启用站点爬取模式 | false |
| `--depth` | `-d` | 爬取深度 (1=单页) | 1 |
| `--max-pages` | `-m` | 最大页面数 | 50 |
| `--concurrency` | `-c` | 并发数 | 3 |
| `--wait` | `-w` | 等待秒数 | 5 |
| `--output` | `-o` | 输出文件/目录 | stdout |
| `--list` | `-l` | URL 列表文件 | - |

### 辅助工具参数

#### url-pattern-analyzer.py

```bash
python3 scripts/web/url-pattern-analyzer.py <urls> [-f file] [-o output] [-j]
```

| 参数 | 说明 |
|------|------|
| `urls` | URL 列表（空格分隔） |
| `-f, --file` | 从文件读取 URL |
| `-o, --output` | 输出文件 |
| `-j, --json` | JSON 格式输出 |

#### batch-crawler.py

```bash
python3 scripts/web/batch-crawler.py [-f file] [-u url] [-o output] [-c concurrency]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-f, --file` | URL 列表文件 | - |
| `-u, --url` | 单个 URL（可多次使用） | - |
| `-o, --output` | 输出目录 | - |
| `-c, --concurrency` | 并发数 | 3 |

#### structured-extractor.py

```bash
python3 scripts/web/structured-extractor.py <file> [-o output] [-j]
```

| 参数 | 说明 |
|------|------|
| `file` | 要提取的文件 |
| `-o, --output` | 输出文件 |
| `-j, --json` | JSON 格式输出 |

#### report-generator.py

```bash
python3 scripts/web/report-generator.py <results> [-o output]
```

| 参数 | 说明 |
|------|------|
| `results` | 爬取结果文件 (JSON) |
| `-o, --output` | 输出文件 |

## 输出格式

### 单页输出

```markdown
# 页面标题

**来源**: {URL}

---

{页面内容}
```

### 站点输出

```markdown
# 站点爬取结果

**入口**: {URL}
**页面数**: {N}

---

## 1. 页面标题

**URL**: {url}

{内容摘要}

---

## 2. 页面标题
...
```

### 站点地图 (JSON)

```json
{
  "base_url": "https://docs.example.com",
  "total_pages": 50,
  "pages": [
    {
      "url": "https://docs.example.com/",
      "title": "文档首页",
      "links_count": 10
    },
    ...
  ]
}
```

## 注意事项

1. **尊重网站** - 遵守 robots.txt，控制请求频率
2. **深度控制** - 建议深度不超过 3，避免爬取过多无关页面
3. **错误处理** - 网络超时、页面不存在等情况会自动重试
4. **动态内容** - 遇到 JavaScript 渲染的页面，使用 --wait 参数增加等待时间
5. **大站点** - 使用 --max-pages 限制页面数，避免运行时间过长

## 常见问题

### Q: 爬取速度慢怎么办？
A: 使用 `-c` 参数增加并发数，例如 `-c 5`，但注意不要过快以免被封

### Q: 页面显示需要登录怎么办？
A: 尝试访问公开内容，或提示用户需要登录凭证

### Q: 动态内容加载不出来？
A: 使用 `-w` 参数增加等待时间，例如 `-w 10`

### Q: 爬取被阻止怎么办？
A: 检查目标网站的 robots.txt，或降低并发数

### Q: 内存占用太大？
A: 减少 --max-pages 参数，或分批爬取

## 与其他工具的关系

| 工具 | 用途 | 选择建议 |
|------|------|----------|
| **web-researcher** | 通用网页爬取 | 临时研究、任意网站 |
| **docs-sync** | 框架文档系统化爬取 | 需要生成结构化文档时 |

## 检查清单

- [ ] 确认 URL 可访问
- [ ] 选择合适的爬取模式（单页/站点）
- [ ] 设置合理的深度和页面数
- [ ] 成功获取页面内容
- [ ] 提取了关键信息
- [ ] 回答了用户问题
- [ ] 提供了结构化输出
