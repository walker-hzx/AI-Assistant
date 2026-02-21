# 文档爬取工具

用于从官网爬取前端框架/组件库文档，生成结构化的 Markdown 参考文档。

## 目录

```
fetch-docs/
├── fetch-headlessui.py    # Headless UI 文档爬取
└── README.md              # 本文件
```

## 输出位置

生成的文档保存在项目根目录：
```
docs/frameworks/
├── headlessui.md         # Headless UI Vue 文档
└── ...                   # 其他框架文档
```

## 使用方法

### Headless UI

```bash
cd scripts/fetch-docs
python3 fetch-headlessui.py
```

输出：`docs/frameworks/headlessui.md`

## 添加新的框架

1. 创建新的爬取脚本 `fetch-{framework}.py`
2. 参考 `fetch-headlessui.py` 的结构
3. 定义该框架的组件列表和选择器规则
4. 运行测试并调整

## 注意事项

- 爬取脚本仅用于 AI-Assistant 项目内部维护
- 不会影响 skills/agents 在其他项目的使用
- 官网结构变化时可能需要更新选择器
- 尊重网站的 robots.txt 和访问频率限制
