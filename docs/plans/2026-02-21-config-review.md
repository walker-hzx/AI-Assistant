# AI-Assistant 配置全面检查计划

## 计划目标

全面检查 AI-Assistant 项目配置，找出可优化点、调整点和缺失项。

## 检查范围

### 1. Agents 检查

| 文件 | 检查内容 |
|------|----------|
| planner.md | 硬编码、逻辑完整性 |
| architect.md | 硬编码、模式通用性 |
| code-reviewer.md | 检查清单完整性 |
| tdd-guide.md | 框架通用性、示例代码 |
| e2e-runner.md | 配置完整性、超时设置 |
| security-reviewer.md | 硬编码、安全检查项 |

### 2. Skills 检查

| 文件 | 检查内容 |
|------|----------|
| brainstorming.md | 流程完整性 |
| writing-plans.md | 计划模板、风险评估 |
| executing-plans.md | 混合执行、里程碑评审 |
| verification-before-completion.md | 验证清单 |
| execution-validation.md | 需求对照 |

### 3. Commands 检查

检查是否有未文档化的命令或需要优化的命令。

### 4. Hooks 检查

检查 hooks 配置是否完整、合理。

## 任务列表

### 任务 1: 检查 agents 文件

- [ ] 逐个读取 agents 文件
- [ ] 识别硬编码内容
- [ ] 识别可优化点

### 任务 2: 检查 skills 文件

- [ ] 逐个读取 skills 文件
- [ ] 检查流程完整性
- [ ] 识别可优化点

### 任务 3: 检查 commands 目录

- [ ] 列出所有 commands
- [ ] 检查是否有缺失

### 任务 4: 检查 hooks 配置

- [ ] 读取 hooks 配置
- [ ] 检查触发时机是否合理

### 任务 5: 汇总问题

- [ ] 创建问题清单文件
- [ ] 分类：硬编码、优化点、缺失项
- [ ] 标注优先级

## 输出

生成 `docs/plans/YYYY-MM-DD-config-review.md` 问题清单文件。
