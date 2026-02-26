# Web 爬虫工具

完整的网页爬取和分析工具集。

## 快速开始

### 单页爬取

```bash
python3 scripts/web/fetch-url.py https://example.com
python3 scripts/web/fetch-url.py https://example.com -o result.md
python3 scripts/web/fetch-url.py https://example.com --wait 10
```

### 整站爬取

```bash
# 基础整站爬取
python3 scripts/web/fetch-url.py https://docs.example.com --crawl

# 控制深度和页面数
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 3 -m 100

# 指定输出
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -o docs/
```

### 批量爬取

```bash
# 从文件读取 URL 列表
python3 scripts/web/batch-crawler.py -f urls.txt -o results/
```

## 工具列表

| 工具 | 用途 |
|------|------|
| **fetch-url.py** | 主爬取脚本（单页/整站） |
| **url-pattern-analyzer.py** | URL 模式分析 |
| **batch-crawler.py** | 批量爬取 |
| **structured-extractor.py** | 结构化提取 |
| **report-generator.py** | 报告生成 |

## 高级用法

### 完整工作流

```bash
# 1. 整站爬取
python3 scripts/web/fetch-url.py https://docs.example.com --crawl -d 2 -m 50 -o docs/

# 2. 分析 URL 模式
python3 scripts/web/url-pattern-analyzer.py -f docs/sitemap.json -o analysis.md

# 3. 批量爬取特定模块
python3 scripts/web/batch-crawler.py -f module-urls.txt -o module-docs/

# 4. 生成完整报告
python3 scripts/web/report-generator.py module-docs/crawl-success.json -o report.md
```

### 结构化提取

```bash
# 从页面内容提取代码块、表格、API
python3 scripts/web/structured-extractor.py content.md -o structured.json -j
```

## 输出文件

运行站点爬取后，会生成两个文件：

- `{name}.md` - 所有页面内容合并
- `{name}.sitemap.json` - 站点结构

批量爬取会生成：

- `crawl-success.json` - 成功的结果
- `crawl-failed.json` - 失败的结果
- `crawl.md` - Markdown 格式汇总

## 参数说明

### fetch-url.py

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--crawl` | - | 启用站点爬取 | false |
| `--depth` | `-d` | 爬取深度 | 1 |
| `--max-pages` | `-m` | 最大页面数 | 50 |
| `--concurrency` | `-c` | 并发数 | 3 |
| `--wait` | `-w` | 等待秒数 | 5 |
| `--output` | `-o` | 输出文件/目录 | stdout |
| `--list` | `-l` | URL 列表文件 | - |