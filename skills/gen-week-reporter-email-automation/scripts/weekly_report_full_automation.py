#!/usr/bin/env python3
"""
完整的周报生成和邮件发送自动化脚本
整合了gen-week-reporter技能调用、HTML转换和邮件发送
"""

import os
import sys
import subprocess
import time
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Email configuration from environment variables
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "your-email@163.com")
SENDER_NAME = os.environ.get("SENDER_NAME", "your-name")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "recipient@example.com")

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查依赖项...")
    
    # 检查必要的Python模块
    required_modules = ['smtplib', 'ssl', 'email']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ 缺少Python模块: {', '.join(missing_modules)}")
        return False
    
    print("✅ Python依赖项检查通过")
    return True

def check_git_repository():
    """检查git仓库"""
    print("📁 检查git仓库...")
    
    repo_path = "/home/developer/my-repos/huawei-developer-demo"
    if not os.path.exists(repo_path):
        print(f"❌ Git仓库不存在: {repo_path}")
        print("请确保git仓库已正确克隆")
        return False
    
    # 检查是否是git仓库
    git_dir = os.path.join(repo_path, ".git")
    if not os.path.exists(git_dir):
        print(f"❌ 不是有效的git仓库: {repo_path}")
        return False
    
    print(f"✅ Git仓库检查通过: {repo_path}")
    return True

def check_scripts():
    """检查必要的脚本文件"""
    print("📄 检查脚本文件...")
    
    desktop_path = "/home/developer/Desktop"
    required_scripts = [
        "create_clean_report.py",
        "send_clean_report.py"
    ]
    
    missing_scripts = []
    for script in required_scripts:
        script_path = os.path.join(desktop_path, script)
        if not os.path.exists(script_path):
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"❌ 缺少脚本文件: {', '.join(missing_scripts)}")
        print("请确保以下脚本在桌面目录:")
        for script in missing_scripts:
            print(f"  - {script}")
        return False
    
    print("✅ 所有脚本文件检查通过")
    return True

def generate_weekly_report():
    """生成周报（调用gen-week-reporter技能）"""
    print("📊 生成周报...")
    
    # 这里应该调用gen-week-reporter技能
    # 由于技能调用需要通过Hermes Agent，这里我们假设周报已经存在
    # 在实际使用中，应该调用gen-week-reporter技能
    
    desktop_path = "/home/developer/Desktop"
    report_files = [f for f in os.listdir(desktop_path) if "周报" in f and f.endswith(".md")]
    
    if not report_files:
        print("❌ 未找到周报文件")
        print("请先使用gen-week-reporter技能生成周报")
        print("或者手动创建周报文件")
        return None
    
    # 按修改时间排序，获取最新的文件
    report_files.sort(key=lambda x: os.path.getmtime(os.path.join(desktop_path, x)), reverse=True)
    latest_report = os.path.join(desktop_path, report_files[0])
    
    print(f"✅ 找到最新周报文件: {os.path.basename(latest_report)}")
    print(f"📊 文件大小: {os.path.getsize(latest_report)} 字节")
    print(f"📅 修改时间: {datetime.fromtimestamp(os.path.getmtime(latest_report)).strftime('%Y-%m-%d %H:%M:%S')}")
    
    return latest_report

def create_html_report(md_file_path):
    """创建清理版HTML报告"""
    print("🔄 创建清理版HTML报告...")
    
    # 检查create_clean_report.py脚本是否存在
    script_path = "/home/developer/Desktop/create_clean_report.py"
    if not os.path.exists(script_path):
        print(f"❌ 未找到脚本: {script_path}")
        print("请确保create_clean_report.py在桌面目录")
        return None
    
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd="/home/developer/Desktop"
        )
        
        if result.returncode == 0:
            print("✅ 清理版HTML报告创建成功")
            
            # 提取生成的HTML文件路径
            html_file = None
            for line in result.stdout.split('\n'):
                if "HTML文件:" in line:
                    html_file = line.split(":")[-1].strip()
                    print(f"📄 生成的HTML文件: {html_file}")
                elif "文件大小:" in line:
                    print(line.strip())
            
            # 如果没有提取到，尝试查找文件
            if not html_file:
                html_files = [f for f in os.listdir("/home/developer/Desktop") 
                            if "周报" in f and f.endswith("_clean.html")]
                if html_files:
                    html_file = os.path.join("/home/developer/Desktop", html_files[0])
                    print(f"📄 自动找到HTML文件: {os.path.basename(html_file)}")
            
            return html_file
        else:
            print(f"❌ 创建HTML报告失败: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 创建HTML报告过程出错: {e}")
        return None

def send_email_report():
    """发送周报邮件"""
    print("📧 发送周报邮件...")
    
    # 检查send_clean_report.py脚本是否存在
    script_path = "/home/developer/Desktop/send_clean_report.py"
    if not os.path.exists(script_path):
        print(f"❌ 未找到脚本: {script_path}")
        print("请确保send_clean_report.py在桌面目录")
        return False
    
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd="/home/developer/Desktop"
        )
        
        if result.returncode == 0:
            print("✅ 周报邮件发送成功")
            
            # 提取关键信息
            for line in result.stdout.split('\n'):
                if "发件人:" in line or "收件人:" in line or "邮件主题:" in line:
                    print(f"   {line.strip()}")
                elif "发送时间:" in line:
                    print(f"   {line.strip()}")
            
            return True
        else:
            print(f"❌ 发送邮件失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 发送邮件过程出错: {e}")
        return False

def quick_send_mode():
    """快速发送模式 - 直接发送已生成的清理版HTML周报"""
    print("🚀 快速发送模式 - 直接发送已生成的清理版HTML周报")
    
    # 检查清理版HTML文件是否存在
    html_files = [f for f in os.listdir("/home/developer/Desktop") 
                 if "周报" in f and f.endswith("_clean.html")]
    
    if not html_files:
        print("❌ 未找到清理版HTML周报文件")
        print("请先运行完整流程或手动创建HTML文件")
        return False
    
    # 使用最新的清理版HTML文件
    latest_html = sorted(html_files, key=lambda x: os.path.getmtime(os.path.join("/home/developer/Desktop", x)), reverse=True)[0]
    html_file_path = os.path.join("/home/developer/Desktop", latest_html)
    
    print(f"📄 使用HTML文件: {latest_html}")
    print(f"📊 文件大小: {os.path.getsize(html_file_path)} 字节")
    
    # 直接发送邮件
    return send_email_report()

def main():
    """主函数 - 完整的周报生成和邮件发送流程"""
    print("=" * 60)
    print("🚀 周报生成与邮件发送自动化系统")
    print("=" * 60)
    print("完整工作流程:")
    print("1. 检查依赖项和git仓库")
    print("2. 生成周报（调用gen-week-reporter技能）")
    print("3. 创建清理版HTML报告")
    print("4. 发送HTML格式邮件")
    print("=" * 60)
    
    start_time = time.time()
    
    # 步骤1: 检查依赖项
    if not check_dependencies():
        print("❌ 依赖项检查失败，请确保所有必要模块已安装")
        return
    
    # 步骤2: 检查git仓库
    if not check_git_repository():
        print("❌ Git仓库检查失败")
        return
    
    # 步骤3: 检查脚本文件
    if not check_scripts():
        print("❌ 脚本文件检查失败")
        return
    
    # 步骤4: 生成周报
    md_file = generate_weekly_report()
    if not md_file:
        print("❌ 周报生成失败")
        return
    
    # 步骤5: 创建清理版HTML报告
    html_file = create_html_report(md_file)
    if not html_file:
        print("❌ 创建HTML报告失败")
        return
    
    # 步骤6: 发送周报邮件
    if not send_email_report():
        print("❌ 发送邮件失败")
        return
    
    # 完成总结
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🎉 周报生成与邮件发送流程完成!")
    print("=" * 60)
    print(f"📅 开始时间: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 完成时间: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  总耗时: {elapsed_time:.2f}秒")
    print(f"📧 收件人: {RECEIVER_EMAIL}")
    print(f"📧 发件人: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"📄 原始周报: {os.path.basename(md_file)}")
    print(f"🌐 HTML报告: {os.path.basename(html_file) if html_file else '未生成'}")
    print(f"📋 发送日志: /home/developer/Desktop/email_send_log.txt")
    print("\n✨ 邮件特点:")
    print("   - 清理版HTML格式，移除所有冗余元数据")
    print("   - 专业美观的邮件设计")
    print("   - 响应式布局，适配各种设备")
    print("   - 包含纯文本备用版本")
    print("   - 使用163邮箱SMTP发送")
    print("=" * 60)
    
    # 显示最新发送记录
    log_file = "/home/developer/Desktop/email_send_log.txt"
    if os.path.exists(log_file):
        print("\n📋 最新发送记录:")
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                print(f"   {lines[-1].strip()}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_send_mode()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("用法: python3 weekly_report_full_automation.py [选项]")
        print("选项:")
        print("  --quick     快速发送模式（直接发送已生成的清理版HTML周报）")
        print("  --help      显示帮助信息")
        print("  无选项      完整工作流程模式")
    else:
        main()