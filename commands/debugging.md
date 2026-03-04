---
name: debugging
description: "调试 - 科学定位 bug，分析根因，给出修复方案"
context: fork
skill: coordinator
---

# 调试专家

**【重要】此命令通过 Skill 智能调度执行**

使用 `/debugging` 进行系统化的错误定位和修复，coordinator 会智能调度。

## 使用方式

```
/debugging
/debugging 登录报错
```

## 调试方法

1. **复现问题** - 确认能稳定复现
2. **收集信息** - 错误消息、堆栈跟踪、环境信息
3. **形成假设** - 基于信息的推理
4. **验证假设** - 设计实验验证
5. **修复问题** - 最小改动原则
6. **确认修复** - 重新测试确保问题解决

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析问题
- 决定是否需要 debugger
- 调度合适的角色修复
