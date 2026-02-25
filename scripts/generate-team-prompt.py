#!/usr/bin/env python3
"""
团队配置转换脚本
将现有的 teams/ 目录下的配置转换为 Claude Code 可以理解的自然语言描述

用法:
    python3 scripts/generate-team-prompt.py [team-name]

示例:
    python3 scripts/generate-team-prompt.py dev-team
    python3 scripts/generate-team-prompt.py python3 scripts/generate-team-prompt analysis-team
   .py  # 列出所有可用团队
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
TEAMS_DIR = PROJECT_DIR / "teams"

# 内置 agent types 映射
AGENT_TYPE_MAP = {
    "Explore": "research and exploration",
    "Plan": "planning and analysis",
    "general-purpose": "general development work",
    "General Purpose": "general development work",
    "Coder": "coding tasks",
    "Researcher": "research and investigation",
    "Reviewer": "code review",
    "Debugger": "debugging and troubleshooting",
    "Reader": "read-only operations",
    "Writer": "documentation and writing",
}


def get_agent_type_description(agent_type: str) -> str:
    """获取 agent type 的描述"""
    return AGENT_TYPE_MAP.get(agent_type, "general tasks")


def format_members(members: list) -> str:
    """格式化团队成员描述"""
    if not members:
        return ""

    lines = []
    for i, member in enumerate(members, 1):
        name = member.get("name", "Unnamed")
        description = member.get("description", "")
        prompt_file = member.get("prompt", "")

        # 提取 prompt 文件名作为角色描述的补充
        if prompt_file:
            role = prompt_file.replace(".md", "").replace("prompts/", "")
        else:
            role = name.lower()

        line = f"{i}. **{name}**: {description}"
        lines.append(line)

    return "\n".join(lines)


def generate_team_prompt(team_name: str, config: dict) -> str:
    """生成团队创建的提示词"""

    team_name_display = config.get("name", team_name)
    description = config.get("description", "")
    agent_type = config.get("agent_type", "general-purpose")
    members = config.get("members", [])

    # 构建成员列表
    member_list = []
    for member in members:
        name = member.get("name", "")
        description = member.get("description", "")
        if name and description:
            member_list.append(f"- {name}: {description}")

    members_str = "\n".join(member_list) if member_list else "team members"

    # 生成提示词
    prompt = f"""## 团队: {team_name_display}

**描述**: {description}

**Agent 类型**: {agent_type} ({get_agent_type_description(agent_type)})"""

    if members_str:
        prompt += f"""

**团队成员**:
{members_str}"""

    prompt += f"""

---

## 复制以下内容给 Claude:

---

"""

    # 生成可以直接使用的自然语言描述
    prompt += f"""Create an agent team for **{team_name_display}**.

**Team description**: {description}

**Team members** (use these roles and descriptions):
"""

    # 添加每个成员的描述
    for member in members:
        name = member.get("name", "")
        description = member.get("description", "")
        if name and description:
            prompt += f"- **{name}**: {description}\n"

    # 添加团队行为指导
    prompt += """
**Requirements**:
- Each teammate should use Sonnet model for better reasoning
- Lead should coordinate work through the shared task list
- Teammates should communicate directly with each other
- Focus on their specific area of responsibility

---

**Paste the above to Claude Code to create the team.**"""

    return prompt


def list_teams():
    """列出所有可用的团队配置"""
    if not TEAMS_DIR.exists():
        print(f"错误: teams 目录不存在: {TEAMS_DIR}")
        sys.exit(1)

    teams = []
    for item in TEAMS_DIR.iterdir():
        if item.is_dir() and (item / "config.json").exists():
            teams.append(item.name)

    if not teams:
        print("未找到团队配置")
        sys.exit(1)

    print("可用的团队配置:\n")
    for team in sorted(teams):
        print(f"  - {team}")
    print(f"\n用法: python3 {sys.argv[0]} <team-name>")


def main():
    if len(sys.argv) < 2:
        list_teams()
        sys.exit(0)

    team_name = sys.argv[1]
    config_file = TEAMS_DIR / team_name / "config.json"

    if not config_file.exists():
        print(f"错误: 配置文件不存在: {config_file}")
        list_teams()
        sys.exit(1)

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    prompt = generate_team_prompt(team_name, config)
    print(prompt)


if __name__ == "__main__":
    main()
