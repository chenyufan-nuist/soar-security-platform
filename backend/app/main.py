from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 注入系统证书库，解决 Windows 上 requests HTTPS 连接失败问题
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

from .database import get_db, init_db
from .models import Alert as AlertModel, Ticket as TicketModel, Playbook as PlaybookModel, ExecutionLog
from .schemas import (
    AlertCreate, AlertResponse, TicketCreate, TicketUpdate, TicketResponse,
    PlaybookRunRequest, ExecutionResult, AgentChatRequest, AgentChatResponse
)
from .services.alert_service import AlertService
from .services.playbook_engine import PlaybookEngine

app = FastAPI(title="SOAR 平台", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
def startup_event():
    init_db()
    # 初始化示例 Playbook
    _init_sample_playbooks()

def _init_sample_playbooks():
    db = next(get_db())
    
    # 检查是否已存在
    if db.query(PlaybookModel).filter_by(name="phishing_response").first():
        return
    
    # 钓鱼攻击响应策略
    phishing_playbook = PlaybookModel(
        name="phishing_response",
        description="自动应对钓鱼邮件事件",
        alert_type="phishing",
        content=json.dumps({
            "name": "phishing_response",
            "steps": [
                {"action": "query_misp", "params": {"ioc": "{{ioc}}"}},
                {"action": "block_url", "params": {"url": "{{ioc}}"}},
                {"action": "notify_user", "params": {"user": "{{user}}"}},
                {"action": "create_ticket", "params": {"title": "钓鱼攻击响应"}}
            ]
        })
    )
    
    # 勒索软件响应策略
    ransomware_playbook = PlaybookModel(
        name="ransomware_response",
        description="自动应对勒索软件事件",
        alert_type="ransomware",
        content=json.dumps({
            "name": "ransomware_response",
            "steps": [
                {"action": "query_misp", "params": {"ioc": "{{ioc}}"}},
                {"action": "isolate_host", "params": {"host": "{{host}}"}},
                {"action": "disable_account", "params": {"user": "admin"}},
                {"action": "create_ticket", "params": {"title": "勒索软件响应"}}
            ]
        })
    )
    
    db.add(phishing_playbook)
    db.add(ransomware_playbook)
    db.commit()
    db.close()


# ============ 告警 API ============

@app.post("/api/alert", response_model=AlertResponse, tags=["告警"])
async def receive_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """接收安全告警"""
    service = AlertService(db)
    return service.create_alert(alert)


@app.get("/api/alerts", response_model=List[AlertResponse], tags=["告警"])
async def get_alerts(
    skip: int = 0,
    limit: int = 10,
    alert_type: str = None,
    db: Session = Depends(get_db)
):
    """获取告警列表"""
    query = db.query(AlertModel)
    if alert_type:
        query = query.filter_by(type=alert_type)
    return query.offset(skip).limit(limit).all()


@app.get("/api/alert/{alert_id}", response_model=AlertResponse, tags=["告警"])
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """获取单个告警详情"""
    alert = db.query(AlertModel).filter_by(id=alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="告警不存在")
    return alert


@app.get("/api/alerts/stats", tags=["告警"])
async def get_alert_stats(db: Session = Depends(get_db)):
    """获取告警统计"""
    total = db.query(AlertModel).count()
    open_alerts = db.query(AlertModel).filter_by(status="open").count()
    resolved = db.query(AlertModel).filter_by(status="resolved").count()
    
    by_type = {}
    types = db.query(AlertModel.type).distinct().all()
    for (t,) in types:
        by_type[t] = db.query(AlertModel).filter_by(type=t).count()
    
    return {
        "total": total,
        "open": open_alerts,
        "resolved": resolved,
        "by_type": by_type
    }


# ============ 工单 API ============

@app.post("/api/ticket", response_model=TicketResponse, tags=["工单"])
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """创建工单"""
    new_ticket = TicketModel(**ticket.dict())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@app.get("/api/tickets", response_model=List[TicketResponse], tags=["工单"])
async def get_tickets(
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db)
):
    """获取工单列表"""
    query = db.query(TicketModel)
    if status:
        query = query.filter_by(status=status)
    return query.order_by(TicketModel.created_at.desc()).offset(skip).limit(limit).all()


@app.get("/api/ticket/{ticket_id}", response_model=TicketResponse, tags=["工单"])
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """获取单个工单"""
    ticket = db.query(TicketModel).filter_by(id=ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="工单不存在")
    return ticket


@app.put("/api/ticket/{ticket_id}", response_model=TicketResponse, tags=["工单"])
async def update_ticket(ticket_id: int, update: TicketUpdate, db: Session = Depends(get_db)):
    """更新工单"""
    ticket = db.query(TicketModel).filter_by(id=ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    if update.status:
        ticket.status = update.status
    if update.assignee:
        ticket.assignee = update.assignee
    if update.report:
        ticket.report = update.report
    
    ticket.updated_at = datetime.now()
    db.commit()
    db.refresh(ticket)
    return ticket


# ============ 响应策略 API ============

@app.post("/api/playbook/run", tags=["响应策略"])
async def run_playbook(request: PlaybookRunRequest, db: Session = Depends(get_db)):
    """手动触发响应策略执行"""
    alert = db.query(AlertModel).filter_by(id=request.alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="告警不存在")
    
    playbook = db.query(PlaybookModel).filter_by(name=request.playbook_name).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="响应策略不存在")

    engine = PlaybookEngine(db)
    result = engine.execute_playbook(playbook, alert)
    
    return {
        "status": "success",
        "playbook": request.playbook_name,
        "alert_id": request.alert_id,
        "actions": result,
        "message": f"响应策略 {request.playbook_name} 执行完成"
    }


@app.get("/api/playbooks", tags=["响应策略"])
async def get_playbooks(db: Session = Depends(get_db)):
    """获取所有响应策略"""
    return db.query(PlaybookModel).filter_by(is_active=True).all()


@app.get("/api/playbook/{playbook_id}", tags=["响应策略"])
async def get_playbook(playbook_id: int, db: Session = Depends(get_db)):
    """获取响应策略详情"""
    playbook = db.query(PlaybookModel).filter_by(id=playbook_id).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="响应策略不存在")
    return playbook


# ============ 智能助手 ============

# 系统提示词（服务器端统一管理）
AGENT_SYSTEM_PROMPT = """你是内嵌在 SOAR 安全运营平台中的智能助手，帮助安全分析师处理日常运维工作。

你的职责：
- 用中文回答问题，语气专业、简洁
- 帮助用户理解安全告警的含义和处置思路
- 提供安全运营的通用最佳实践建议
- 遇到不懂的问题诚实说明，不要编造"""


@app.post("/api/agent/chat", response_model=AgentChatResponse, tags=["智能助手"])
async def agent_chat(request: AgentChatRequest):
    """智能助手聊天代理"""
    # 优先读环境变量 → 降级读请求体 → 都没有才报错
    api_key = os.getenv("DEEPSEEK_API_KEY") or request.api_key
    if not api_key:
        raise HTTPException(status_code=500, detail="智能助手服务未配置：请在设置中填入 DeepSeek API Key")

    # 构建消息列表（系统提示词 + 历史对话）
    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        *request.messages
    ]

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return AgentChatResponse(reply=reply)

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="智能助手响应超时，请稍后重试")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 500
        if status == 401:
            raise HTTPException(status_code=502, detail="智能助手认证失败，API Key 无效或已过期，请检查后重试")
        elif status == 429:
            raise HTTPException(status_code=429, detail="请求过于频繁，请稍等片刻再试")
        elif status == 503:
            raise HTTPException(status_code=503, detail="智能助手服务正在维护中，请稍后重试")
        else:
            raise HTTPException(status_code=502, detail=f"智能助手服务异常 (HTTP {status})，请稍后重试")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="智能助手连接失败：无法访问 api.deepseek.com，请检查网络连接或代理设置")
    except requests.exceptions.SSLError:
        raise HTTPException(status_code=502, detail="智能助手 SSL 证书验证失败，请检查系统时间和网络环境")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="智能助手网络请求失败，请检查是否能访问 api.deepseek.com")


# ============ 健康检查 ============

@app.get("/health", tags=["健康检查"])
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "SOAR 平台"
    }


@app.get("/", tags=["根路由"])
async def root():
    """API 文档入口"""
    return {
        "message": "欢迎使用 SOAR 平台",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
