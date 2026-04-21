#!/bin/bash
# 周报生成与邮件发送自动化系统 - 快速启动脚本
# 使用方法: ./weekly_report_quick_start.sh [选项]

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 函数：检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "命令 '$1' 未找到，请先安装"
        exit 1
    fi
}

# 函数：检查文件是否存在
check_file() {
    if [ ! -f "$1" ]; then
        print_error "文件 '$1' 不存在"
        return 1
    fi
    return 0
}

# 函数：检查目录是否存在
check_dir() {
    if [ ! -d "$1" ]; then
        print_error "目录 '$1' 不存在"
        return 1
    fi
    return 0
}

# 函数：显示帮助信息
show_help() {
    echo "周报生成与邮件发送自动化系统 - 快速启动脚本"
    echo ""
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  full        完整工作流程（生成周报 -> 创建HTML -> 发送邮件）"
    echo "  quick       快速发送模式（直接发送已生成的清理版HTML周报）"
    echo "  html        仅创建HTML（不发送邮件）"
    echo "  send        仅发送邮件（不生成HTML）"
    echo "  test        测试模式（不实际发送邮件）"
    echo "  status      显示系统状态"
    echo "  logs        查看发送日志"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 full      # 完整工作流程"
    echo "  $0 quick     # 快速发送模式"
    echo "  $0 status    # 显示系统状态"
}

# 函数：显示系统状态
show_status() {
    print_info "=== 系统状态检查 ==="
    
    # 检查Python
    check_command python3
    print_success "Python3 已安装"
    
    # 检查git仓库
    if check_dir "/home/developer/my-repos/huawei-developer-demo"; then
        print_success "Git仓库存在: /home/developer/my-repos/huawei-developer-demo"
    fi
    
    # 检查脚本文件
    print_info "检查脚本文件..."
    SCRIPTS=(
        "create_clean_report.py"
        "send_clean_report.py"
        "weekly_report_full_automation.py"
    )
    
    for script in "${SCRIPTS[@]}"; do
        if check_file "/home/developer/Desktop/$script"; then
            print_success "$script 存在"
        fi
    done
    
    # 检查周报文件
    print_info "检查周报文件..."
    REPORT_FILES=$(ls -la ~/Desktop/*.md 2>/dev/null | grep -i "周报" | wc -l)
    if [ $REPORT_FILES -gt 0 ]; then
        print_success "找到 $REPORT_FILES 个周报文件"
        ls -la ~/Desktop/*.md | grep -i "周报" | head -5
    else
        print_warning "未找到周报文件"
    fi
    
    # 检查HTML文件
    print_info "检查HTML文件..."
    HTML_FILES=$(ls -la ~/Desktop/*.html 2>/dev/null | grep -i "周报" | wc -l)
    if [ $HTML_FILES -gt 0 ]; then
        print_success "找到 $HTML_FILES 个HTML周报文件"
        ls -la ~/Desktop/*.html | grep -i "周报" | head -5
    else
        print_warning "未找到HTML周报文件"
    fi
    
    # 检查发送日志
    print_info "检查发送日志..."
    if check_file "/home/developer/Desktop/email_send_log.txt"; then
        LOG_COUNT=$(wc -l < /home/developer/Desktop/email_send_log.txt)
        print_success "发送日志存在，共 $LOG_COUNT 条记录"
        echo "最新5条记录:"
        tail -5 /home/developer/Desktop/email_send_log.txt
    else
        print_warning "发送日志文件不存在"
    fi
    
    print_info "=== 状态检查完成 ==="
}

# 函数：查看发送日志
show_logs() {
    if check_file "/home/developer/Desktop/email_send_log.txt"; then
        print_info "发送日志内容:"
        echo "================================"
        cat /home/developer/Desktop/email_send_log.txt
        echo "================================"
        LOG_COUNT=$(wc -l < /home/developer/Desktop/email_send_log.txt)
        print_info "共 $LOG_COUNT 条记录"
    else
        print_error "发送日志文件不存在"
    fi
}

# 函数：完整工作流程
run_full_workflow() {
    print_info "开始完整工作流程..."
    print_info "1. 检查环境..."
    check_command python3
    check_dir "/home/developer/my-repos/huawei-developer-demo"
    
    print_info "2. 运行完整自动化脚本..."
    cd /home/developer/Desktop
    python3 weekly_report_full_automation.py
    
    if [ $? -eq 0 ]; then
        print_success "完整工作流程完成"
    else
        print_error "完整工作流程失败"
        exit 1
    fi
}

# 函数：快速发送模式
run_quick_send() {
    print_info "开始快速发送模式..."
    print_info "检查清理版HTML文件..."
    
    HTML_FILES=$(ls -la ~/Desktop/*.html 2>/dev/null | grep -i "周报" | grep -i "clean" | wc -l)
    if [ $HTML_FILES -eq 0 ]; then
        print_error "未找到清理版HTML周报文件"
        print_info "请先运行完整工作流程或创建HTML文件"
        exit 1
    fi
    
    print_info "找到清理版HTML文件，开始发送..."
    cd /home/developer/Desktop
    python3 weekly_report_full_automation.py --quick
    
    if [ $? -eq 0 ]; then
        print_success "快速发送完成"
    else
        print_error "快速发送失败"
        exit 1
    fi
}

# 函数：仅创建HTML
run_html_only() {
    print_info "开始创建HTML..."
    print_info "检查周报文件..."
    
    REPORT_FILES=$(ls -la ~/Desktop/*.md 2>/dev/null | grep -i "周报" | wc -l)
    if [ $REPORT_FILES -eq 0 ]; then
        print_error "未找到周报文件"
        print_info "请先使用gen-week-reporter技能生成周报"
        exit 1
    fi
    
    print_info "找到周报文件，开始创建HTML..."
    cd /home/developer/Desktop
    python3 create_clean_report.py
    
    if [ $? -eq 0 ]; then
        print_success "HTML创建完成"
    else
        print_error "HTML创建失败"
        exit 1
    fi
}

# 函数：仅发送邮件
run_send_only() {
    print_info "开始发送邮件..."
    print_info "检查清理版HTML文件..."
    
    HTML_FILES=$(ls -la ~/Desktop/*.html 2>/dev/null | grep -i "周报" | grep -i "clean" | wc -l)
    if [ $HTML_FILES -eq 0 ]; then
        print_error "未找到清理版HTML周报文件"
        print_info "请先创建HTML文件"
        exit 1
    fi
    
    print_info "找到清理版HTML文件，开始发送..."
    cd /home/developer/Desktop
    python3 send_clean_report.py
    
    if [ $? -eq 0 ]; then
        print_success "邮件发送完成"
    else
        print_error "邮件发送失败"
        exit 1
    fi
}

# 函数：测试模式
run_test_mode() {
    print_info "开始测试模式..."
    print_info "注意：测试模式不会实际发送邮件"
    
    # 这里可以添加测试逻辑
    print_info "测试环境检查..."
    check_command python3
    check_dir "/home/developer/Desktop"
    
    print_info "测试脚本检查..."
    if check_file "/home/developer/Desktop/create_clean_report.py" && \
       check_file "/home/developer/Desktop/send_clean_report.py"; then
        print_success "所有脚本文件存在"
    else
        print_error "缺少脚本文件"
        exit 1
    fi
    
    print_info "测试SMTP连接..."
    python3 -c "
import smtplib, ssl
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL('smtp.163.com', 465, context=context) as server:
        print('✅ SMTP服务器连接正常')
except Exception as e:
    print(f'❌ 连接失败: {e}')
"
    
    print_success "测试模式完成"
}

# 主程序
main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case "$1" in
        "full")
            run_full_workflow
            ;;
        "quick")
            run_quick_send
            ;;
        "html")
            run_html_only
            ;;
        "send")
            run_send_only
            ;;
        "test")
            run_test_mode
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "help")
            show_help
            ;;
        *)
            print_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主程序
main "$@"