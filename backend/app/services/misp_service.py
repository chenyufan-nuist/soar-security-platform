import requests
import json
from typing import Optional


class MISPService:
    """MISP 威胁情报服务"""
    
    def __init__(self, misp_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 MISP 服务
        由于本地演示环境可能没有 MISP 实例，这里使用模拟数据
        """
        self.misp_url = misp_url or "http://misp:6666"
        self.api_key = api_key or "demo_key"
        self.use_mock = True  # 默认使用模拟数据
    
    def query_ioc(self, ioc: str):
        """查询 IOC 信息"""
        if self.use_mock:
            return self._mock_query(ioc)
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                f"{self.misp_url}/api/search/{ioc}",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"MISP 查询失败: {e}")
        
        return self._mock_query(ioc)
    
    def _mock_query(self, ioc: str):
        """模拟 MISP 查询结果"""
        threat_db = {
            "http://malicious.com": {
                "type": "URL",
                "threat_level": "high",
                "tags": ["phishing", "banking-trojan"],
                "last_seen": "2026-04-20",
                "reputation": -95,
                "action": "block_immediately"
            },
            "45.77.12.8": {
                "type": "IP",
                "threat_level": "critical",
                "tags": ["ransomware-c2", "known-malicious"],
                "last_seen": "2026-04-21",
                "reputation": -100,
                "action": "isolate_immediately"
            },
            "fake-login-portal.com": {
                "type": "Domain",
                "threat_level": "high",
                "tags": ["phishing", "credential-harvester"],
                "last_seen": "2026-04-22",
                "reputation": -90,
                "action": "block"
            },
            "test@evil.com": {
                "type": "Email",
                "threat_level": "medium",
                "tags": ["phishing", "spam"],
                "last_seen": "2026-04-21",
                "reputation": -70,
                "action": "quarantine"
            }
        }
        
        if ioc in threat_db:
            return {
                "found": True,
                "ioc": ioc,
                **threat_db[ioc],
                "recommendation": "按照建议动作立即处置"
            }
        else:
            return {
                "found": False,
                "ioc": ioc,
                "threat_level": "unknown",
                "recommendation": "未知威胁，建议观察"
            }
    
    def get_threat_level(self, ioc: str) -> str:
        """获取威胁等级"""
        result = self.query_ioc(ioc)
        return result.get("threat_level", "unknown")
    
    def get_recommendation(self, ioc: str) -> str:
        """获取处置建议"""
        result = self.query_ioc(ioc)
        return result.get("action", "unknown")
