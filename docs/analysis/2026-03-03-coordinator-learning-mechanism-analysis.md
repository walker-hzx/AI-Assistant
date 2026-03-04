# 管家智能调度学习进化机制深度分析

> 分析日期：2026-03-03
> 分析范围：coordinator 调度系统的学习进化机制设计
> 分析师：策略分析师

---

## 执行摘要

本报告针对管家智能调度系统的"学习进化机制"进行深度分析。核心问题是：**每次任务都从零开始，经验无法积累**。通过系统性的分析，本报告提出完整的学习框架设计，包括数据模型、检索算法、集成方案和风险规避策略。

**关键结论**：
- 学习的本质是建立「任务特征 → 决策 → 结果」的映射关系
- 存储应采用「执行记录 + 模式库」双层结构
- 应用的核心是相似度匹配 + 规则推理
- 闭环形成的难点在于避免"学坏"和验证学习效果

---

## 一、问题本质分析

### 1.1 表面问题 vs 根本问题

| 层面 | 描述 |
|------|------|
| **表面问题** | 每次任务都从零开始，之前的经验无法复用 |
| **根本问题** | 缺乏「经验积累 → 模式提取 → 智能应用」的闭环机制 |
| **关联问题** | 任务理解自动化的输出（任务画像）未被用于历史经验匹配 |

### 1.2 现有系统的能力与缺失

**已实现**：
- 任务理解自动化（2.47.0）：自动识别任务类型、复杂度、影响范围
- 执行监控增强（2.48.0）：进度预警、偏差检测、质量前移

**缺失**：
- 历史执行数据的结构化存储
- 任务特征到决策的映射关系记录
- 基于历史经验的智能建议机制

### 1.3 学习的价值

| 维度 | 价值 |
|------|------|
| **效率提升** | 相似任务可直接参考历史方案，减少重复分析 |
| **质量提升** | 从失败中学习，避免重复犯同样的错误 |
| **智能化** | 逐步从"规则调度"向"经验驱动"演进 |

---

## 二、学习什么？（知识维度）

### 2.1 三类知识

```
学习内容
├── 成功经验
│   ├── 流程组合：什么类型的任务用了什么流程
│   ├── Subagent选择：什么场景选择了什么角色
│   ├── 时间预估：实际执行时间 vs 预估时间的规律
│   └── 产出模式：成功任务的产出物特征
│
├── 失败教训
│   ├── 错误模式：哪些决策导致了失败
│   ├── 预警信号：失败前有哪些可识别的征兆
│   ├── 恢复策略：失败后如何成功修复
│   └── 边界条件：什么情况下会触发问题
│
└── 决策上下文
    ├── 任务特征：输入描述 → 提取的特征
    ├── 决策过程：特征 → 选择的方案
    └── 结果映射：方案 → 最终结果
```

### 2.2 知识粒度设计

| 知识类型 | 粒度 | 举例 |
|----------|------|------|
| 流程组合 | 任务类型 → 流程模板 | Bug修复 → 调试→执行→验证 |
| Subagent选择 | 任务特征 → 角色选择 | 涉及UI → 调度ui-ux-reviewer |
| 时间预估 | 任务复杂度 → 时间规律 | 复杂度3 → 平均耗时X分钟 |
| 错误模式 | 错误类型 → 解决方案 | 验证失败 → 检查依赖→重试 |

---

## 三、存储什么？（数据模型）

### 3.1 存储架构设计

```
学习存储系统
├── 执行记录库（原始数据）
│   ├── 每个任务的完整执行轨迹
│   └── 结构化存储，便于检索
│
├── 模式库（提炼知识）
│   ├── 流程模式：任务类型 → 标准流程
│   ├── 角色模式：任务特征 → 推荐角色
│   ├── 时间模式：复杂度 → 预估公式
│   └── 错误模式：错误类型 → 解决方案
│
└── 索引（加速检索）
    ├── 任务特征索引
    ├── 时间序列索引
    └── 标签索引
```

### 3.2 执行记录数据结构

```typescript
// 执行记录 - 每个任务完成后自动记录
interface ExecutionRecord {
  // 任务画像（输入）
  taskProfile: {
    id: string;                      // 唯一标识
    rawInput: string;                // 用户原始输入
    taskType: TaskType;              // 任务类型
    complexity: number;               // 复杂度 1-5
    scope: Scope;                     // 影响范围
    reversibility: Reversibility;     // 可逆性
    riskLevel: number;                // 风险等级 0-1
    keywords: string[];              // 关键词
    confidence: number;               // 识别置信度
  };

  // 决策过程
  decision: {
    selectedFlow: string[];           // 选择的流程步骤
    selectedAgents: Agent[];          // 选择的Subagent
    estimatedTime: number;            // 预估时间（分钟）
    milestones: Milestone[];         // 里程碑设计
  };

  // 执行过程
  execution: {
    actualTime: number;               // 实际时间（分钟）
    agentCalls: AgentCall[];         // Subagent调用记录
    retryCount: number;              // 重试次数
    warnings: Warning[];             // 预警记录
    issues: Issue[];                // 遇到的问题
  };

  // 执行结果
  result: {
    status: 'success' | 'failed' | 'partial';
    outputs: Output[];               // 产出物
    verificationPassed: boolean;      // 验证是否通过
    reviewPassed: boolean;           // 审查是否通过
    lessons: string[];              // 经验教训（成功后填写）
    errorPatterns: string[];        // 错误模式（失败后填写）
  };

  // 元数据
  metadata: {
    createdAt: string;               // 创建时间
    completedAt: string;              // 完成时间
    duration: number;                 // 总耗时（分钟）
    version: string;                 // 记录版本
  };
}
```

### 3.3 模式库数据结构

```typescript
// 流程模式 - 从成功经验中提炼
interface FlowPattern {
  id: string;
  taskType: TaskType;                // 适用任务类型
  conditions: TaskCondition[];       // 适用条件
  flow: string[];                    // 标准流程步骤
  successRate: number;               // 历史成功率
  sampleCount: number;               // 样本数量
  lastUpdated: string;               // 最后更新时间
}

// 角色模式 - 从执行记录中提炼
interface RolePattern {
  id: string;
  trigger: TaskFeature;              // 触发特征
  recommendedAgent: Agent;          // 推荐角色
  successRate: number;              // 使用该角色的成功率
  alternativeAgents: Agent[];      // 备选角色
}

// 时间模式 - 从时间数据中提炼
interface TimePattern {
  id: string;
  complexity: number;               // 复杂度
  taskType: TaskType;
  avgTime: number;                   // 平均时间
  variance: number;                  // 时间方差
  confidence: number;                // 置信度
}

// 错误模式 - 从失败教训中提炼
interface ErrorPattern {
  id: string;
  errorType: string;                 // 错误类型
  symptoms: string[];               // 症状特征
  rootCause: string;                 // 根本原因
  solutions: Solution[];            // 解决方案
  frequency: number;                 // 发生频率
  severity: 'low' | 'medium' | 'high';
}
```

### 3.4 存储介质选择

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **JSON文件** | 简单、无需额外依赖 | 检索慢、大量数据性能差 | 初期验证 |
| **SQLite** | 轻量、支持SQL检索 | 并发能力有限 | 单用户场景 |
| **PostgreSQL** | 功能强大、可扩展 | 需要额外服务 | 生产环境 |

**推荐方案**：初期使用JSON文件（`docs/coordinator/learning/`），验证可行性后迁移到SQLite/PostgreSQL。

---

## 四、如何应用？（检索与应用）

### 4.1 检索流程

```
新任务输入
    ↓
任务理解自动化 → 提取任务画像
    ↓
相似任务检索
    ├── 特征提取：taskType + complexity + scope + keywords
    ├── 相似度计算：余弦相似度 / Jaccard相似度
    └── Top-K 匹配：返回最相似的N个历史任务
    ↓
模式匹配
    ├── 流程模式匹配：查找相同任务类型的标准流程
    ├── 角色模式匹配：查找相似特征的角色选择
    └── 时间模式匹配：查找相似复杂度的时间预估
    ↓
建议生成
    ├── 流程建议：推荐的标准流程
    ├── 角色建议：推荐的Subagent
    └── 预估时间：基于历史的预估
```

### 4.2 相似度计算算法

```typescript
// 任务相似度计算
function calculateSimilarity(taskA: TaskProfile, taskB: TaskProfile): number {
  // 1. 任务类型权重
  const typeWeight = 0.3;
  const typeSimilarity = taskA.taskType === taskB.taskType ? 1 : 0;

  // 2. 复杂度距离（归一化）
  const complexityWeight = 0.2;
  const complexitySimilarity = 1 - Math.abs(taskA.complexity - taskB.complexity) / 4;

  // 3. 范围相似度
  const scopeWeight = 0.2;
  const scopeMap = { 'single-file': 1, 'module': 2, 'cross-module': 3, 'system': 4 };
  const scopeSimilarity = 1 - Math.abs(scopeMap[taskA.scope] - scopeMap[taskB.scope]) / 3;

  // 4. 关键词重叠度（Jaccard）
  const keywordWeight = 0.3;
  const setA = new Set(taskA.keywords);
  const setB = new Set(taskB.keywords);
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  const keywordSimilarity = intersection.size / union.size;

  // 5. 加权求和
  return typeWeight * typeSimilarity +
         complexityWeight * complexitySimilarity +
         scopeWeight * scopeSimilarity +
         keywordWeight * keywordSimilarity;
}

// 阈值设定
const SIMILARITY_THRESHOLD = 0.7;    // 相似度 >= 0.7 认为相似
const MIN_SAMPLE_COUNT = 3;          // 至少3个样本才可靠
```

### 4.3 应用规则

```typescript
// 智能建议生成
function generateSuggestions(task: TaskProfile, similarTasks: ExecutionRecord[]): Suggestion {
  const suggestions: Suggestion = {
    flow: null,
    agents: [],
    estimatedTime: null,
    warnings: [],
    confidence: 0
  };

  // 1. 流程建议
  if (similarTasks.length >= MIN_SAMPLE_COUNT) {
    const flowPatterns = extractFlowPatterns(similarTasks);
    const bestFlow = flowPatterns.sort((a, b) => b.successRate - a.successRate)[0];
    if (bestFlow && bestFlow.successRate >= 0.8) {
      suggestions.flow = bestFlow.flow;
      suggestions.confidence += 0.3;
    }
  }

  // 2. 角色建议
  const agentPatterns = extractAgentPatterns(similarTasks);
  suggestions.agents = agentPatterns
    .filter(p => p.successRate >= 0.7)
    .map(p => p.recommendedAgent);

  // 3. 时间预估
  const avgTime = similarTasks.reduce((sum, t) => sum + t.execution.actualTime, 0) / similarTasks.length;
  suggestions.estimatedTime = Math.round(avgTime * 1.2); // 加20%缓冲

  // 4. 风险预警
  const errorPatterns = extractErrorPatterns(similarTasks);
  suggestions.warnings = errorPatterns
    .filter(e => e.severity === 'high')
    .map(e => e.symptoms.join(', '));

  return suggestions;
}
```

### 4.4 建议展示方式

```
【智能建议】（基于 X 个相似任务）

📋 推荐流程：
   步骤1 → 步骤2 → 步骤3（成功率 85%）

🤖 推荐角色：
   • executor（主要执行）
   • qa（验证）

⏱️ 预估时间：
   约 30 分钟（历史平均）

⚠️ 风险提示：
   - 历史任务中有 2 次出现"验证失败"问题
   - 建议提前准备降级方案

【操作选项】
[采用建议] [调整后采用] [忽略建议]
```

---

## 五、闭环如何形成？（持续进化）

### 5.1 完整闭环流程

```
执行阶段
    ↓
【Step 1: 记录】
  - 任务完成后自动生成执行记录
  - 结构化存储到执行记录库
    ↓
【Step 2: 学习】
  - 定期（如每天）运行学习任务
  - 从执行记录中提取模式
  - 更新模式库
    ↓
【Step 3: 应用】
  - 新任务来时检索相似历史
  - 生成智能建议
  - 供调度决策参考
    ↓
【Step 4: 验证】
  - 跟踪应用建议后的执行结果
  - 计算建议准确率
  - 反馈优化模式库
    ↓
返回 Step 1（持续循环）
```

### 5.2 自动学习触发机制

```typescript
// 学习触发条件
const LEARN_TRIGGERS = [
  { type: 'daily', condition: '每天 UTC 0点执行' },
  { type: 'threshold', condition: '执行记录数 >= 10' },
  { type: 'manual', condition: '用户触发学习' }
];

// 学习任务内容
async function runLearningTask() {
  // 1. 加载近期执行记录
  const records = await loadRecentRecords(days = 7);

  // 2. 提取流程模式
  const flowPatterns = extractFlowPatterns(records);

  // 3. 提取角色模式
  const rolePatterns = extractRolePatterns(records);

  // 4. 提取时间模式
  const timePatterns = extractTimePatterns(records);

  // 5. 提取错误模式（从失败任务）
  const errorPatterns = extractErrorPatterns(records.filter(r => r.result.status === 'failed'));

  // 6. 更新模式库
  await updatePatternLibrary({
    flow: flowPatterns,
    role: rolePatterns,
    time: timePatterns,
    error: errorPatterns
  });

  // 7. 记录学习统计
  await recordLearningStats({
    recordsProcessed: records.length,
    patternsUpdated: {
      flow: flowPatterns.length,
      role: rolePatterns.length,
      time: timePatterns.length,
      error: errorPatterns.length
    }
  });
}
```

### 5.3 验证学习效果

```typescript
// 学习效果评估指标
interface LearningMetrics {
  // 建议采纳率
  adoptionRate: number;              // 建议被采纳的比例

  // 建议准确率
  accuracyRate: {
    flow: number;                    // 流程建议准确率
    agent: number;                   // 角色建议准确率
    time: number;                    // 时间预估准确率（±20%误差内）
  };

  // 效果提升
  improvement: {
    avgTimeReduction: number;        // 平均时间减少
    successRateIncrease: number;     // 成功率提升
    retryReduction: number;          // 重试次数减少
  };

  // 模式质量
  patternQuality: {
    coverage: number;                // 模式覆盖率
    confidence: number;              // 模式置信度
    staleness: number;              // 模式陈旧度
  };
}

// 定期生成效果报告
async function generateLearningReport(): Promise<LearningReport> {
  const metrics = await calculateMetrics();
  return {
    period: 'last 7 days',
    metrics,
    recommendations: [
      '流程模式覆盖不足，建议增加 bugfix 类型样本',
      '时间预估偏乐观，建议增加缓冲系数'
    ]
  };
}
```

---

## 六、与现有系统集成

### 6.1 集成架构

```
┌─────────────────────────────────────────────────────────┐
│                    Coordinator                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ 任务理解    │  │ 执行监控    │  │ 学习进化     │   │
│  │ 自动化      │  │ 增强        │  │ （新增）     │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │           │
│         └────────────────┴────────────────┘           │
│                          │                             │
│                          ▼                             │
│  ┌───────────────────────────────────────────────┐   │
│  │              智能建议引擎                      │   │
│  │  • 相似任务检索                                 │   │
│  │  • 模式匹配                                     │   │
│  │  • 建议生成                                     │   │
│  └──────────────────────┬──────────────────────┘   │
└─────────────────────────┼───────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │ 执行记录库 │   │  模式库   │   │   索引    │
   └───────────┘   └───────────┘   └───────────┘
```

### 6.2 集成点

| 阶段 | 集成点 | 功能 |
|------|--------|------|
| 任务理解自动化 | 输出任务画像时 | 触发相似任务检索 |
| 调度决策时 | 生成智能建议 | 提供流程/角色/时间建议 |
| 任务完成时 | 自动记录执行 | 触发学习任务 |
| 定时任务 | 模式提取更新 | 每天/每周运行学习 |

### 6.3 改动范围

| 模块 | 改动内容 | 优先级 |
|------|----------|--------|
| `coordinator/SKILL.md` | 新增学习进化机制说明 | P1 |
| 任务理解自动化模块 | 增加相似任务检索调用 | P1 |
| 执行记录模板 | 扩展字段（learning字段） | P1 |
| 新增学习模块 | 学习引擎核心逻辑 | P1 |
| 存储层 | JSON文件存储实现 | P1 |

---

## 七、潜在风险与规避方案

### 7.1 风险识别矩阵

| 风险类型 | 风险描述 | 可能性 | 影响 | 规避方案 |
|----------|----------|--------|------|----------|
| **数据质量** | 历史数据噪音导致模式错误 | 高 | 高 | 设置样本数量阈值，只用高质量数据 |
| **过拟合** | 模式过于具体，无法泛化 | 中 | 高 | 模式需要跨任务验证，定期清理 |
| **学坏** | 从失败中学习了错误模式 | 中 | 高 | 区分成功/失败模式，标记置信度 |
| **冷启动** | 初期无数据，无法学习 | 高 | 中 | 提供默认模式库作为基础 |
| **性能** | 大量数据检索变慢 | 低 | 中 | 使用索引+缓存，定期优化 |
| **一致性** | 模式库与实际不符 | 中 | 中 | 定期验证+手动审核机制 |

### 7.2 规避方案详解

#### 方案 1：冷启动策略

```
默认模式库（基于专家经验）
├── 流程模式
│   ├── bugfix → [debugger, executor, qa]
│   ├── feature → [requirements-analyst, executor, qa, code-reviewer]
│   └── research → [web-researcher]
│
├── 角色模式
│   ├── 涉及UI → ui-ux-reviewer
│   ├── 涉及安全 → security-reviewer
│   └── 涉及测试 → test-designer
│
└── 时间模式
    ├── 复杂度1 → 5分钟
    ├── 复杂度2 → 15分钟
    ├── 复杂度3 → 30分钟
    └── 复杂度4+ → 60分钟
```

#### 方案 2：防学坏机制

```typescript
// 成功/失败模式分开存储
const patternLibrary = {
  successPatterns: {
    flow: [...],      // 只从成功任务提取
    agent: [...],
    time: [...]
  },
  failurePatterns: {
    errors: [...],    // 专门存储失败模式
    warnings: [...]  // 预警信号
  }
};

// 模式置信度计算
function calculatePatternConfidence(pattern: Pattern): number {
  // 样本数量（越多越可靠）
  const sampleFactor = Math.min(pattern.sampleCount / 10, 1) * 0.4;

  // 一致性（结果越一致越可靠）
  const consistencyFactor = pattern.successRate > 0.8 ? 0.3 : 0.1;

  // 时效性（越新越可靠）
  const recencyFactor = Math.max(0, 1 - daysSinceUpdate / 30) * 0.3;

  return sampleFactor + consistencyFactor + recencyFactor;
}

// 低置信度模式不使用
function usePattern(pattern: Pattern): boolean {
  return pattern.confidence >= 0.6;
}
```

#### 方案 3：验证与反馈

```
验证机制
├── 实时验证
│   ├── 建议被采纳时记录
│   ├── 执行结果回传
│   └── 统计准确率
│
├── 定期审核
│   ├── 每周人工抽检模式质量
│   ├── 发现问题及时修正
│   └── 异常模式加入黑名单
│
└── 兜底策略
    ├── 高风险建议必须人工确认
    ├── 低置信度建议降低权重
    └── 始终保留默认建议
```

---

## 八、实施路线图

### 8.1 分阶段实现

| 阶段 | 时间 | 目标 | 产出 |
|------|------|------|------|
| **Phase 1** | 1周 | 基础能力 | 执行记录自动存储、简单检索 |
| **Phase 2** | 1周 | 模式提取 | 流程/角色模式自动提取 |
| **Phase 3** | 1周 | 智能建议 | 调度时提供建议 |
| **Phase 4** | 1周 | 闭环验证 | 效果评估、持续优化 |

### 8.2 详细计划

```
Phase 1：基础能力（第1周）
├── 数据模型设计
│   ├── 定义执行记录数据结构
│   └── 定义模式库结构
├── 存储实现
│   ├── 创建 docs/coordinator/learning/ 目录
│   └── 实现 JSON 存储/读取逻辑
└── 集成到 Coordinator
    └── 任务完成时自动记录

Phase 2：模式提取（第2周）
├── 流程模式提取
│   ├── 按任务类型分组
│   └── 提取标准流程
├── 角色模式提取
│   ├── 按任务特征分组
│   └── 统计角色成功率
└── 时间模式提取
    ├── 按复杂度分组
    └── 计算时间分布

Phase 3：智能建议（第3周）
├── 相似度算法实现
├── 检索优化（索引）
└── 建议展示UI设计

Phase 4：闭环验证（第4周）
├── 学习效果评估指标
├── 定期报告生成
└── 模式质量维护
```

---

## 九、总结与建议

### 9.1 核心设计要点

| 要点 | 设计 |
|------|------|
| **学习目标** | 流程组合、角色选择、时间预估、错误模式 |
| **存储结构** | 执行记录库 + 模式库双层结构 |
| **检索方式** | 任务特征相似度匹配 |
| **应用方式** | 智能建议 + 规则推理 |
| **闭环机制** | 执行→记录→学习→应用→验证→优化 |

### 9.2 实施建议

1. **从小开始**：先用少量数据验证可行性，再逐步扩展
2. **重视质量**：数据质量是学习效果的基础
3. **持续迭代**：模式需要不断验证和优化
4. **保留兜底**：始终保留默认规则，避免完全依赖学习

### 9.3 预期收益

| 维度 | 预期收益 |
|------|----------|
| **调度效率** | 相似任务参考历史方案，减少分析时间 |
| **执行质量** | 从失败中学习，减少重复错误 |
| **智能化水平** | 从规则驱动向数据驱动演进 |

---

## 附录

### 附录 A：数据结构完整定义

详见第三部分「存储什么？」章节。

### 附录 B：算法伪代码

详见第四部分「如何应用？」章节。

### 附录 C：集成检查清单

```
集成前检查：
[ ] 执行记录数据结构已定义
[ ] 存储目录已创建
[ ] 任务画像字段已标准化
[ ] 模式库结构已设计

集成时检查：
[ ] 任务完成时触发记录
[ ] 检索时传入正确参数
[ ] 建议展示格式统一
[ ] 错误处理完善

集成后检查：
[ ] 数据正确存储
[ ] 检索返回正确结果
[ ] 建议被正确采纳
[ ] 效果指标正常
```

---

*报告结束*
