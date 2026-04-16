#!/usr/bin/env python3
"""
周报收集器 - 交互式收集周报内容
支持多种输入方式和模板系统
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class WeeklyReportCollector:
    def __init__(self, storage_path: str = None):
        """初始化周报收集器"""
        self.storage_path = storage_path or os.path.expanduser("~/weekly-reports")
        self.templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")
        
        # 创建存储目录
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.templates_path, exist_ok=True)
        
        # 可用模板
        self.available_templates = self._discover_templates()
    
    def _discover_templates(self) -> Dict[str, str]:
        """发现可用的模板"""
        templates = {}
        template_dir = Path(self.templates_path)
        
        if template_dir.exists():
            for template_file in template_dir.glob("*.md"):
                template_name = template_file.stem
                templates[template_name] = str(template_file)
        
        return templates
    
    def collect_interactive(self, template: str = None) -> Dict[str, Any]:
        """交互式收集周报内容"""
        print("📝 周报收集器 - 交互式模式")
        print("=" * 50)
        
        # 选择模板
        if not template:
            template = self._select_template()
        
        # 收集基本信息
        report_data = self._collect_basic_info()
        report_data["template"] = template
        
        # 根据模板收集具体内容
        if template == "engineer":
            report_data["content"] = self._collect_engineer_content()
        elif template == "manager":
            report_data["content"] = self._collect_manager_content()
        else:
            report_data["content"] = self._collect_general_content()
        
        # 生成报告ID和时间戳
        report_data["report_id"] = self._generate_report_id()
        report_data["created_at"] = datetime.datetime.now().isoformat()
        report_data["metadata"] = {
            "source": "interactive",
            "template": template,
            "version": "1.0.0"
        }
        
        return report_data
    
    def _select_template(self) -> str:
        """选择模板"""
        print("\n📋 请选择周报模板：")
        for i, template_name in enumerate(self.available_templates.keys(), 1):
            print(f"  {i}. {template_name}")
        
        while True:
            try:
                choice = input(f"\n请输入选择 (1-{len(self.available_templates)}): ").strip()
                if not choice:
                    return "engineer"  # 默认模板
                
                idx = int(choice) - 1
                if 0 <= idx < len(self.available_templates):
                    return list(self.available_templates.keys())[idx]
                else:
                    print(f"❌ 请输入 1-{len(self.available_templates)} 之间的数字")
            except ValueError:
                print("❌ 请输入有效的数字")
    
    def _collect_basic_info(self) -> Dict[str, str]:
        """收集基本信息"""
        print("\n📋 基本信息")
        print("-" * 30)
        
        data = {}
        
        # 姓名
        name = input("姓名 (默认: 当前用户): ").strip()
        data["author"] = name if name else os.getenv("USER", "匿名用户")
        
        # 日期范围
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        
        date_range = input(f"日期范围 (默认: {start_of_week} 到 {end_of_week}): ").strip()
        if date_range:
            data["date_range"] = date_range
        else:
            data["date_range"] = f"{start_of_week} 到 {end_of_week}"
        
        # 部门/项目
        department = input("部门/项目名称: ").strip()
        if department:
            data["department"] = department
        
        # 角色
        role = input("角色 (如: 工程师, 项目经理等): ").strip()
        if role:
            data["role"] = role
        
        return data
    
    def _collect_engineer_content(self) -> Dict[str, Any]:
        """收集工程师周报内容"""
        print("\n👨‍💻 工程师周报内容")
        print("-" * 30)
        
        content = {}
        
        # 本周完成的工作
        print("\n✅ 本周完成的工作 (每行一项，空行结束):")
        completed = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            completed.append(line)
        content["completed"] = completed
        
        # 进行中的工作
        print("\n🔄 进行中的工作 (每行一项，格式: 任务名称 - 进度%，空行结束):")
        in_progress = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            in_progress.append(line)
        content["in_progress"] = in_progress
        
        # 遇到的问题
        print("\n🚧 遇到的问题/阻碍 (每行一项，空行结束):")
        blockers = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            blockers.append(line)
        content["blockers"] = blockers
        
        # 下周计划
        print("\n📅 下周计划 (每行一项，空行结束):")
        next_week = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            next_week.append(line)
        content["next_week"] = next_week
        
        # 关键指标 (可选)
        print("\n📊 关键指标 (可选，格式: 指标=数值，空行结束):")
        metrics = {}
        while True:
            line = input("  > ").strip()
            if not line:
                break
            if "=" in line:
                key, value = line.split("=", 1)
                metrics[key.strip()] = value.strip()
        if metrics:
            content["metrics"] = metrics
        
        return content
    
    def _collect_manager_content(self) -> Dict[str, Any]:
        """收集项目经理周报内容"""
        print("\n👔 项目经理周报内容")
        print("-" * 30)
        
        content = {}
        
        # 项目状态
        print("\n📈 项目整体状态:")
        content["project_status"] = input("  项目状态描述: ").strip()
        
        # 本周成果
        print("\n🎯 本周重点成果 (每行一项，空行结束):")
        achievements = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            achievements.append(line)
        content["achievements"] = achievements
        
        # 风险与问题
        print("\n🚨 风险与问题 (每行一项，空行结束):")
        risks = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            risks.append(line)
        content["risks"] = risks
        
        # 下周计划
        print("\n📅 下周计划 (每行一项，空行结束):")
        next_week = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            next_week.append(line)
        content["next_week"] = next_week
        
        # 需要决策的事项
        print("\n🎯 需要决策的事项 (每行一项，空行结束):")
        decisions = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            decisions.append(line)
        content["decisions_needed"] = decisions
        
        return content
    
    def _collect_general_content(self) -> Dict[str, Any]:
        """收集通用周报内容"""
        print("\n📝 通用周报内容")
        print("-" * 30)
        
        content = {}
        
        # 本周总结
        print("\n📋 本周工作总结:")
        content["summary"] = input("  简要总结本周工作: ").strip()
        
        # 具体工作
        print("\n✅ 具体完成的工作 (每行一项，空行结束):")
        completed = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            completed.append(line)
        content["completed"] = completed
        
        # 下周计划
        print("\n📅 下周工作计划 (每行一项，空行结束):")
        next_week = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            next_week.append(line)
        content["next_week"] = next_week
        
        # 其他事项
        print("\n💡 其他事项/建议 (每行一项，空行结束):")
        others = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            others.append(line)
        if others:
            content["others"] = others
        
        return content
    
    def _generate_report_id(self) -> str:
        """生成报告ID"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"weekly_report_{timestamp}"
    
    def save_report(self, report_data: Dict[str, Any], filename: str = None) -> str:
        """保存报告到文件"""
        if not filename:
            filename = f"{report_data['report_id']}.json"
        
        filepath = os.path.join(self.storage_path, filename)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 保存JSON文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        # 同时保存Markdown格式的副本
        md_filepath = filepath.replace('.json', '.md')
        self._save_markdown_report(report_data, md_filepath)
        
        return filepath
    
    def _save_markdown_report(self, report_data: Dict[str, Any], filepath: str):
        """保存Markdown格式的报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 周报 - {report_data.get('author', '匿名用户')}\n\n")
            f.write(f"**日期**: {report_data.get('date_range', '未指定')}\n")
            f.write(f"**模板**: {report_data.get('template', '未指定')}\n")
            f.write(f"**生成时间**: {report_data.get('created_at', '未指定')}\n\n")
            
            if 'role' in report_data:
                f.write(f"**角色**: {report_data['role']}\n")
            if 'department' in report_data:
                f.write(f"**部门/项目**: {report_data['department']}\n")
            
            f.write("\n---\n\n")
            
            content = report_data.get('content', {})
            
            if 'summary' in content:
                f.write("## 本周总结\n\n")
                f.write(f"{content['summary']}\n\n")
            
            if 'completed' in content and content['completed']:
                f.write("## ✅ 本周完成\n\n")
                for item in content['completed']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'in_progress' in content and content['in_progress']:
                f.write("## 🔄 进行中\n\n")
                for item in content['in_progress']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'blockers' in content and content['blockers']:
                f.write("## 🚧 问题与阻碍\n\n")
                for item in content['blockers']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'next_week' in content and content['next_week']:
                f.write("## 📅 下周计划\n\n")
                for item in content['next_week']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'achievements' in content and content['achievements']:
                f.write("## 🎯 重点成果\n\n")
                for item in content['achievements']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'risks' in content and content['risks']:
                f.write("## 🚨 风险与问题\n\n")
                for item in content['risks']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'decisions_needed' in content and content['decisions_needed']:
                f.write("## 🎯 需要决策的事项\n\n")
                for item in content['decisions_needed']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'others' in content and content['others']:
                f.write("## 💡 其他事项\n\n")
                for item in content['others']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            if 'metrics' in content and content['metrics']:
                f.write("## 📊 关键指标\n\n")
                for key, value in content['metrics'].items():
                    f.write(f"- **{key}**: {value}\n")
                f.write("\n")
    
    def list_templates(self):
        """列出所有可用模板"""
        print("📋 可用模板:")
        print("-" * 30)
        for template_name, template_path in self.available_templates.items():
            print(f"  • {template_name}: {template_path}")
    
    def validate_report(self, report_data: Dict[str, Any]) -> bool:
        """验证报告数据"""
        required_fields = ['report_id', 'created_at', 'author', 'content']
        
        for field in required_fields:
            if field not in report_data:
                print(f"❌ 缺少必要字段: {field}")
                return False
        
        if not isinstance(report_data.get('content', {}), dict):
            print("❌ content字段必须是字典类型")
            return False
        
        return True

def main():
    parser = argparse.ArgumentParser(description='周报收集器')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式模式')
    parser.add_argument('--template', '-t', help='指定模板名称')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--list-templates', '-l', action='store_true', help='列出所有模板')
    parser.add_argument('--storage', '-s', help='存储路径', default='~/weekly-reports')
    parser.add_argument('--debug', '-d', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    collector = WeeklyReportCollector(
        storage_path=os.path.expanduser(args.storage)
    )
    
    if args.list_templates:
        collector.list_templates()
        return
    
    if args.interactive or not sys.stdin.isatty():
        # 交互式模式
        try:
            report_data = collector.collect_interactive(args.template)
            
            if collector.validate_report(report_data):
                # 保存报告
                if args.output:
                    output_path = args.output
                else:
                    output_path = None
                
                saved_path = collector.save_report(report_data, output_path)
                print(f"\n✅ 周报已保存到: {saved_path}")
                print(f"📄 Markdown版本: {saved_path.replace('.json', '.md')}")
                
                # 显示摘要
                print(f"\n📋 报告摘要:")
                print(f"  ID: {report_data['report_id']}")
                print(f"  作者: {report_data.get('author', '未知')}")
                print(f"  模板: {report_data.get('template', '未知')}")
                print(f"  时间: {report_data.get('date_range', '未知')}")
                
                content = report_data.get('content', {})
                if 'completed' in content:
                    print(f"  完成项: {len(content['completed'])}个")
                if 'next_week' in content:
                    print(f"  下周计划: {len(content['next_week'])}个")
            else:
                print("❌ 报告数据验证失败")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  用户中断")
            sys.exit(0)
        except Exception as e:
            print(f"❌ 收集周报时出错: {e}")
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        # 非交互式模式，显示帮助
        parser.print_help()

if __name__ == "__main__":
    main()