# 周报收集器使用示例

## 基本使用

### 1. 交互式收集周报

```bash
# 启动交互式收集
python3 scripts/collect.py --interactive

# 使用特定模板
python3 scripts/collect.py --interactive --template engineer

# 指定输出文件
python3 scripts/collect.py --interactive --output my_report.json
```

### 2. 配置管理器

```bash
# 交互式配置向导
python3 scripts/config_manager.py --setup

# 显示当前配置
python3 scripts/config_manager.py --show

# 显示特定配置项
python3 scripts/config_manager.py --show email

# 获取配置值
python3 scripts/config_manager.py --get default_template

# 设置配置值
python3 scripts/config_manager.py --set default_template manager
python3 scripts/config_manager.py --set notifications.enabled true
python3 scripts/config_manager.py --set email.smtp_port 587
```

### 3. 列出可用模板

```bash
python3 scripts/collect.py --list-templates
```

## 使用示例

### 示例 1: 完整工作流

```bash
# 1. 首次配置
python3 scripts/config_manager.py --setup

# 2. 收集周报 (使用工程师模板)
python3 scripts/collect.py --interactive --template engineer --output weekly_report_2026-04-15.json

# 3. 查看生成的报告
cat weekly_report_2026-04-15.json | jq .

# 4. 查看Markdown格式
cat weekly_report_2026-04-15.md
```

### 示例 2: 批量处理

```bash
# 创建批处理脚本
cat > collect_weekly.sh << 'EOF'
#!/bin/bash
# 周报自动收集脚本

REPORT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="weekly_report_${REPORT_DATE}.json"

echo "开始收集周报..."
python3 scripts/collect.py --interactive --template engineer --output "$REPORT_FILE"

if [ $? -eq 0 ]; then
    echo "周报已保存到: $REPORT_FILE"
    
    # 可选: 自动发送邮件
    # python3 scripts/send_report.py --report "$REPORT_FILE"
else
    echo "周报收集失败"
    exit 1
fi
EOF

chmod +x collect_weekly.sh
./collect_weekly.sh
```

### 示例 3: 集成到工作流

```bash
# 在Git提交后自动收集周报
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Git提交后自动记录到周报

if [ -f "weekly_report_current.json" ]; then
    # 获取本次提交信息
    COMMIT_MSG=$(git log -1 --pretty=%B)
    COMMIT_AUTHOR=$(git log -1 --pretty=%an)
    COMMIT_DATE=$(git log -1 --pretty=%cd --date=short)
    
    # 添加到周报
    python3 -c "
import json
import sys

try:
    with open('weekly_report_current.json', 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    if 'git_commits' not in report['content']:
        report['content']['git_commits'] = []
    
    report['content']['git_commits'].append({
        'date': '$COMMIT_DATE',
        'author': '$COMMIT_AUTHOR',
        'message': '$COMMIT_MSG'
    })
    
    with open('weekly_report_current.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print('✅ Git提交已记录到周报')
except Exception as e:
    print(f'❌ 记录Git提交失败: {e}')
    sys.exit(1)
"
fi
EOF

chmod +x .git/hooks/post-commit
```

## 配置文件示例

### 完整配置文件 (~/.weekly-report-collector/config.json)

```json
{
  "default_template": "engineer",
  "auto_save": true,
  "storage_path": "~/weekly-reports",
  "git_integration": false,
  "notifications": {
    "enabled": true,
    "reminder_day": "friday",
    "reminder_time": "17:00",
    "email_reminder": false,
    "email_recipients": []
  },
  "email": {
    "enabled": true,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your-email@gmail.com",
    "smtp_password": "",
    "default_recipients": [
      "manager@company.com",
      "team@company.com"
    ]
  },
  "templates": {
    "engineer": "工程师周报模板",
    "manager": "项目经理周报模板",
    "designer": "设计师周报模板",
    "sales": "销售周报模板"
  }
}
```

### 环境变量设置

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"  # 使用应用专用密码

# 周报系统配置
export WEEKLY_REPORT_STORAGE="$HOME/weekly-reports"
export WEEKLY_REPORT_DEFAULT_TEMPLATE="engineer"
export WEEKLY_REPORT_AUTO_SEND="true"
```

## 报告数据结构示例

### JSON格式报告

```json
{
  "report_id": "weekly_report_20260415_143022",
  "created_at": "2026-04-15T14:30:22.123456",
  "author": "张三",
  "role": "软件工程师",
  "department": "产品研发部",
  "date_range": "2026-04-08 到 2026-04-12",
  "template": "engineer",
  "content": {
    "completed": [
      "完成用户登录模块重构",
      "修复了5个生产环境bug",
      "优化了API响应时间，从200ms降到50ms"
    ],
    "in_progress": [
      "支付功能开发 - 进度70%",
      "性能测试 - 进度30%"
    ],
    "blockers": [
      "第三方支付接口文档不完整",
      "测试环境数据库性能问题"
    ],
    "next_week": [
      "完成支付功能开发",
      "进行系统性能测试",
      "编写技术文档"
    ],
    "metrics": {
      "commits": "15",
      "prs": "3",
      "code_review": "5"
    }
  },
  "metadata": {
    "source": "interactive",
    "template": "engineer",
    "version": "1.0.0"
  }
}
```

### Markdown格式报告

```markdown
# 周报 - 张三

**日期**: 2026-04-08 到 2026-04-12
**模板**: engineer
**生成时间**: 2026-04-15T14:30:22.123456
**角色**: 软件工程师
**部门/项目**: 产品研发部

---

## ✅ 本周完成

- 完成用户登录模块重构
- 修复了5个生产环境bug
- 优化了API响应时间，从200ms降到50ms

## 🔄 进行中

- 支付功能开发 - 进度70%
- 性能测试 - 进度30%

## 🚧 问题与阻碍

- 第三方支付接口文档不完整
- 测试环境数据库性能问题

## 📅 下周计划

- 完成支付功能开发
- 进行系统性能测试
- 编写技术文档

## 📊 关键指标

- **commits**: 15
- **prs**: 3
- **code_review**: 5
```

## 故障排除

### 常见问题

1. **权限错误**
   ```bash
   # 确保有写入权限
   chmod +x scripts/*.py
   chmod 755 ~/weekly-reports
   ```

2. **Python依赖问题**
   ```bash
   # 确保使用Python 3.8+
   python3 --version
   
   # 安装所需依赖
   pip3 install --user -r requirements.txt
   ```

3. **配置文件问题**
   ```bash
   # 重新生成配置文件
   rm ~/.weekly-report-collector/config.json
   python3 scripts/config_manager.py --setup
   ```

4. **模板找不到**
   ```bash
   # 检查模板文件
   ls -la templates/
   
   # 重新下载模板
   cp -r /path/to/templates/* templates/
   ```

### 调试模式

```bash
# 启用调试输出
python3 scripts/collect.py --interactive --debug

# 查看详细日志
export WEEKLY_REPORT_DEBUG=1
python3 scripts/collect.py --interactive
```

## 进阶用法

### 自定义模板

1. 在 `templates/` 目录创建新模板文件，如 `my_template.md`
2. 模板会自动被发现和使用
3. 使用 `--template my_template` 参数

### 自动化脚本

```bash
#!/bin/bash
# 自动化周报收集和发送

# 配置
TEMPLATE="engineer"
OUTPUT_DIR="$HOME/weekly-reports"
REPORT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="$OUTPUT_DIR/weekly_${REPORT_DATE}.json"

# 收集周报
echo "开始收集周报..."
python3 scripts/collect.py --interactive --template "$TEMPLATE" --output "$REPORT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ 周报收集完成: $REPORT_FILE"
    
    # 转换为Markdown
    MD_FILE="${REPORT_FILE%.json}.md"
    python3 -c "
import json
import sys

with open('$REPORT_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('$MD_FILE', 'w', encoding='utf-8') as f:
    f.write(f'# 周报 - {data[\"author\"]}\\n\\n')
    f.write(f'**日期**: {data[\"date_range\"]}\\n')
    # ... 更多格式化代码
"
    
    echo "✅ Markdown版本: $MD_FILE"
    
    # 可选: 发送邮件
    # if [ -n "$SMTP_USER" ]; then
    #     python3 scripts/send_report.py --report "$REPORT_FILE"
    # fi
else
    echo "❌ 周报收集失败"
    exit 1
fi
```

### 与现有系统集成

```python
# 在你的Python项目中集成
import sys
sys.path.append('/path/to/weekly-report-collector/scripts')

from collect import WeeklyReportCollector

# 创建收集器实例
collector = WeeklyReportCollector(storage_path='/custom/path')

# 收集周报
report = collector.collect_interactive(template='engineer')

# 保存报告
saved_path = collector.save_report(report)

print(f"周报已保存到: {saved_path}")
```

## 支持与反馈

如有问题或建议，请：
1. 检查日志文件
2. 使用 `--debug` 参数运行
3. 查看 `examples/` 目录中的示例
4. 提交Issue或Pull Request