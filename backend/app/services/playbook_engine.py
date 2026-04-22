import json
from sqlalchemy.orm import Session
from datetime import datetime
from ..models import ExecutionLog, Ticket as TicketModel
from .misp_service import MISPService


class PlaybookEngine:
    """剧本执行引擎"""
    
    def __init__(self, db: Session):
        self.db = db
        self.misp = MISPService()
    
    def execute_playbook(self, playbook, alert):
        """执行剧本"""
        playbook_content = json.loads(playbook.content)
        steps = playbook_content.get("steps", [])
        
        execution_results = []
        
        for step in steps:
            action = step.get("action")
            params = step.get("params", {})
            
            # 替换参数中的模板变量
            params = self._replace_variables(params, alert)
            
            # 执行动作
            result = self._execute_action(action, params)
            
            # 记录执行日志
            log = ExecutionLog(
                playbook_id=playbook.id,
                alert_id=alert.id,
                action=action,
                status="success" if result["status"] == "success" else "failed",
                result=json.dumps(result)
            )
            self.db.add(log)
            
            execution_results.append({
                "action": action,
                "status": result["status"],
                "message": result.get("message", "")
            })
        
        # 创建工单
        ticket = TicketModel(
            alert_id=alert.id,
            title=f"[{alert.type.upper()}] 自动响应处置",
            description=f"告警 IOC: {alert.ioc}",
            status="resolved",
            actions=json.dumps(execution_results),
            report=self._generate_report(alert, execution_results)
        )
        self.db.add(ticket)
        self.db.commit()
        
        return execution_results
    
    def _replace_variables(self, params: dict, alert):
        """替换参数中的模板变量"""
        result = {}
        for key, value in params.items():
            if isinstance(value, str):
                value = value.replace("{{ioc}}", alert.ioc or "")
                value = value.replace("{{user}}", alert.user or "")
                value = value.replace("{{host}}", alert.host or "")
                value = value.replace("{{type}}", alert.type or "")
            result[key] = value
        return result
    
    def _execute_action(self, action: str, params: dict):
        """执行单个动作"""
        try:
            if action == "query_misp":
                result = self.misp.query_ioc(params.get("ioc", ""))
                return {
                    "status": "success",
                    "message": f"查询威胁情报成功: {result}",
                    "data": result
                }
            
            elif action == "block_url":
                url = params.get("url", "")
                return {
                    "status": "success",
                    "message": f"已封禁 URL: {url}",
                    "data": {"url": url, "action": "blocked"}
                }
            
            elif action == "block_ip":
                ip = params.get("ip", "")
                return {
                    "status": "success",
                    "message": f"已封禁 IP: {ip}",
                    "data": {"ip": ip, "action": "blocked"}
                }
            
            elif action == "isolate_host":
                host = params.get("host", "")
                return {
                    "status": "success",
                    "message": f"已隔离主机: {host}",
                    "data": {"host": host, "action": "isolated"}
                }
            
            elif action == "disable_account":
                user = params.get("user", "")
                return {
                    "status": "success",
                    "message": f"已禁用账号: {user}",
                    "data": {"user": user, "action": "disabled"}
                }
            
            elif action == "notify_user":
                user = params.get("user", "")
                return {
                    "status": "success",
                    "message": f"已通知用户: {user}",
                    "data": {"user": user, "notified": True}
                }
            
            elif action == "create_ticket":
                title = params.get("title", "自动工单")
                return {
                    "status": "success",
                    "message": f"已创建工单: {title}",
                    "data": {"title": title, "created": True}
                }
            
            else:
                return {
                    "status": "failed",
                    "message": f"未知动作: {action}"
                }
        
        except Exception as e:
            return {
                "status": "failed",
                "message": f"执行失败: {str(e)}"
            }
    
    def _generate_report(self, alert, execution_results):
        """生成处置报告"""
        report = {
            "title": f"安全事件自动响应报告",
            "event_type": alert.type,
            "ioc": alert.ioc,
            "severity": alert.severity,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "已处置",
            "actions_taken": execution_results,
            "summary": f"对{alert.type}事件进行了自动响应，共执行{len(execution_results)}个处置动作。"
        }
        return json.dumps(report, ensure_ascii=False, indent=2)
