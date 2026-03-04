#!/usr/bin/env bash
# 学习数据收集 - SessionStart 钩子
# 初始化学习数据收集

set -euo pipefail

# 用户数据目录
USER_DATA_DIR="${HOME}/.claude/ai-assistant"
mkdir -p "${USER_DATA_DIR}"
mkdir -p "${USER_DATA_DIR}/task-history"
mkdir -p "${USER_DATA_DIR}/patterns"

# 初始化用户画像（如果不存在）
PROFILE_FILE="${USER_DATA_DIR}/user-profile.json"
if [ ! -f "$PROFILE_FILE" ]; then
    cat > "$PROFILE_FILE" << 'EOF'
{
  "version": "1.0",
  "created": "2026-03-04",
  "updated": "2026-03-04",
  "preferences": {
    "codeStyle": "简洁优先",
    "verification": {
      "minCoverage": 80,
      "skipE2E": [],
      "alwaysReview": []
    },
    "communication": {
      "detailLevel": "简洁",
      "autoQuiet": [],
      "confirmBefore": []
    }
  },
  "patterns": {
    "taskTypes": {},
    "interventions": [],
    "successPatterns": [],
    "failurePatterns": []
  },
  "statistics": {
    "totalTasks": 0,
    "completedTasks": 0,
    "failedTasks": 0,
    "avgTaskDuration": 0,
    "totalSessions": 0
  }
}
EOF
fi

# 记录会话开始
SESSION_FILE="${USER_DATA_DIR}/current-session.json"
cat > "$SESSION_FILE" << EOF
{
  "startTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "project": "${CLAUDE_PROJECT_DIR:-unknown}",
  "tasks": []
}
EOF

# 更新统计
python3 -c "
import json
import os

profile_file = os.path.expanduser('~/.claude/ai-assistant/user-profile.json')
if os.path.exists(profile_file):
    with open(profile_file, 'r') as f:
        profile = json.load(f)
    profile['statistics']['totalSessions'] = profile['statistics'].get('totalSessions', 0) + 1
    profile['updated'] = '$(date -u +"%Y-%m-%d")'
    with open(profile_file, 'w') as f:
        json.dump(profile, f, indent=2)
" 2>/dev/null || true

exit 0
