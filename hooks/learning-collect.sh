#!/usr/bin/env bash
# 学习数据收集 - SessionEnd 钩子
# 会话结束时汇总并保存学习数据

set -euo pipefail

USER_DATA_DIR="${HOME}/.claude/ai-assistant"
SESSION_FILE="${USER_DATA_DIR}/current-session.json"
PROFILE_FILE="${USER_DATA_DIR}/user-profile.json"

# 如果没有会话文件，直接退出
if [ ! -f "$SESSION_FILE" ]; then
    exit 0
fi

# 读取会话数据
SESSION_DATA=$(cat "$SESSION_FILE" 2>/dev/null || echo '{}')

# 检查是否有任务记录
if echo "$SESSION_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(1 if not d.get('tasks') else 0)" 2>/dev/null; then
    # 没有任务记录，清理并退出
    rm -f "$SESSION_FILE"
    exit 0
fi

# 更新用户画像
python3 << 'PYEOF'
import json
import os
from datetime import datetime

user_data_dir = os.path.expanduser('~/.claude/ai-assistant')
session_file = os.path.join(user_data_dir, 'current-session.json')
profile_file = os.path.join(user_data_dir, 'user-profile.json')

if not os.path.exists(session_file):
    exit(0)

with open(session_file, 'r') as f:
    session = json.load(f)

# 读取现有画像
profile = {"statistics": {}, "patterns": {"taskTypes": {}}}
if os.path.exists(profile_file):
    with open(profile_file, 'r') as f:
        profile = json.load(f)

# 确保数据结构完整
if 'statistics' not in profile:
    profile['statistics'] = {}
if 'patterns' not in profile:
    profile['patterns'] = {}
if 'taskTypes' not in profile['patterns']:
    profile['patterns']['taskTypes'] = {}

# 更新统计数据
tasks = session.get('tasks', [])
if tasks:
    profile['statistics']['totalTasks'] = profile['statistics'].get('totalTasks', 0) + len(tasks)

    completed = sum(1 for t in tasks if t.get('result') == 'completed')
    failed = sum(1 for t in tasks if t.get('result') == 'failed')

    profile['statistics']['completedTasks'] = profile['statistics'].get('completedTasks', 0) + completed
    profile['statistics']['failedTasks'] = profile['statistics'].get('failedTasks', 0) + failed

# 记录任务类型模式
for task in tasks:
    task_type = task.get('type', 'unknown')
    if task_type not in profile['patterns']['taskTypes']:
        profile['patterns']['taskTypes'][task_type] = {'count': 0, 'totalComplexity': 0}
    profile['patterns']['taskTypes'][task_type]['count'] += 1
    profile['patterns']['taskTypes'][task_type]['totalComplexity'] += task.get('complexity', 0)

# 更新偏好（从会话中收集）
for task in tasks:
    # 收集 quietMode 使用情况
    if task.get('quietMode'):
        prefs = profile.get('preferences', {}).get('communication', {})
        if 'autoQuiet' not in prefs:
            prefs['autoQuiet'] = []
        if task_type not in prefs['autoQuiet']:
            prefs['autoQuiet'].append(task_type)

# 保存更新后的画像
profile['updated'] = datetime.now().strftime('%Y-%m-%d')
with open(profile_file, 'w') as f:
    json.dump(profile, f, indent=2)

# 将会话历史保存到文件
import hashlib
task_hash = hashlib.md5(str(tasks).encode()).hexdigest()[:8]
history_file = os.path.join(user_data_dir, 'task-history', f"{session.get('startTime', 'unknown')}_{task_hash}.json")
os.makedirs(os.path.dirname(history_file), exist_ok=True)
with open(history_file, 'w') as f:
    json.dump(session, f, indent=2)

print(f"Learning data saved: {len(tasks)} tasks")
PYEOF

# 清理当前会话文件
rm -f "$SESSION_FILE"

exit 0
