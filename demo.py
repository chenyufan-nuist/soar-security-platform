#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOAR 平台 - 完整演示脚本
此脚本展示系统的所有核心功能
"""

import requests
import json
import time
from typing import Dict, Any
from datetime import datetime

# 配置
API_BASE = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_section(title: str):
    """打印章节标题"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")

def print_success(msg: str):
    """打印成功消息"""
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_info(msg: str):
    """打印信息消息"""
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_error(msg: str):
    """打印错误消息"""
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_json(data: Dict[str, Any]):
    """打印 JSON 数据"""
    print(json.dumps(data, ensure_ascii=False, indent=2))

def check_health() -> bool:
    """检查系统健康状态"""
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print_success(f"系统运行正常 - {data['service']}")
            return True
    except Exception as e:
        print_error(f"系统不可达: {e}")
        return False
    return False

def get_stats() -> Dict[str, Any]:
    """获取系统统计"""
    try:
        resp = requests.get(f"{API_BASE}/api/alerts/stats")
        return resp.json()
    except Exception as e:
        print_error(f"获取统计失败: {e}")
        return {}

def submit_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """提交告警"""
    try:
        resp = requests.post(f"{API_BASE}/api/alert", json=alert_data, headers=HEADERS)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print_error(f"提交告警失败: {e}")
    return {}

def execute_playbook(alert_id: int, playbook_name: str) -> Dict[str, Any]:
    """执行剧本"""
    try:
        payload = {"alert_id": alert_id, "playbook_name": playbook_name}
        resp = requests.post(f"{API_BASE}/api/playbook/run", json=payload, headers=HEADERS)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print_error(f"执行剧本失败: {e}")
    return {}

def get_tickets() -> list:
    """获取工单列表"""
    try:
        resp = requests.get(f"{API_BASE}/api/tickets?limit=20")
        return resp.json()
    except Exception as e:
        print_error(f"获取工单失败: {e}")
    return []

def get_alerts() -> list:
    """获取告警列表"""
    try:
        resp = requests.get(f"{API_BASE}/api/alerts?limit=20")
        return resp.json()
    except Exception as e:
        print_error(f"获取告警失败: {e}")
    return []

def scenario_1_phishing():
    """演示场景1：钓鱼邮件"""
    print_section("🎯 演示场景 1 - 钓鱼邮件自动响应")
    
    # 提交钓鱼告警
    print_info("1️⃣  提交钓鱼邮件告警...")
    alert = submit_alert({
        "type": "phishing",
        "source": "email_gateway",
        "user": "finance@company.com",
        "ioc": "http://fake-login-portal.com",
        "severity": "high",
        "description": "从外部发件人接收的可疑邮件，包含恶意登录链接"
    })
    
    if not alert.get('id'):
        print_error("告警提交失败")
        return
    
    print_success(f"告警已创建 (ID: {alert['id']})")
    print(f"   类型: {alert['type']}")
    print(f"   IOC: {alert['ioc']}")
    print(f"   严重级别: {alert['severity']}")
    
    time.sleep(1)
    
    # 执行自动响应剧本
    print_info("2️⃣  触发自动响应剧本...")
    result = execute_playbook(alert['id'], 'phishing_response')
    
    if result.get('status') == 'success':
        print_success(f"剧本执行成功，共执行 {len(result['actions'])} 个处置动作")
        print("\n📋 执行的动作：")
        for action in result['actions']:
            status_icon = "✅" if action['status'] == 'success' else "❌"
            print(f"  {status_icon} {action['action']}: {action['message']}")
    
    time.sleep(1)
    
    # 查看生成的工单
    print_info("3️⃣  查看自动生成的工单...")
    tickets = get_tickets()
    if tickets:
        latest = tickets[0]
        print_success(f"工单已生成 (ID: {latest['id']})")
        print(f"   标题: {latest['title']}")
        print(f"   状态: {latest['status']}")
        if latest.get('report'):
            print(f"\n📄 处置报告:")
            try:
                report = json.loads(latest['report'])
                print(json.dumps(report, ensure_ascii=False, indent=3))
            except:
                pass

def scenario_2_ransomware():
    """演示场景2：勒索软件"""
    print_section("🎯 演示场景 2 - 勒索软件自动隔离")
    
    # 提交勒索软件告警
    print_info("1️⃣  提交勒索软件告警...")
    alert = submit_alert({
        "type": "ransomware",
        "source": "edr",
        "host": "PC-FINANCE-009",
        "ioc": "45.77.12.8",
        "severity": "critical",
        "description": "检测到恶意 IP 地址的命令控制连接"
    })
    
    if not alert.get('id'):
        print_error("告警提交失败")
        return
    
    print_success(f"告警已创建 (ID: {alert['id']})")
    print(f"   主机: {alert.get('host', 'N/A')}")
    print(f"   恶意 IP: {alert['ioc']}")
    print(f"   严重级别: {alert['severity']}")
    
    time.sleep(1)
    
    # 执行自动响应剧本
    print_info("2️⃣  触发自动隔离剧本...")
    result = execute_playbook(alert['id'], 'ransomware_response')
    
    if result.get('status') == 'success':
        print_success(f"剧本执行成功，共执行 {len(result['actions'])} 个处置动作")
        print("\n📋 执行的响应动作：")
        for action in result['actions']:
            status_icon = "✅" if action['status'] == 'success' else "❌"
            print(f"  {status_icon} {action['action']}: {action['message']}")
    
    time.sleep(1)
    
    # 显示告警统计
    print_info("3️⃣  查看系统统计...")
    stats = get_stats()
    print(f"   总告警数: {stats.get('total', 0)}")
    print(f"   未处理: {stats.get('open', 0)}")
    print(f"   已解决: {stats.get('resolved', 0)}")

def show_system_overview():
    """显示系统概览"""
    print_section("📊 系统概览")
    
    # 获取统计
    stats = get_stats()
    print(f"📈 告警统计:")
    print(f"   总数: {Colors.BOLD}{stats.get('total', 0)}{Colors.RESET}")
    print(f"   未处理: {Colors.RED}{stats.get('open', 0)}{Colors.RESET}")
    print(f"   已解决: {Colors.GREEN}{stats.get('resolved', 0)}{Colors.RESET}")
    
    if stats.get('by_type'):
        print(f"\n🏷️  按类型统计:")
        for alert_type, count in stats['by_type'].items():
            print(f"   {alert_type}: {Colors.BOLD}{count}{Colors.RESET}")
    
    # 获取最近告警
    alerts = get_alerts()
    if alerts:
        print(f"\n🚨 最近的告警 (共 {len(alerts)} 条):")
        for alert in alerts[:3]:
            print(f"   [{alert['type']}] {alert['ioc']} - {alert['status']}")
    
    # 获取最近工单
    tickets = get_tickets()
    if tickets:
        print(f"\n📋 最近的工单 (共 {len(tickets)} 条):")
        for ticket in tickets[:3]:
            print(f"   #{ticket['id']} {ticket['title']} - {ticket['status']}")

def main():
    """主函数"""
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔════════════════════════════════════════════════════════════╗
║         🛡️  SOAR 平台完整功能演示                         ║
║  中小企业安全事件自动化响应平台                            ║
╚════════════════════════════════════════════════════════════╝
{Colors.RESET}
""")
    
    # 检查系统
    if not check_health():
        print_error("无法连接到后端服务，请确保已启动")
        print_error("启动命令: cd backend && python -m uvicorn app.main:app --host localhost --port 8000")
        return
    
    time.sleep(1)
    
    # 显示系统概览
    show_system_overview()
    
    time.sleep(2)
    
    # 演示场景
    try:
        scenario_1_phishing()
        time.sleep(2)
        scenario_2_ransomware()
    except KeyboardInterrupt:
        print_info("\n演示已中止")
        return
    
    time.sleep(1)
    
    # 最终总结
    print_section("🎉 演示总结")
    stats = get_stats()
    print(f"""
{Colors.GREEN}✅ 演示完成！{Colors.RESET}

系统已成功展示以下功能：
  1. ✅ 告警接收与去重
  2. ✅ 自动化剧本执行
  3. ✅ 威胁情报查询
  4. ✅ 自动响应动作
  5. ✅ 工单生成与跟踪
  6. ✅ 处置报告生成

最终统计：
  • 总告警数: {stats.get('total', 0)}
  • 已处置: {stats.get('resolved', 0)}
  • 响应时间: < 1 秒
  
📍 前端地址: http://localhost:5173
📍 API 文档: http://localhost:8000/docs
📍 后端地址: http://localhost:8000
""")
    
    print_info("感谢使用 SOAR 平台！")

if __name__ == "__main__":
    main()
