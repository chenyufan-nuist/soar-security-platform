# 🛡️ SOAR — 中小企业安全事件自动化响应平台

面向中小企业的轻量级安全编排自动化与响应（SOAR）平台，实现从告警接入、威胁情报查询到自动响应处置与工单闭环的全流程自动化。

---

## 🚀 快速启动

### 前置要求
- Python 3.8+ / pip
- Node.js 14+ / npm

### 方式一：一键启动（Windows）

```bash
.\start.bat
```

脚本会自动创建虚拟环境、安装依赖、启动后端（8000 端口）和前端（5173 端口）。

### 方式二：手动启动

**后端：**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**前端（新终端）：**
```bash
cd frontend
npm install
npm run dev
```

### 方式三：Docker

```bash
docker-compose up
```

---

## 🎬 演示操作步骤

### 录制前准备

清空旧数据（可选，确保界面干净从零开始）：

```powershell
Remove-Item backend/soar.db -ErrorAction SilentlyContinue
```

### 第一步：启动系统

运行 `.\start.bat` 或手动启动前后端。打开浏览器访问 **http://localhost:5173**，仪表盘各项统计应为 0。

### 第二步：发送模拟攻击告警

新建终端，运行演示脚本：

```bash
python demo.py
```

控制台将输出两条告警：一条钓鱼邮件攻击、一条勒索软件攻击。

### 第三步：执行响应策略

1. 切回浏览器，进入 **Threat Alerts** 页面查看告警
2. 进入 **Automation Engine** 页面
3. 在 `Target Alert ID` 中选择告警，在 `Playbook Module` 中选择对应策略
4. 点击 **AUTHORIZE DEPLOYMENT** 执行
5. 观察弹窗中每一步执行结果（威胁情报查询 → 自动封禁/隔离 → 通知 → 生成工单）
6. 切换到 **Dispatch Center** 查看自动生成的处置工单

### 模拟攻击场景

| 场景 | 告警类型 | IOC | 演示策略 |
|------|---------|-----|---------|
| 钓鱼邮件 | phishing | http://fake-login-portal.com | phishing_response |
| 勒索软件 | ransomware | 45.77.12.8 | ransomware_response |

---

## 📡 API 参考

### 告警

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/alert` | 接收安全告警 |
| GET | `/api/alerts?limit=10&type=phishing` | 获取告警列表（支持分页和类型筛选） |
| GET | `/api/alert/{id}` | 获取单个告警详情 |
| GET | `/api/alerts/stats` | 告警统计（总数/未处理/已解决/按类型） |

**提交告警示例：**
```bash
curl -X POST "http://localhost:8000/api/alert" \
  -H "Content-Type: application/json" \
  -d '{"type":"phishing","source":"email_gateway","user":"finance@company.com","ioc":"http://fake-login-portal.com","severity":"high"}'
```

### 工单

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ticket` | 创建工单 |
| GET | `/api/tickets?limit=10&status=open` | 获取工单列表 |
| GET | `/api/ticket/{id}` | 获取工单详情 |
| PUT | `/api/ticket/{id}` | 更新工单（状态/经办人/报告） |

### 响应策略

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/playbook/run` | 执行响应策略 |
| GET | `/api/playbooks` | 获取所有活跃策略 |
| GET | `/api/playbook/{id}` | 获取策略详情 |

**执行策略示例：**
```bash
curl -X POST "http://localhost:8000/api/playbook/run" \
  -H "Content-Type: application/json" \
  -d '{"alert_id":1,"playbook_name":"phishing_response"}'
```

### 系统

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/docs` | Swagger API 文档 |

---

## 📁 项目结构

```
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI 应用入口
│   │   ├── database.py             # 数据库配置 (SQLAlchemy)
│   │   ├── models.py               # 数据模型 (Alert/Ticket/Playbook/ExecutionLog)
│   │   ├── schemas.py              # Pydantic 请求/响应模型
│   │   └── services/
│   │       ├── alert_service.py    # 告警服务（去重/分类）
│   │       ├── playbook_engine.py  # 响应策略执行引擎
│   │       └── misp_service.py     # 威胁情报服务（MISP 接口）
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.vue       # 全局态势仪表盘
│   │   │   ├── AlertList.vue       # 威胁告警列表
│   │   │   ├── TicketManagement.vue # 工单调度中心
│   │   │   ├── PlaybookRunner.vue  # 自动化引擎
│   │   │   └── AgentChat.vue       # 智能助手
│   │   ├── App.vue                 # 根组件
│   │   └── main.js
│   ├── vite.config.js
│   └── Dockerfile
├── demo.py                         # 模拟攻击告警生成脚本
├── start.bat                       # 一键启动脚本
├── docker-compose.yml
├── 中小企业安全事件自动化响应平台_SOAR_设计文档.md
└── README.md
```

---

## 🛠 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 后端框架 | FastAPI | 高性能异步 API |
| ORM | SQLAlchemy | 数据持久化 |
| 数据库 | SQLite | 轻量级零配置（可切换 MySQL） |
| 前端框架 | Vue 3 | 响应式交互界面 |
| 构建工具 | Vite | 快速开发与构建 |
| HTTP 客户端 | Axios | API 通信 |
| 容器化 | Docker + Docker Compose | 一键部署 |

---

## 🔧 常见问题

**Q: 后端无法连接？**
A: 确保已启动 FastAPI 服务且 8000 端口未被占用。

**Q: 前端 CORS 错误？**
A: 后端已配置全开放 CORS，确保从 http://localhost:5173 访问。

**Q: 如何重置数据？**
A: 删除 `backend/soar.db` 文件后重启后端，数据库将自动重建。

**Q: 智能助手无法使用？**
A: 检查 `backend/.env` 中 `DEEPSEEK_API_KEY` 是否已配置有效密钥。

---

## 🔮 后续优化方向

- 可视化策略编排（拖拽式设计）
- 智能风险评分与推荐
- 多租户隔离支持
- 钉钉/企业微信实时告警推送
- 处置动作回滚机制

---

**信息安全竞赛作品 · SOAR 安全运营平台**
