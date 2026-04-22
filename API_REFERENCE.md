# 📚 SOAR 平台 API 接口文档

**版本**: 1.0.0  
**基础 URL**: `http://localhost:8000`  
**内容类型**: `application/json`

---

## 目录

1. [告警接口](#告警接口)
2. [工单接口](#工单接口)
3. [剧本接口](#剧本接口)
4. [系统接口](#系统接口)

---

## 告警接口

### 1. 接收告警 - POST /api/alert

**描述**: 接收来自外部系统的安全告警

**请求体**:
```json
{
  "type": "phishing",           // 告警类型（必须）
  "source": "email_gateway",    // 告警来源（必须）
  "user": "test@company.com",   // 用户（可选）
  "host": "PC-001",             // 主机名（可选）
  "ioc": "http://malicious.com",// 威胁指标（必须）
  "severity": "high",           // 严重级别（可选）: low, medium, high, critical
  "description": "描述信息"      // 描述（可选）
}
```

**响应** (200 OK):
```json
{
  "id": 1,
  "type": "phishing",
  "source": "email_gateway",
  "user": "test@company.com",
  "host": null,
  "ioc": "http://malicious.com",
  "severity": "high",
  "status": "open",
  "created_at": "2026-04-22T10:00:00",
  "updated_at": "2026-04-22T10:00:00"
}
```

**cURL 示例**:
```bash
curl -X POST "http://localhost:8000/api/alert" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "phishing",
    "source": "email_gateway",
    "user": "test@company.com",
    "ioc": "http://fake-login.com",
    "severity": "high"
  }'
```

---

### 2. 获取告警列表 - GET /api/alerts

**描述**: 分页获取所有告警

**查询参数**:
- `skip` (int): 跳过数量，默认 0
- `limit` (int): 返回数量，默认 10
- `alert_type` (string): 筛选告警类型，可选

**响应** (200 OK):
```json
[
  {
    "id": 1,
    "type": "phishing",
    "source": "email_gateway",
    "user": "test@company.com",
    "ioc": "http://malicious.com",
    "severity": "high",
    "status": "open",
    "created_at": "2026-04-22T10:00:00",
    "updated_at": "2026-04-22T10:00:00"
  }
]
```

**cURL 示例**:
```bash
# 获取前 20 个告警
curl "http://localhost:8000/api/alerts?limit=20"

# 按类型筛选
curl "http://localhost:8000/api/alerts?alert_type=phishing&limit=10"
```

---

### 3. 获取单个告警 - GET /api/alert/{alert_id}

**描述**: 获取特定告警的详情

**路径参数**:
- `alert_id` (int): 告警 ID

**响应** (200 OK):
```json
{
  "id": 1,
  "type": "phishing",
  "source": "email_gateway",
  "user": "test@company.com",
  "ioc": "http://malicious.com",
  "severity": "high",
  "status": "open",
  "created_at": "2026-04-22T10:00:00",
  "updated_at": "2026-04-22T10:00:00"
}
```

**错误** (404 Not Found):
```json
{
  "detail": "告警不存在"
}
```

---

### 4. 告警统计 - GET /api/alerts/stats

**描述**: 获取告警统计信息

**响应** (200 OK):
```json
{
  "total": 5,
  "open": 2,
  "resolved": 3,
  "by_type": {
    "phishing": 2,
    "ransomware": 3
  }
}
```

---

## 工单接口

### 1. 创建工单 - POST /api/ticket

**描述**: 手动创建工单

**请求体**:
```json
{
  "alert_id": 1,                           // 关联告警 ID（必须）
  "title": "钓鱼邮件响应工单",             // 工单标题（必须）
  "description": "需要进一步调查",         // 描述（可选）
  "assignee": "security-admin"             // 负责人（可选）
}
```

**响应** (200 OK):
```json
{
  "id": 1,
  "alert_id": 1,
  "title": "钓鱼邮件响应工单",
  "description": "需要进一步调查",
  "assignee": "security-admin",
  "status": "open",
  "actions": null,
  "report": null,
  "created_at": "2026-04-22T10:00:00",
  "updated_at": "2026-04-22T10:00:00"
}
```

---

### 2. 获取工单列表 - GET /api/tickets

**描述**: 分页获取所有工单

**查询参数**:
- `skip` (int): 跳过数量，默认 0
- `limit` (int): 返回数量，默认 10
- `status` (string): 筛选状态，可选值: open, in_progress, resolved, closed

**响应** (200 OK):
```json
[
  {
    "id": 1,
    "alert_id": 1,
    "title": "钓鱼邮件响应工单",
    "assignee": "security-admin",
    "status": "resolved",
    "actions": "[...]",
    "report": "{...}",
    "created_at": "2026-04-22T10:00:00",
    "updated_at": "2026-04-22T10:05:00"
  }
]
```

---

### 3. 获取单个工单 - GET /api/ticket/{ticket_id}

**描述**: 获取工单详情

**路径参数**:
- `ticket_id` (int): 工单 ID

**响应** (200 OK):
```json
{
  "id": 1,
  "alert_id": 1,
  "title": "钓鱼邮件响应工单",
  "description": "需要进一步调查",
  "assignee": "security-admin",
  "status": "resolved",
  "actions": "[{...}]",
  "report": "{...}",
  "created_at": "2026-04-22T10:00:00",
  "updated_at": "2026-04-22T10:05:00"
}
```

---

### 4. 更新工单 - PUT /api/ticket/{ticket_id}

**描述**: 更新工单信息

**路径参数**:
- `ticket_id` (int): 工单 ID

**请求体** (所有字段可选):
```json
{
  "status": "in_progress",      // 新状态
  "assignee": "new-admin",      // 新负责人
  "report": "处置报告内容"       // 处置报告
}
```

**响应** (200 OK):
```json
{
  "id": 1,
  "alert_id": 1,
  "title": "钓鱼邮件响应工单",
  "status": "in_progress",
  "assignee": "new-admin",
  "report": "处置报告内容",
  "created_at": "2026-04-22T10:00:00",
  "updated_at": "2026-04-22T10:10:00"
}
```

---

## 剧本接口

### 1. 执行剧本 - POST /api/playbook/run

**描述**: 手动触发剧本执行

**请求体**:
```json
{
  "alert_id": 1,                    // 告警 ID（必须）
  "playbook_name": "phishing_response"  // 剧本名称（必须）
}
```

**响应** (200 OK):
```json
{
  "status": "success",
  "playbook": "phishing_response",
  "alert_id": 1,
  "actions": [
    {
      "action": "query_misp",
      "status": "success",
      "message": "查询威胁情报成功: {...}"
    },
    {
      "action": "block_url",
      "status": "success",
      "message": "已封禁 URL: http://malicious.com"
    },
    {
      "action": "notify_user",
      "status": "success",
      "message": "已通知用户: test@company.com"
    },
    {
      "action": "create_ticket",
      "status": "success",
      "message": "已创建工单: 钓鱼攻击响应"
    }
  ],
  "message": "剧本 phishing_response 执行完成"
}
```

**错误** (404 Not Found):
```json
{
  "detail": "告警不存在"
}
```

---

### 2. 获取剧本列表 - GET /api/playbooks

**描述**: 获取所有可用剧本

**响应** (200 OK):
```json
[
  {
    "id": 1,
    "name": "phishing_response",
    "description": "自动应对钓鱼邮件事件",
    "alert_type": "phishing",
    "is_active": true,
    "created_at": "2026-04-22T09:00:00"
  },
  {
    "id": 2,
    "name": "ransomware_response",
    "description": "自动应对勒索软件事件",
    "alert_type": "ransomware",
    "is_active": true,
    "created_at": "2026-04-22T09:00:00"
  }
]
```

---

### 3. 获取单个剧本 - GET /api/playbook/{playbook_id}

**描述**: 获取剧本详情

**路径参数**:
- `playbook_id` (int): 剧本 ID

**响应** (200 OK):
```json
{
  "id": 1,
  "name": "phishing_response",
  "description": "自动应对钓鱼邮件事件",
  "content": "{\"name\": \"phishing_response\", \"steps\": [...]}",
  "alert_type": "phishing",
  "is_active": true,
  "created_at": "2026-04-22T09:00:00",
  "updated_at": "2026-04-22T09:00:00"
}
```

---

## 系统接口

### 1. 健康检查 - GET /health

**描述**: 检查系统健康状态

**响应** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-04-22T10:00:00",
  "service": "SOAR 平台"
}
```

---

### 2. 根路由 - GET /

**描述**: API 文档入口

**响应** (200 OK):
```json
{
  "message": "欢迎使用 SOAR 平台",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

---

## 支持的告警类型

| 类型 | 描述 | 默认响应剧本 |
|------|------|----------|
| phishing | 钓鱼邮件 | phishing_response |
| ransomware | 勒索软件 | ransomware_response |
| malware | 恶意软件 | - |
| suspicious_ip | 可疑 IP | - |

---

## 错误码

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 404 | 资源不存在 |
| 422 | 请求验证失败 |
| 500 | 服务器错误 |

---

## 数据模型参考

### Alert (告警)
```python
{
  "id": int,           # 告警 ID
  "type": str,         # 告警类型
  "source": str,       # 告警来源
  "user": Optional[str],   # 用户
  "host": Optional[str],   # 主机
  "ioc": str,          # 威胁指标
  "severity": str,     # 严重级别
  "status": str,       # 状态
  "created_at": datetime,
  "updated_at": datetime
}
```

### Ticket (工单)
```python
{
  "id": int,
  "alert_id": int,
  "title": str,
  "description": Optional[str],
  "assignee": Optional[str],
  "status": str,       # open, in_progress, resolved, closed
  "actions": Optional[str],  # JSON 格式的动作列表
  "report": Optional[str],   # 处置报告
  "created_at": datetime,
  "updated_at": datetime
}
```

### Playbook (剧本)
```python
{
  "id": int,
  "name": str,
  "description": Optional[str],
  "content": str,      # JSON/YAML 格式
  "alert_type": str,
  "is_active": bool,
  "created_at": datetime,
  "updated_at": datetime
}
```

---

## 快速测试

### Python 客户端
```python
import requests

API = "http://localhost:8000/api"

# 1. 提交告警
alert = requests.post(f"{API}/alert", json={
    "type": "phishing",
    "source": "email_gateway",
    "user": "user@company.com",
    "ioc": "http://malicious.com",
    "severity": "high"
}).json()

# 2. 执行剧本
result = requests.post(f"{API}/playbook/run", json={
    "alert_id": alert["id"],
    "playbook_name": "phishing_response"
}).json()

# 3. 查看工单
tickets = requests.get(f"{API}/tickets").json()
print(tickets)
```

---

## 完整工作流示例

```bash
# 1. 提交告警
curl -X POST "http://localhost:8000/api/alert" \
  -H "Content-Type: application/json" \
  -d '{"type": "phishing", "source": "email", "user": "user@company.com", "ioc": "http://malicious.com", "severity": "high"}'

# 2. 获取告警列表
curl "http://localhost:8000/api/alerts"

# 3. 执行剧本
curl -X POST "http://localhost:8000/api/playbook/run" \
  -H "Content-Type: application/json" \
  -d '{"alert_id": 1, "playbook_name": "phishing_response"}'

# 4. 查看生成的工单
curl "http://localhost:8000/api/tickets"
```

---

## API 在线文档

启动后端后，访问以下 URL 查看交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

**版本**: 1.0.0  
**最后更新**: 2026-04-22  
**状态**: ✅ 生产就绪
