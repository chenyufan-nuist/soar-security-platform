# 🛡️ SOAR 平台 - 本地运行指南

## 快速启动（3 分钟内运行）

### 前置要求
- Python 3.8+
- Node.js 14+
- pip 包管理工具
- npm 包管理工具

---

## 方案一：自动启动脚本（推荐）

### Windows 用户

运行 `start.bat` 文件：
```bash
start.bat
```

该脚本会自动：
1. 创建 Python 虚拟环境
2. 安装后端依赖
3. 启动 FastAPI 服务（8000 端口）
4. 安装前端依赖
5. 启动 Vue3 开发服务器（5173 端口）

前端界面已经调整为更像真实安全运营控制台的深色风格，不再突出明显的演示入口。

---

## 方案二：手动启动

### 1. 启动后端服务

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（仅首次）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动 FastAPI 服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**后端已启动** → http://localhost:8000

API 文档查看：http://localhost:8000/docs

---

### 2. 启动前端服务

```bash
# 在新的终端窗口中

# 进入前端目录
cd frontend

# 安装依赖（仅首次）
npm install

# 启动开发服务器
npm run dev
```

**前端已启动** → http://localhost:5173

---

## 使用方式

### 场景 1：钓鱼邮件应对

1. 打开前端界面 http://localhost:5173
2. 进入"剧本执行"页面
3. 在弹窗中点击"创建测试告警"或直接通过 API 提交告警

**API 提交示例：**
```bash
curl -X POST "http://localhost:8000/api/alert" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "phishing",
    "source": "email_gateway",
    "user": "finance@company.com",
    "ioc": "http://fake-login-portal.com",
    "severity": "high"
  }'
```

4. 选择 `phishing_response` 剧本，点击"执行剧本"
5. 观察执行结果和生成的工单

---

### 场景 2：勒索软件告警

**API 提交示例：**
```bash
curl -X POST "http://localhost:8000/api/alert" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "ransomware",
    "source": "edr",
    "host": "PC-009",
    "ioc": "45.77.12.8",
    "severity": "critical"
  }'
```

---

## 项目文件结构

```
d:\信息作品竞赛\
├── backend/                        # FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI 主程序
│   │   ├── database.py             # 数据库配置
│   │   ├── models.py               # 数据模型
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── api/                    # API 路由
│   │   └── services/               # 业务逻辑服务
│   │       ├── alert_service.py    # 告警服务
│   │       ├── playbook_engine.py  # 剧本引擎
│   │       └── misp_service.py     # 威胁情报服务
│   └── requirements.txt            # Python 依赖
│
├── frontend/                       # Vue3 前端
│   ├── src/
│   │   ├── components/             # Vue 组件
│   │   │   ├── Dashboard.vue       # 仪表盘
│   │   │   ├── AlertList.vue       # 告警列表
│   │   │   ├── TicketManagement.vue # 工单管理
│   │   │   └── PlaybookRunner.vue  # 剧本执行
│   │   ├── App.vue                 # 根组件
│   │   └── main.js                 # 入口文件
│   ├── index.html                  # HTML 入口
│   ├── vite.config.js              # Vite 配置
│   └── package.json                # NPM 依赖
│
├── 中小企业安全事件自动化响应平台_SOAR_设计文档.md  # 设计文档
└── README.md                       # 本文档
```

---

## API 端点一览

### 告警相关
- `POST /api/alert` - 接收告警
- `GET /api/alerts` - 获取告警列表
- `GET /api/alert/{id}` - 获取单个告警
- `GET /api/alerts/stats` - 告警统计

### 工单相关
- `POST /api/ticket` - 创建工单
- `GET /api/tickets` - 工单列表
- `GET /api/ticket/{id}` - 工单详情
- `PUT /api/ticket/{id}` - 更新工单

### 剧本相关
- `POST /api/playbook/run` - 执行剧本
- `GET /api/playbooks` - 剧本列表
- `GET /api/playbook/{id}` - 剧本详情

### 系统
- `GET /health` - 健康检查
- `GET /docs` - Swagger API 文档

---

## 常见问题

### Q: 后端无法连接？
A: 确保已运行 `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Q: 前端显示 CORS 错误？
A: 后端已配置 CORS，确保前端访问 http://localhost:5173

### Q: 数据库在哪里？
A: SQLite 数据库文件在 `backend/soar.db`，首次启动自动创建

### Q: 如何重置数据？
A: 删除 `backend/soar.db` 文件，重启后端服务

---

## 讲解口径

> **本系统基于 SOAR 思想，实现了一个轻量级的安全事件自动化响应平台。**
>
> 核心价值：将中小企业常见的安全告警（如钓鱼邮件、勒索软件）转化为可编排、可执行、可追踪的自动化工作流。
>
> **关键特性：**
> 1. 🎯 告警聚合与去重 - 减少告警噪音
> 2. 📜 剧本自动编排 - 标准化处置流程
> 3. 🔗 威胁情报联动 - 基于 MISP 的快速判断
> 4. 📋 工单闭环管理 - 追踪处理全过程
> 5. 📊 可视化仪表盘 - 安全态势一览无余
>
> **通过这个系统，一个 1 人安全团队就能处理原来需要 3-5 人的工作量。**

---

## 后续优化方向

1. **可视化剧本编排**：支持拖拽式剧本设计
2. **AI 智能推荐**：基于历史数据推荐最优响应方案
3. **多租户支持**：为不同的中小企业隔离数据
4. **实时告警推送**：集成钉钉、企业微信通知
5. **响应动作回滚**：支持撤销已执行的动作

---

## 技术栈详解

| 组件 | 技术 | 用途 |
| ---- | ---- | ---- |
| 后端框架 | FastAPI | 高性能 API 服务 |
| 数据存储 | SQLite | 轻量级数据库 |
| 前端框架 | Vue3 | 动态交互界面 |
| 构建工具 | Vite | 快速开发构建 |
| API 通信 | Axios | HTTP 客户端 |

---

## 许可与致谢

本项目为信息安全竞赛作品，展示了 SOAR 平台的核心功能。

联系方式：[你的联系方式]

---

**祝演示顺利！** 🎉
