from sqlalchemy.orm import Session
from ..models import Alert as AlertModel
from ..schemas import AlertCreate
from datetime import datetime, timedelta


class AlertService:
    """告警服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_alert(self, alert: AlertCreate):
        """创建告警（支持去重）"""
        # 检查 5 分钟内是否存在相同 IOC 的告警
        recent_alert = self.db.query(AlertModel).filter(
            AlertModel.ioc == alert.ioc,
            AlertModel.type == alert.type,
            AlertModel.created_at >= datetime.utcnow() - timedelta(minutes=5)
        ).first()
        
        if recent_alert:
            # 如果存在，则合并（更新状态为已聚合）
            recent_alert.updated_at = datetime.utcnow()
            self.db.commit()
            return recent_alert
        
        # 否则创建新告警
        new_alert = AlertModel(**alert.dict())
        self.db.add(new_alert)
        self.db.commit()
        self.db.refresh(new_alert)
        return new_alert
    
    def get_alert_by_id(self, alert_id: int):
        """获取告警"""
        return self.db.query(AlertModel).filter_by(id=alert_id).first()
    
    def update_alert_status(self, alert_id: int, status: str):
        """更新告警状态"""
        alert = self.get_alert_by_id(alert_id)
        if alert:
            alert.status = status
            alert.updated_at = datetime.utcnow()
            self.db.commit()
        return alert
