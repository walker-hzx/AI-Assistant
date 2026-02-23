# 概念搜索学习工具

## 功能

遇到不确定的概念时，搜索并学习。

## 使用方式

```bash
# 基本用法
python scripts/learn-concept/search.py "React hooks"

# 指定优先搜索源
python scripts/learn-concept/search.py "React hooks" "mdn"
python scripts/learn-concept/search.py "React hooks" "wikipedia"
python scripts/learn-concept/search.py "React hooks" "google"
```

## 优先搜索源

| 源 | 说明 | 适用场景 |
|----|------|----------|
| wikipedia | 维基百科 | 通用概念 |
| mdn | MDN Web Docs | Web 技术 |
| google | Google 搜索 | 其他情况 |

## 在对话中调用

遇到不确定的概念时：

1. 先问用户："要不要我搜索学习一下？"
2. 用户同意后，运行脚本
3. 根据返回的 URL 访问学习

## 输出示例

```json
{
  "query": "React hooks",
  "priority_source": "wikipedia",
  "sources": [
    {
      "source": "wikipedia",
      "url": "https://en.wikipedia.org/wiki/React_Hooks"
    },
    {
      "source": "mdn",
      "url": "https://developer.mozilla.org/zh-CN/search?q=React hooks"
    },
    {
      "source": "google",
      "url": "https://www.google.com/search?q=React hooks"
    }
  ]
}
```
