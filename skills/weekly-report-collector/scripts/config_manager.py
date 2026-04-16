#!/usr/bin/env python3
"""
周报收集器配置管理器
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_path: str = None):
        """初始化配置管理器"""
        if config_path:
            self.config_path = os.path.expanduser(config_path)
        else:
            self.config_path = os.path.expanduser("~/.weekly-report-collector/config.json")
        
        self.config_dir = os.path.dirname(self.config_path)
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "default_template": "engineer",
            "auto_save": True,
            "storage_path": "~/weekly-reports",
            "git_integration": False,
            "notifications": {
                "enabled": True,
                "reminder_day": "friday",
                "reminder_time": "17:00",
                "email_reminder": False,
                "email_recipients": []
            },
            "email": {
                "enabled": False,
                "smtp_host": "",
                "smtp_port": 587,
                "smtp_user": "",
                "smtp_password": "",
                "default_recipients": []
            },
            "templates": {
                "engineer": "工程师周报模板",
                "manager": "项目经理周报模板",
                "designer": "设计师周报模板",
                "sales": "销售周报模板"
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置，用户配置覆盖默认配置
                    self._deep_update(default_config, user_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  配置文件加载失败，使用默认配置: {e}")
        
        return default_config
    
    def _deep_update(self, base: Dict, update: Dict):
        """深度更新字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已保存到: {self.config_path}")
            return True
        except IOError as e:
            print(f"❌ 保存配置失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        # 遍历到最后一个键的父级
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
        return self.save_config()
    
    def show_config(self, section: str = None):
        """显示配置"""
        if section:
            value = self.get(section)
            if value is not None:
                print(f"\n🔧 配置项: {section}")
                print("-" * 40)
                if isinstance(value, dict):
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"  {value}")
            else:
                print(f"❌ 配置项不存在: {section}")
        else:
            print("\n🔧 当前配置:")
            print("=" * 50)
            self._print_config_section(self.config)
    
    def _print_config_section(self, config: Dict, indent: int = 0):
        """递归打印配置部分"""
        for key, value in config.items():
            if isinstance(value, dict):
                print(" " * indent + f"{key}:")
                self._print_config_section(value, indent + 2)
            else:
                print(" " * indent + f"{key}: {value}")
    
    def setup_interactive(self):
        """交互式配置向导"""
        print("🎯 周报收集器配置向导")
        print("=" * 50)
        
        # 基本配置
        print("\n📋 基本配置")
        print("-" * 30)
        
        default_template = input(f"默认模板 (engineer/manager/designer/sales) [默认: {self.config['default_template']}]: ").strip()
        if default_template:
            self.config['default_template'] = default_template
        
        auto_save = input(f"自动保存报告 (yes/no) [默认: {'yes' if self.config['auto_save'] else 'no'}]: ").strip().lower()
        if auto_save in ['yes', 'y', 'true']:
            self.config['auto_save'] = True
        elif auto_save in ['no', 'n', 'false']:
            self.config['auto_save'] = False
        
        storage_path = input(f"报告存储路径 [默认: {self.config['storage_path']}]: ").strip()
        if storage_path:
            self.config['storage_path'] = storage_path
        
        # 通知配置
        print("\n🔔 通知配置")
        print("-" * 30)
        
        notifications_enabled = input(f"启用通知提醒 (yes/no) [默认: {'yes' if self.config['notifications']['enabled'] else 'no'}]: ").strip().lower()
        if notifications_enabled in ['yes', 'y', 'true']:
            self.config['notifications']['enabled'] = True
            
            reminder_day = input(f"提醒日期 (monday/tuesday/wednesday/thursday/friday) [默认: {self.config['notifications']['reminder_day']}]: ").strip()
            if reminder_day:
                self.config['notifications']['reminder_day'] = reminder_day
            
            reminder_time = input(f"提醒时间 (HH:MM) [默认: {self.config['notifications']['reminder_time']}]: ").strip()
            if reminder_time:
                self.config['notifications']['reminder_time'] = reminder_time
            
            email_reminder = input(f"启用邮件提醒 (yes/no) [默认: {'yes' if self.config['notifications']['email_reminder'] else 'no'}]: ").strip().lower()
            if email_reminder in ['yes', 'y', 'true']:
                self.config['notifications']['email_reminder'] = True
            elif email_reminder in ['no', 'n', 'false']:
                self.config['notifications']['email_reminder'] = False
        else:
            self.config['notifications']['enabled'] = False
        
        # 邮件配置
        print("\n📧 邮件配置 (用于发送周报)")
        print("-" * 30)
        
        email_enabled = input(f"启用邮件发送 (yes/no) [默认: {'yes' if self.config['email']['enabled'] else 'no'}]: ").strip().lower()
        if email_enabled in ['yes', 'y', 'true']:
            self.config['email']['enabled'] = True
            
            smtp_host = input(f"SMTP服务器 [默认: {self.config['email']['smtp_host']}]: ").strip()
            if smtp_host:
                self.config['email']['smtp_host'] = smtp_host
            
            smtp_port = input(f"SMTP端口 [默认: {self.config['email']['smtp_port']}]: ").strip()
            if smtp_port:
                try:
                    self.config['email']['smtp_port'] = int(smtp_port)
                except ValueError:
                    print("⚠️  端口必须是数字，使用默认值")
            
            smtp_user = input(f"SMTP用户名 [默认: {self.config['email']['smtp_user']}]: ").strip()
            if smtp_user:
                self.config['email']['smtp_user'] = smtp_user
            
            # 密码不显示输入
            print("💡 密码将在环境变量中设置，不在配置文件中存储")
            
            # 默认收件人
            print("\n📮 默认收件人 (多个用逗号分隔，直接回车跳过):")
            recipients = input("  收件人邮箱: ").strip()
            if recipients:
                self.config['email']['default_recipients'] = [r.strip() for r in recipients.split(',')]
        else:
            self.config['email']['enabled'] = False
        
        # Git集成
        print("\n🔗 Git集成配置")
        print("-" * 30)
        
        git_integration = input(f"启用Git集成 (yes/no) [默认: {'yes' if self.config['git_integration'] else 'no'}]: ").strip().lower()
        if git_integration in ['yes', 'y', 'true']:
            self.config['git_integration'] = True
        elif git_integration in ['no', 'n', 'false']:
            self.config['git_integration'] = False
        
        # 保存配置
        if self.save_config():
            print(f"\n✅ 配置完成!")
            print(f"📁 配置文件: {self.config_path}")
            
            # 显示环境变量设置建议
            if self.config['email']['enabled'] and self.config['email']['smtp_password']:
                print("\n🔐 请设置以下环境变量:")
                print(f"  export SMTP_HOST='{self.config['email']['smtp_host']}'")
                print(f"  export SMTP_PORT='{self.config['email']['smtp_port']}'")
                print(f"  export SMTP_USER='{self.config['email']['smtp_user']}'")
                print("  export SMTP_PASS='您的密码'")
            
            # 创建存储目录
            storage_path = os.path.expanduser(self.config['storage_path'])
            os.makedirs(storage_path, exist_ok=True)
            print(f"📁 报告存储目录: {storage_path}")
        else:
            print("❌ 配置保存失败")

def main():
    parser = argparse.ArgumentParser(description='周报收集器配置管理器')
    parser.add_argument('--setup', action='store_true', help='交互式配置向导')
    parser.add_argument('--show', '-s', metavar='SECTION', help='显示配置项或整个配置')
    parser.add_argument('--get', '-g', metavar='KEY', help='获取配置值')
    parser.add_argument('--set', metavar=('KEY', 'VALUE'), nargs=2, help='设置配置值')
    parser.add_argument('--config', '-c', help='配置文件路径', default='~/.weekly-report-collector/config.json')
    
    args = parser.parse_args()
    
    config_manager = ConfigManager(args.config)
    
    if args.setup:
        config_manager.setup_interactive()
    elif args.show:
        config_manager.show_config(args.show)
    elif args.get:
        value = config_manager.get(args.get)
        print(value)
    elif args.set:
        key, value = args.set
        # 尝试解析值类型
        try:
            if value.lower() in ['true', 'yes', 'y']:
                value = True
            elif value.lower() in ['false', 'no', 'n']:
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                value = float(value)
        except (ValueError, AttributeError):
            pass  # 保持字符串类型
        
        if config_manager.set(key, value):
            print(f"✅ 配置已更新: {key} = {value}")
        else:
            print(f"❌ 配置更新失败")
    else:
        # 显示当前配置
        config_manager.show_config()

if __name__ == "__main__":
    main()