#!/bin/bash
# 周报收集器安装脚本

set -e

echo "🚀 开始安装周报收集器..."

# 检查Python版本
echo "🔍 检查Python版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3.8或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查必要的目录
echo "📁 创建必要的目录..."
mkdir -p ~/weekly-reports
mkdir -p ~/.weekly-report-collector
mkdir -p templates

echo "✅ 目录创建完成"

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x scripts/*.py 2>/dev/null || true

# 运行配置向导
echo "🎯 运行配置向导..."
if [ -f "scripts/config_manager.py" ]; then
    python3 scripts/config_manager.py --setup
else
    echo "⚠️  配置脚本未找到，跳过配置向导"
fi

# 创建示例报告目录
echo "📝 创建示例..."
if [ -d "examples" ]; then
    cp examples/* ~/.weekly-report-collector/ 2>/dev/null || true
fi

# 测试收集器
echo "🧪 测试收集器..."
if [ -f "scripts/collect.py" ]; then
    echo "📋 可用模板:"
    python3 scripts/collect.py --list-templates
else
    echo "❌ 收集器脚本未找到"
fi

# 显示使用说明
echo ""
echo "🎉 安装完成!"
echo "=" * 50
echo ""
echo "📖 使用说明:"
echo "1. 交互式收集周报:"
echo "   python3 scripts/collect.py --interactive"
echo ""
echo "2. 查看配置:"
echo "   python3 scripts/config_manager.py --show"
echo ""
echo "3. 修改配置:"
echo "   python3 scripts/config_manager.py --setup"
echo ""
echo "4. 查看示例:"
echo "   cat examples/basic_usage.md"
echo ""
echo "📁 报告存储目录: ~/weekly-reports/"
echo "⚙️  配置文件: ~/.weekly-report-collector/config.json"
echo ""
echo "💡 提示: 可以将脚本添加到PATH或创建别名"
echo "   alias weekly-report='python3 /path/to/scripts/collect.py'"
echo ""
echo "🔗 与smart-weekly-report集成:"
echo "   收集周报后，可以使用smart-weekly-report技能进行格式化"
echo ""
echo "📧 与email-send集成:"
echo "   配置SMTP信息后，可以自动发送周报邮件"
echo ""
echo "=" * 50
echo "✨ 开始使用: python3 scripts/collect.py --interactive"