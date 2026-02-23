#!/usr/bin/env python3
"""
代码索引扫描工具
扫描项目代码，生成索引文件
"""

import os
import json
from pathlib import Path


# 扫描规则配置
SCAN_RULES = {
    "frontend": {
        "tools": {
            "patterns": ["utils/*.ts", "utils/*.js", "helpers/*.ts", "composables/*.ts"],
            "description": "工具函数"
        },
        "components": {
            "patterns": ["components/**/*.vue", "components/**/*.tsx"],
            "description": "组件"
        },
        "api": {
            "patterns": ["api/*.ts", "services/*.ts"],
            "description": "API 服务"
        },
        "hooks": {
            "patterns": ["hooks/*.ts", "composables/*.ts"],
            "description": "组合式函数"
        }
    },
    "backend": {
        "services": {
            "patterns": ["services/*.py", "service/*.py"],
            "description": "服务层"
        },
        "repositories": {
            "patterns": ["repositories/*.py", "repo/*.py"],
            "description": "仓储层"
        },
        "models": {
            "patterns": ["models/*.py"],
            "description": "数据模型"
        },
        "schemas": {
            "patterns": ["schemas/*.py", "schemas/*.pydantic.py"],
            "description": "Pydantic 模型"
        },
        "api": {
            "patterns": ["api/**/*.py"],
            "description": "API 路由"
        }
    }
}


def scan_directory(base_path, patterns):
    """扫描目录获取文件列表"""
    files = []
    for pattern in patterns:
        path = Path(base_path) / pattern
        for match in path.parent.glob(path.name):
            if match.is_file():
                files.append(str(match.relative_to(base_path)))
    return files


def scan_project(base_path):
    """扫描整个项目"""
    index = {
        "project": str(base_path),
        "frontend": {},
        "backend": {}
    }

    # 扫描前端代码
    for category, config in SCAN_RULES["frontend"].items():
        files = scan_directory(base_path / "src", config["patterns"])
        if files:
            index["frontend"][category] = {
                "description": config["description"],
                "files": sorted(files)
            }

    # 扫描后端代码
    for category, config in SCAN_RULES["backend"].items():
        files = scan_directory(base_path / "src", config["patterns"])
        if files:
            index["backend"][category] = {
                "description": config["description"],
                "files": sorted(files)
            }

    return index


def generate_markdown(index):
    """生成 Markdown 格式的索引"""
    lines = ["# 代码索引\n", "> 自动生成的代码索引文件\n"]

    # 前端
    if index.get("frontend"):
        lines.append("## 前端\n")
        for category, data in index["frontend"].items():
            lines.append(f"### {data['description']}\n")
            for f in data["files"]:
                lines.append(f"- `{f}`")
            lines.append("")

    # 后端
    if index.get("backend"):
        lines.append("## 后端\n")
        for category, data in index["backend"].items():
            lines.append(f"### {data['description']}\n")
            for f in data["files"]:
                lines.append(f"- `{f}`")
            lines.append("")

    return "\n".join(lines)


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scan.py <project_path>")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: {project_path} does not exist")
        sys.exit(1)

    # 扫描项目
    index = scan_project(project_path)

    # 输出 JSON
    print(json.dumps(index, ensure_ascii=False, indent=2))

    # 生成 Markdown
    md = generate_markdown(index)
    print("\n--- Markdown ---\n")
    print(md)


if __name__ == "__main__":
    main()
