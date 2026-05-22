#!/usr/bin/env python3
"""
周报邮件发送脚本
集成到 weekly-report-collector 技能中
"""

import os
import logging
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class ReportEmailSender:
    def __init__(self, config_path: str = None):
        """初始化邮件发送器"""
        self.config_path = config_path or os.path.expanduser("~/.weekly-report-collector/config.json")
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_host": "",
                "smtp_port": 587,
                "smtp_user": "",
                "smtp_password": "",
                "default_recipients": []
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置
                    if "email" in user_config:
                        default_config["email"].update(user_config["email"])
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  配置文件加载失败: {e}")
        
        # 从环境变量覆盖配置
        env_host = os.getenv("SMTP_HOST")
        env_port = os.getenv("SMTP_PORT")
        env_user = os.getenv("SMTP_USER")
        env_pass = os.getenv("SMTP_PASS")
        
        if env_host:
            default_config["email"]["smtp_host"] = env_host
        if env_port:
            try:
                default_config["email"]["smtp_port"] = int(env_port)
            except ValueError:
                pass
        if env_user:
            default_config["email"]["smtp_user"] = env_user
        if env_pass:
            default_config["email"]["smtp_password"] = env_pass
        
        return default_config
    
    def send_report_email(self, report_path: str, recipients: List[str] = None, 
                         subject: str = None, body: str = None) -> bool:
        """发送周报邮件"""
        email_config = self.config["email"]
        
        if not email_config.get("enabled", False):
            print("❌ 邮件功能未启用，请在配置中启用")
            return False
        
        # 检查必要配置
        required = ["smtp_host", "smtp_user", "smtp_password"]
        for key in required:
            if not email_config.get(key):
                logging.debug(f"缺少必要配置: email.{key}")
                return False
        
        # 确定收件人
        if not recipients:
            recipients = email_config.get("default_recipients", [])
        
        if not recipients:
            print("❌ 未指定收件人")
            return False
        
        # 加载报告数据
        report_data = self._load_report(report_path)
        if not report_data:
            return False
        
        # 生成邮件内容
        if not subject:
            subject = self._generate_subject(report_data)
        
        if not body:
            body = self._generate_body(report_data)
        
        # 发送邮件
        return self._send_email(recipients, subject, body, email_config)
    
    def _load_report(self, report_path: str) -> Optional[Dict]:
        """加载报告数据"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"❌ 加载报告失败: {e}")
            return None
    
    def _generate_subject(self, report_data: Dict) -> str:
        """生成邮件主题"""
        author = report_data.get('author', '未知作者')
        date_range = report_data.get('date_range', '未知日期')
        template = report_data.get('template', '周报')
        
        return f"【周报】{author} - {date_range} - {template}"
    
    def _generate_body(self, report_data: Dict) -> str:
        """生成邮件正文"""
        author = report_data.get('author', '未知作者')
        date_range = report_data.get('date_range', '未知日期')
        template = report_data.get('template', '未知模板')
        created_at = report_data.get('created_at', '')
        content = report_data.get('content', {})
        
        # 构建邮件正文
        body = f"""周报提交通知

📋 报告信息：
- 作者：{author}
- 日期：{date_range}
- 模板：{template}
- 提交时间：{created_at}

📊 报告摘要：
"""
        
        # 添加内容摘要
        if 'completed' in content and content['completed']:
            body += f"\n✅ 本周完成 ({len(content['completed'])}项)：\n"
            for i, item in enumerate(content['completed'][:5], 1):
                body += f"  {i}. {item}\n"
            if len(content['completed']) > 5:
                body += f"  ... 等 {len(content['completed'])} 项工作\n"
        
        if 'next_week' in content and content['next_week']:
            body += f"\n📅 下周计划 ({len(content['next_week'])}项)：\n"
            for i, item in enumerate(content['next_week'][:5], 1):
                body += f"  {i}. {item}\n"
            if len(content['next_week']) > 5:
                body += f"  ... 等 {len(content['next_week'])} 项计划\n"
        
        if 'blockers' in content and content['blockers']:
            body += f"\n🚧 问题与阻碍 ({len(content['blockers'])}项)：\n"
            for i, item in enumerate(content['blockers'][:3], 1):
                body += f"  {i}. {item}\n"
        
        # 添加附件信息
        report_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        json_path = report_data.get('_filepath', '')
        md_path = json_path.replace('.json', '.md') if json_path else ''
        
        body += f"""
📎 附件：
- JSON格式报告：{json_path if json_path else '未保存'}
- Markdown格式：{md_path if os.path.exists(md_path) else '未生成'}

---
此邮件由 OpenClaw 周报管理系统自动发送
报告ID：{report_data.get('report_id', '未知')}
"""
        
        return body
    
    def _send_email(self, recipients: List[str], subject: str, body: str, 
                   email_config: Dict) -> bool:
        """使用 msmtp 发送邮件"""
        try:
            # 构建邮件内容
            email_content = f"""To: {', '.join(recipients)}
From: {email_config['smtp_user']}
Subject: {subject}
Date: $(date -R)
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0
X-Mailer: OpenClaw Weekly Report System

{body}"""
            
            # 使用 msmtp 发送
            process = subprocess.Popen(
                ['msmtp', '--read-recipients'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 写入收件人
            for recipient in recipients:
                process.stdin.write(recipient + '\n')
            process.stdin.close()
            
            # 发送邮件内容
            msmtp_process = subprocess.Popen(
                ['msmtp', '--read-envelope-from'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = msmtp_process.communicate(
                input=f"From: {email_config['smtp_user']}\n\n{email_content}"
            )
            
            if msmtp_process.returncode == 0:
                print(f"✅ 邮件发送成功！收件人: {', '.join(recipients)}")
                return True
            else:
                print(f"❌ 邮件发送失败: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 发送邮件时出错: {e}")
            return False
    
    def send_test_email(self, recipient: str) -> bool:
        """发送测试邮件"""
        test_subject = "OpenClaw 周报系统测试邮件"
        test_body = f"""这是一封测试邮件，用于验证 OpenClaw 周报系统的邮件发送功能。

📋 测试详情：
- 发件人：{self.config['email'].get('smtp_user', '未知')}
- 收件人：{recipient}
- 发送时间：$(date)
- 服务器：{self.config['email'].get('smtp_host', '未知')}:{self.config['email'].get('smtp_port', '未知')}

✅ 如果收到此邮件，表示：
1. SMTP 配置正确
2. 授权码/密码有效
3. 邮件发送功能正常

🔧 系统状态：
- msmtp 版本：$(msmtp --version | head -1)
- 配置文件：~/.msmtprc
- 环境变量：已设置

感谢测试！

--
OpenClaw 周报管理系统
测试时间：$(date)"""
        
        return self._send_email([recipient], test_subject, test_body, self.config['email'])
    
    def check_config(self) -> Dict:
        """检查邮件配置"""
        email_config = self.config["email"]
        status = {
            "enabled": email_config.get("enabled", False),
            "smtp_host": email_config.get("smtp_host", ""),
            "smtp_port": email_config.get("smtp_port", 0),
            "smtp_user": email_config.get("smtp_user", ""),
            "has_password": bool(email_config.get("smtp_password")),
            "default_recipients": email_config.get("default_recipients", []),
            "msmtp_installed": self._check_msmtp_installed(),
            "config_file": os.path.exists(os.path.expanduser("~/.msmtprc"))
        }
        return status
    
    def _check_msmtp_installed(self) -> bool:
        """检查 msmtp 是否安装"""
        try:
            subprocess.run(["which", "msmtp"], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

def main():
    parser = argparse.ArgumentParser(description='周报邮件发送器')
    parser.add_argument('--report', '-r', help='周报JSON文件路径')
    parser.add_argument('--to', '-t', nargs='+', help='收件人邮箱地址')
    parser.add_argument('--subject', '-s', help='邮件主题')
    parser.add_argument('--body', '-b', help='邮件正文')
    parser.add_argument('--test', action='store_true', help='发送测试邮件')
    parser.add_argument('--check', action='store_true', help='检查邮件配置')
    parser.add_argument('--config', '-c', help='配置文件路径')
    
    args = parser.parse_args()
    
    sender = ReportEmailSender(args.config)
    
    if args.check:
        status = sender.check_config()
        print("\n🔧 邮件配置状态:")
        print("=" * 50)
        print(f"✅ 启用状态: {'是' if status['enabled'] else '否'}")
        print(f"📧 SMTP服务器: {status['smtp_host']}:{status['smtp_port']}")
        print(f"👤 发件人: {status['smtp_user']}")
        logging.debug(f"密码配置: {'已设置' if status['has_password'] else '未设置'}")
        print(f"📨 默认收件人: {', '.join(status['default_recipients'])}")
        print(f"📦 msmtp安装: {'是' if status['msmtp_installed'] else '否'}")
        print(f"📁 配置文件: {'存在' if status['config_file'] else '不存在'}")
        
        # 检查环境变量
        print(f"🌐 SMTP_HOST环境变量: {os.getenv('SMTP_HOST', '未设置')}")
        print(f"🌐 SMTP_USER环境变量: {os.getenv('SMTP_USER', '未设置')}")
        
        return
    
    if args.test:
        if not args.to:
            print("❌ 请指定测试邮件收件人: --to recipient@example.com")
            return
        
        print(f"📧 发送测试邮件到: {args.to[0]}")
        if sender.send_test_email(args.to[0]):
            print("✅ 测试邮件发送成功！")
        else:
            print("❌ 测试邮件发送失败")
        return
    
    if args.report:
        recipients = args.to if args.to else None
        if sender.send_report_email(args.report, recipients, args.subject, args.body):
            print("✅ 周报邮件发送成功！")
        else:
            print("❌ 周报邮件发送失败")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()