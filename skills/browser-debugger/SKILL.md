---
name: browser-debugger
description: "浏览器错误捕获 - 自动捕获浏览器 Console 错误、网络请求失败、页面异常等信息。使用 Playwright 监听控制台和网络事件"
model: sonnet
user-invocable: true
---

# 浏览器错误捕获

自动捕获浏览器 Console 错误、网络请求失败、页面异常等信息。

## 核心功能

| 功能 | 说明 |
|------|------|
| **Console 捕获** | 监听 console.log/error/warn 等 |
| **网络请求** | 捕获失败的 API 请求 |
| **页面异常** | 捕获 JavaScript 错误 |
| **截图功能** | 错误发生时自动截图 |
| **HAR 导出** | 导出完整网络请求记录 |

## 使用方式

### 1. 命令行使用

```bash
# 捕获单个页面的错误
python3 scripts/web/browser-capture.py https://example.com

# 捕获并导出 HAR
python3 scripts/web/browser-capture.py https://example.com --har output.har

# 截图保存
python3 scripts/web/browser-capture.py https://example.com --screenshot error.png
```

### 2. Skill 调用

在需要调试浏览器错误时，coordinator 会自动调度此 skill。

## 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 要访问的 URL | - |
| `--wait` | 等待秒数 | 5 |
| `--har` | 导出 HAR 文件 | - |
| `--screenshot` | 错误时截图 | - |
| `--console-only` | 只捕获 console | false |

## 输出格式

### Console 错误

```json
{
  "type": "console",
  "level": "error",
  "message": "Failed to load resource: net::ERR_CONNECTION_REFUSED",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 网络请求失败

```json
{
  "type": "network",
  "method": "GET",
  "url": "https://api.example.com/users",
  "status": 500,
  "response": "Internal Server Error",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 页面异常

```json
{
  "type": "page-error",
  "message": "Uncaught TypeError: Cannot read property 'foo' of undefined",
  "stack": "at Object.<anonymous> (/app.js:10:5)",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 使用场景

### 场景 1：API 报错

```
用户：登录接口报错了，帮我看看

执行：
python3 scripts/web/browser-debugger.py http://localhost:3000/api/login

产出：
[ERROR] GET /api/login - 401 Unauthorized
[CONSOLE] Error: Invalid credentials
```

### 场景 2：页面加载失败

```
用户：首页加载不出来

执行：
python3 scripts/web/browser-debugger.py http://localhost:3000 --screenshot error.png

产出：
[PAGE-ERROR] Failed to load script bundle.js
[Screenshot] saved to error.png
```

### 场景 3：调试用户流程

```
用户：提交表单后有错误

执行：
python3 scripts/web/browser-debugger.py http://localhost:3000/form --har form-debug.har

产出：
[NETWORK] POST /api/submit - 422 Validation Error
[CONSOLE] ValidationError: email is required
```

## 与 debugger 的关系

| 工具 | 职责 |
|------|------|
| **browser-debugger** | 捕获浏览器错误信息 |
| **debugger** | 分析错误原因，定位代码 Bug |

**工作流**：
1. browser-debugger 捕获错误
2. 将错误信息交给 debugger
3. debugger 分析并修复代码

## 检查清单

- [ ] 确认 URL 可访问
- [ ] 成功捕获 Console 错误
- [ ] 成功捕获网络请求失败
- [ ] 成功捕获页面异常
- [ ] 提供了完整的错误信息
- [ ] 如需要，提供了截图或 HAR
