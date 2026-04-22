from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

class Alert(Base):
    """告警模型"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), index=True)  # phishing, ransomware, etc.
    source = Column(String(50))  # 告警来源
    user = Column(String(100), nullable=True)
    host = Column(String(100), nullable=True)
    ioc = Column(String(255), index=True)  # 威胁指标
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    status = Column(String(20), default="open")  # open, in_progress, resolved, closed
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Ticket(Base):
    """工单模型"""
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, index=True)
    title = Column(String(255))
    description = Column(Text, nullable=True)
    assignee = Column(String(100), nullable=True)
    status = Column(String(20), default="open")  # open, in_progress, resolved, closed
    actions = Column(Text, nullable=True)  # JSON 格式的已执行动作列表
    report = Column(Text, nullable=True)  # 处置报告
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Playbook(Base):
    """剧本模型"""
    __tablename__ = "playbooks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text)  # YAML/JSON 格式的剧本定义
    alert_type = Column(String(50))  # 触发的告警类型
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExecutionLog(Base):
    """执行日志模型"""
    __tablename__ = "execution_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    playbook_id = Column(Integer, index=True)
    alert_id = Column(Integer, index=True)
    action = Column(String(100))
    status = Column(String(20))  # success, failed
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
