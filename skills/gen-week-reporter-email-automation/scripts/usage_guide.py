#!/usr/bin/env python3
"""
周报生成与邮件发送自动化系统 - 使用指南
"""

import os
import sys
from datetime import datetime

# Email configuration from environment variables
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "your-email@163.com")
SENDER_NAME = os.environ.get("SENDER_NAME", "your-name")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "recipient@example.com")

def print_header():
    """打印标题"""
    print("=" * 70)
    print("📊 周报生成与邮件发送自动化系统")
    print("=" * 70)

def print_usage():
    """打印使用说明"""
    print_header()
    print("\n📋 使用说明:")
    print("=" * 70)
    print("这个系统提供了完整的周报生成和邮件发送工作流程。")
    print("整合了gen-week-reporter技能调用、HTML转换和邮件发送。")
    print("=" * 70)
    
    print("\n🚀 主要功能:")
    print("-" * 50)
    print("1. ✅ 自动生成周报（调用gen-week-reporter技能）")
    print("2. ✅ 创建清理版HTML格式（移除不需要的元数据）")
    print("3. ✅ 发送HTML格式周报到指定邮箱")
    print("4. ✅ 完整的错误处理和日志记录")
    print("5. ✅ 支持快速发送模式")
    
    print("\n📧 邮箱配置:")
    print("-" * 50)
    print(f"发件人: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"收件人: {RECEIVER_EMAIL}")
    print("SMTP服务器: smtp.163.com:465 (SSL)")
    
    print("\n🗂️ 文件位置:")
    print("-" * 50)
    print("脚本文件: /home/developer/Desktop/")
    print("周报文件: /home/developer/Desktop/")
    print("发送日志: /home/developer/Desktop/email_send_log.txt")
    
    print("\n⚙️ 使用方法:")
    print("-" * 50)
    print("方法1: 完整工作流程")
    print("  cd /home/developer/Desktop")
    print("  python3 weekly_report_full_automation.py")
    print("")
    print("方法2: 快速发送模式（已有周报文件）")
    print("  cd /home/developer/Desktop")
    print("  python3 weekly_report_full_automation.py --quick")
    print("")
    print("方法3: 分步执行")
    print("  # 步骤1: 生成周报")
    print("  cd /home/developer/my-repos/huawei-developer-demo")
    print("  # 调用gen-week-reporter技能")
    print("")
    print("  # 步骤2: 创建HTML")
    print("  cd /home/developer/Desktop")
    print("  python3 create_clean_report.py")
    print("")
    print("  # 步骤3: 发送邮件")
    print("  python3 send_clean_report.py")

def print_workflow():
    """打印工作流程"""
    print("\n🔄 完整工作流程:")
    print("=" * 70)
    print("1. 🔍 检查依赖项和git仓库")
    print("2. 📊 生成周报（调用gen-week-reporter技能）")
    print("3. 🎨 创建清理版HTML报告")
    print("4. 📧 发送HTML格式邮件")
    print("5. 📋 记录发送日志")
    print("=" * 70)

def print_removed_content():
    """打印移除的内容"""
    print("\n🗑️ 清理版HTML移除的内容:")
    print("=" * 70)
    print("1. ❌ 报告生成时间")
    print("2. ❌ 数据来源")
    print("3. ❌ 监控周期")
    print("4. ❌ 报告数量")
    print("5. ❌ 最佳实践案例数量")
    print("6. ❌ 风险提示")
    print("7. ❌ 后续计划")
    print("=" * 70)
    print("✨ 保留核心内容，移除冗余元数据")

def print_troubleshooting():
    """打印故障排除指南"""
    print("\n🔧 故障排除指南:")
    print("=" * 70)
    print("1. 周报文件不存在")
    print("   解决方案: 先使用gen-week-reporter技能生成周报")
    print("")
    print("2. HTML文件不存在")
    print("   解决方案: 先运行create_clean_report.py生成HTML文件")
    print("")
    print("3. 发送失败: 认证错误")
    print("   解决方案: 检查客户端授权码是否正确")
    print("")
    print("4. 发送失败: 连接超时")
    print("   解决方案: 检查网络连接，确认SMTP服务器地址和端口")
    print("")
    print("5. 脚本文件不存在")
    print("   解决方案: 确保脚本文件在桌面目录")
    print("   ls -la ~/Desktop/*.py")
    print("")
    print("6. 文件发现失败")
    print("   解决方案: 脚本会自动查找最新周报文件")
    print("   如果失败，手动检查桌面目录中的周报文件")
    print("   ls -la ~/Desktop/*.md | grep -i \"周报\"")

def print_automation():
    """打印自动化部署指南"""
    print("\n🤖 自动化部署:")
    print("=" * 70)
    print("设置定时任务（每周一早上9点自动发送）:")
    print("")
    print("1. 编辑crontab:")
    print("   crontab -e")
    print("")
    print("2. 添加以下行:")
    print("   0 9 * * 1 cd /home/developer/Desktop && python3 weekly_report_full_automation.py")
    print("")
    print("3. 保存并退出")

def print_logs():
    """打印日志查看方法"""
    print("\n📋 日志和监控:")
    print("=" * 70)
    print("发送日志位置: /home/developer/Desktop/email_send_log.txt")
    print("")
    print("查看所有发送记录:")
    print("  cat /home/developer/Desktop/email_send_log.txt")
    print("")
    print("查看最新5条记录:")
    print("  tail -5 /home/developer/Desktop/email_send_log.txt")
    print("")
    print("查看今天发送的记录:")
    print("  grep \"$(date +%Y-%m-%d)\" /home/developer/Desktop/email_send_log.txt")

def print_test_commands():
    """打印测试命令"""
    print("\n🧪 测试命令:")
    print("=" * 70)
    print("测试SMTP连接:")
    print("  python3 -c \"")
    print("  import smtplib, ssl")
    print("  context = ssl.create_default_context()")
    print("  try:")
    print("      with smtplib.SMTP_SSL('smtp.163.com', 465, context=context) as server:")
    print("          print('SMTP服务器连接正常')")
    print("  except Exception as e:")
    print("      print(f'连接失败: {e}')")
    print("  \"")
    print("")
    print("检查脚本执行权限:")
    print("  chmod +x /home/developer/Desktop/*.py")
    print("")
    print("检查文件是否存在:")
    print("  ls -la ~/Desktop/*.py")
    print("  ls -la ~/Desktop/*.md | grep -i \"周报\"")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--workflow":
        print_workflow()
    elif len(sys.argv) > 1 and sys.argv[1] == "--troubleshoot":
        print_troubleshooting()
    elif len(sys.argv) > 1 and sys.argv[1] == "--automation":
        print_automation()
    elif len(sys.argv) > 1 and sys.argv[1] == "--logs":
        print_logs()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        print_test_commands()
    elif len(sys.argv) > 1 and sys.argv[1] == "--removed":
        print_removed_content()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_usage()
    else:
        print_usage()
        print("\n📚 更多选项:")
        print("  --workflow     查看完整工作流程")
        print("  --troubleshoot 查看故障排除指南")
        print("  --automation   查看自动化部署指南")
        print("  --logs         查看日志查看方法")
        print("  --test         查看测试命令")
        print("  --removed      查看移除的内容")
        print("  --help         显示帮助信息")
        
        print("\n" + "=" * 70)
        print("💡 提示: 使用以下命令开始:")
        print("  cd /home/developer/Desktop")
        print("  python3 weekly_report_full_automation.py")
        print("=" * 70)

if __name__ == "__main__":
    main()