from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AlertCreate(BaseModel):
    type: str
    source: str
    user: Optional[str] = None
    host: Optional[str] = None
    ioc: str
    severity: Optional[str] = "medium"
    description: Optional[str] = None


class AlertResponse(BaseModel):
    id: int
    type: str
    source: str
    user: Optional[str]
    host: Optional[str]
    ioc: str
    severity: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketCreate(BaseModel):
    alert_id: int
    title: str
    description: Optional[str] = None
    assignee: Optional[str] = None


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assignee: Optional[str] = None
    report: Optional[str] = None


class TicketResponse(BaseModel):
    id: int
    alert_id: int
    title: str
    description: Optional[str]
    assignee: Optional[str]
    status: str
    actions: Optional[str]
    report: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlaybookCreate(BaseModel):
    name: str
    description: Optional[str] = None
    content: str  # YAML/JSON
    alert_type: str


class PlaybookResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    alert_type: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PlaybookRunRequest(BaseModel):
    alert_id: int
    playbook_name: str


class ExecutionResult(BaseModel):
    action: str
    status: str
    result: Optional[str] = None
