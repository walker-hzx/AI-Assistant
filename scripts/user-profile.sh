#!/usr/bin/env bash
# 用户画像查看工具
# 显示收集的学习数据

PROFILE_FILE="${HOME}/.claude/ai-assistant/user-profile.json"
HISTORY_DIR="${HOME}/.claude/ai-assistant/task-history"

echo "=== 用户画像 ==="
echo ""

if [ -f "$PROFILE_FILE" ]; then
    python3 << 'PYEOF'
import json
import os
from pathlib import Path

profile_file = os.path.expanduser('~/.claude/ai-assistant/user-profile.json')

if not os.path.exists(profile_file):
    print("暂无数据")
    exit(0)

with open(profile_file, 'r') as f:
    profile = json.load(f)

# 显示基本信息
print(f"版本: {profile.get('version', 'N/A')}")
print(f"创建时间: {profile.get('created', 'N/A')}")
print(f"最后更新: {profile.get('updated', 'N/A')}")
print("")

# 显示偏好
prefs = profile.get('preferences', {})
print("【偏好设置】")
print(f"  代码风格: {prefs.get('codeStyle', 'N/A')}")

comm = prefs.get('communication', {})
print(f"  沟通风格: {comm.get('detailLevel', 'N/A')}")
auto_quiet = comm.get('autoQuiet', [])
if auto_quiet:
    print(f"  自动 quietMode: {', '.join(auto_quiet)}")
print("")

# 显示统计
stats = profile.get('statistics', {})
print("【任务统计】")
print(f"  总任务数: {stats.get('totalTasks', 0)}")
print(f"  完成任务: {stats.get('completedTasks', 0)}")
print(f"  失败任务: {stats.get('failedTasks', 0)}")
print("")

# 显示任务类型分布
patterns = profile.get('patterns', {})
task_types = patterns.get('taskTypes', {})
if task_types:
    print("【任务类型分布】")
    for task_type, data in sorted(task_types.items()):
        count = data.get('count', 0)
        print(f"  {task_type}: {count}")
    print("")

# 显示干预记录
interventions = patterns.get('interventions', [])
if interventions:
    print("【最近干预】")
    for iv in interventions[-5:]:
        print(f"  - {iv.get('step', 'N/A')}: {iv.get('reason', 'N/A')}")
    print("")

# 历史文件数量
history_dir = os.path.expanduser('~/.claude/ai-assistant/task-history')
if os.path.exists(history_dir):
    history_count = len([f for f in os.listdir(history_dir) if f.endswith('.json')])
    print(f"【历史记录】")
    print(f"  已保存会话数: {history_count}")

PYEOF
else
    echo "暂无数据，请先使用插件执行一些任务"
fi

echo ""
echo "数据位置: ~/.claude/ai-assistant/"
