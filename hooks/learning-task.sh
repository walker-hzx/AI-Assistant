#!/usr/bin/env bash
# 任务数据记录工具
# 用于在任务执行过程中记录学习数据

set -euo pipefail

USER_DATA_DIR="${HOME}/.claude/ai-assistant"
SESSION_FILE="${USER_DATA_DIR}/current-session.json"

# 用法: ./learning-task.sh --type feature --complexity 3 --result completed [--quiet]
usage() {
    echo "Usage: $0 --type <task_type> --complexity <1-5> --result <completed|failed|adjusted> [--quiet]"
    echo "  --type: feature, bugfix, refactor, docs, test, research"
    echo "  --complexity: 1-5"
    echo "  --result: completed, failed, adjusted"
    echo "  --quiet: silent mode"
    exit 1
}

# 解析参数
TYPE=""
COMPLEXITY=0
RESULT=""
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --type) TYPE="$2"; shift 2 ;;
        --complexity) COMPLEXITY="$2"; shift 2 ;;
        --result) RESULT="$2"; shift 2 ;;
        --quiet) QUIET=true; shift ;;
        *) usage ;;
    esac
done

# 验证参数
if [ -z "$TYPE" ] || [ -z "$RESULT" ]; then
    usage
fi

# 读取当前会话
if [ ! -f "$SESSION_FILE" ]; then
    [ "$QUIET" = false ] && echo "No active session"
    exit 0
fi

# 使用 Python 更新会话数据
python3 << PYEOF
import json
import os
import sys
from datetime import datetime

session_file = os.path.expanduser('~/.claude/ai-assistant/current-session.json')

if not os.path.exists(session_file):
    sys.exit(0)

with open(session_file, 'r') as f:
    session = json.load(f)

# 添加任务记录
task = {
    'type': '$TYPE',
    'complexity': $COMPLEXITY,
    'result': '$RESULT',
    'timestamp': datetime.now().isoformat()
}

if 'tasks' not in session:
    session['tasks'] = []

session['tasks'].append(task)

with open(session_file, 'w') as f:
    json.dump(session, f, indent=2)

if not $QUIET:
    print(f"Task recorded: $TYPE ($COMPLEXITY) - $RESULT")
PYEOF

exit 0
