# 🚀 快速启动指南

## 5 分钟内开始使用 SOAR 平台

### 前置条件
- Python 3.8+
- npm + Node.js（用于前端，可选）

---

## 方式 1：仅启动后端（推荐用于演示）

### 步骤 1：安装依赖（首次）
```bash
cd d:\信息作品竞赛\backend
pip install -r requirements.txt
```

### 步骤 2：启动服务
```bash
python -m uvicorn app.main:app --host localhost --port 8000 --reload
```

✅ 后端已启动 → http://localhost:8000

### 步骤 3：验证 API
回到项目根目录后，在新的终端中运行演示脚本：
```bash
cd d:\信息作品竞赛
python demo.py
```

---

## 方式 2：完整启动（后端 + 前端）

### 第一步：启动后端（在 Terminal 1）
```bash
cd d:\信息作品竞赛\backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host localhost --port 8000 --reload
```

### 第二步：启动前端（在 Terminal 2）
```bash
cd d:\信息作品竞赛\frontend
npm.cmd install
npm.cmd run dev
```

✅ 前端已启动 → http://localhost:5173

---

## 快速演示（30 秒）

### 提交测试告警
```python
import requests

# 提交钓鱼告警
requests.post("http://localhost:8000/api/alert", json={
    "type": "phishing",
    "source": "email_gateway",
    "user": "test@company.com",
    "ioc": "http://malicious.com",
    "severity": "high"
})

# 获取告警列表
response = requests.get("http://localhost:8000/api/alerts")
print(response.json())
```

### 执行自动响应
```python
# 执行剧本
requests.post("http://localhost:8000/api/playbook/run", json={
    "alert_id": 1,
    "playbook_name": "phishing_response"
})
```

---

## 完整系统文件清单

```
d:\信息作品竞赛\
│
├── 📋 README.md                          # 完整文档
├── 🚀 QUICKSTART.md                      # 本文件
├── 🎬 demo.py                            # 自动演示脚本
├── 🎯 中小企业安全事件自动化响应...SOAR_设计文档.md
│
├── 📁 backend/
│   ├── app/
│   │   ├── main.py                       # FastAPI 主程序（核心）
│   │   ├── database.py                   # 数据库配置
│   │   ├── models.py                     # 数据模型
│   │   ├── schemas.py                    # API 规范
│   │   ├── services/
│   │   │   ├── alert_service.py          # 告警逻辑
│   │   │   ├── playbook_engine.py        # 剧本执行引擎（核心）
│   │   │   └── misp_service.py           # 威胁情报接口
│   │   └── api/
│   └── requirements.txt
│
├── 📁 frontend/
│   ├── src/
│   │   ├── App.vue                       # 主组件
│   │   ├── main.js                       # 入口文件
│   │   └── components/
│   │       ├── Dashboard.vue             # 仪表盘
│   │       ├── AlertList.vue             # 告警列表
│   │       ├── TicketManagement.vue      # 工单管理
│   │       └── PlaybookRunner.vue        # 剧本执行
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
```

---

## 核心 API 端点

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | /api/alert | 接收告警 |
| GET | /api/alerts | 告警列表 |
| GET | /api/alerts/stats | 统计信息 |
| POST | /api/playbook/run | 执行剧本 |
| GET | /api/tickets | 工单列表 |
| POST | /api/ticket | 创建工单 |
| GET | /docs | Swagger 文档 |

---

## 常见问题

### Q: 运行 demo.py 时提示连接失败？
**A:** 确保后端已启动：
```bash
cd d:\信息作品竞赛\backend
python -m uvicorn app.main:app --host localhost --port 8000
```

### Q: 前端无法加载？
**A:** 需要 Node.js，[下载安装](https://nodejs.org/)，然后：
```bash
cd d:\信息作品竞赛\frontend
npm install
npm run dev
```

如果你在 PowerShell 里遇到 `npm.ps1` 执行策略限制，可以改用：
```bash
npm.cmd install
npm.cmd run dev
```

如果你更习惯直接输入 `npm install`，也可以把 Terminal 2 换成 cmd 窗口再执行。

### Q: 如何查看 API 文档？
**A:** 打开 http://localhost:8000/docs（需要后端运行）

### Q: 如何重置所有数据？
**A:** 删除 `backend/soar.db` 文件后重启后端

---

## 演示脚本功能清单

✅ 系统健康检查  
✅ 告警统计展示  
✅ 钓鱼邮件场景演示  
✅ 勒索软件场景演示  
✅ 剧本自动执行  
✅ 工单生成验证  
✅ 响应报告输出  

---

## 下一步

1. **阅读设计文档**：了解系统架构
    直接打开 [中小企业安全事件自动化响应平台_SOAR_设计文档.md](中小企业安全事件自动化响应平台_SOAR_设计文档.md)

2. **查看 API 文档**：http://localhost:8000/docs

3. **启动完整系统**：前端 + 后端

4. **自定义剧本**：编辑 `backend/app/main.py` 中的 playbook 定义

---

## 技术栈

- **后端**：FastAPI + SQLAlchemy + SQLite
- **前端**：Vue3 + Vite + Axios
- **威胁情报**：MISP API 集成（模拟）

---

## 联系与支持

此项目为信息安全竞赛作品。

**快速链接**：
- 后端 API：http://localhost:8000
- 前端应用：http://localhost:5173
- API 文档：http://localhost:8000/docs
- 演示脚本：`python demo.py`

## Windows 推荐启动顺序

1. 先启动后端：`cd d:\信息作品竞赛\backend` 然后 `python -m uvicorn app.main:app --host localhost --port 8000 --reload`
2. 再启动前端：`cd d:\信息作品竞赛\frontend` 然后 `npm install` 和 `npm run dev`
    - 如果你用的是 PowerShell，请改成 `npm.cmd install` 和 `npm.cmd run dev`
3. 最后回到项目根目录运行演示脚本：`cd d:\信息作品竞赛` 然后 `python demo.py`

---

**祝演示顺利！** 🎉
