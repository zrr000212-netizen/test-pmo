# 周报收集器 (Weekly Report Collector)

一个交互式周报收集工具，支持多种输入方式和模板系统，可与现有技能集成实现完整的周报管理流程。

## ✨ 功能特性

- **交互式收集**: 通过对话方式收集周报内容
- **模板系统**: 内置工程师、项目经理等专业模板
- **多种输入**: 支持命令行交互、文件导入
- **数据验证**: 自动验证输入数据的完整性
- **多格式输出**: 支持 JSON 和 Markdown 格式
- **配置管理**: 灵活的配置系统
- **扩展性强**: 易于添加新模板和功能

## 🚀 快速开始

### 安装

```bash
# 1. 确保在技能目录中
cd /home/developer/.openclaw/workspace/skills/weekly-report-collector

# 2. 运行安装脚本
chmod +x scripts/install.sh
./scripts/install.sh
```

### 基本使用

```bash
# 交互式收集周报
python3 scripts/collect.py --interactive

# 使用特定模板
python3 scripts/collect.py --interactive --template engineer

# 指定输出文件
python3 scripts/collect.py --interactive --output my_report.json

# 列出所有模板
python3 scripts/collect.py --list-templates
```

### 配置管理

```bash
# 交互式配置向导
python3 scripts/config_manager.py --setup

# 显示当前配置
python3 scripts/config_manager.py --show

# 获取特定配置
python3 scripts/config_manager.py --get default_template

# 设置配置
python3 scripts/config_manager.py --set default_template manager
```

## 📋 模板系统

### 内置模板

1. **engineer** - 工程师周报模板
   - 技术工作追踪
   - Bug修复记录
   - 代码优化和性能指标
   - 技术研究和学习进展

2. **manager** - 项目经理周报模板
   - 项目状态和健康度
   - 里程碑和交付物
   - 风险和问题管理
   - 团队状态和资源

3. **designer** - 设计师周报模板
   - 设计任务完成情况
   - 设计评审和反馈
   - 设计系统更新
   - 创意和研究工作

4. **sales** - 销售周报模板
   - 销售业绩和目标
   - 客户跟进和沟通
   - 市场反馈和竞品
   - 下周销售计划

### 自定义模板

在 `templates/` 目录下创建 `.md` 文件即可添加新模板：

```markdown
# 自定义模板

## 基本信息
- **姓名**: {{name}}
- **日期**: {{date_range}}

## 自定义部分
[你的模板内容...]
```

## 🔧 配置说明

### 配置文件位置
`~/.weekly-report-collector/config.json`

### 主要配置项

```json
{
  "default_template": "engineer",
  "auto_save": true,
  "storage_path": "~/weekly-reports",
  "git_integration": false,
  "notifications": {
    "enabled": true,
    "reminder_day": "friday",
    "reminder_time": "17:00"
  },
  "email": {
    "enabled": false,
    "smtp_host": "",
    "smtp_port": 587,
    "smtp_user": "",
    "default_recipients": []
  }
}
```

### 环境变量

```bash
# SMTP配置（用于邮件发送）
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"

# 周报系统配置
export WEEKLY_REPORT_STORAGE="$HOME/weekly-reports"
export WEEKLY_REPORT_DEFAULT_TEMPLATE="engineer"
```

## 🔗 与其他技能集成

### 与 smart-weekly-report 集成

收集的数据可以传递给 smart-weekly-report 技能进行格式化：

```bash
# 收集周报数据
python3 scripts/collect.py --interactive --output raw_data.json

# 使用 smart-weekly-report 格式化
# （需要 smart-weekly-report 技能支持 JSON 输入）
```

### 与 email-send 集成

配置 SMTP 信息后，可以自动发送周报邮件：

```bash
# 配置邮件设置
python3 scripts/config_manager.py --setup

# 发送周报邮件
# （需要 email-send 技能）
```

## 📁 文件结构

```
weekly-report-collector/
├── SKILL.md                    # 技能定义文档
├── README.md                   # 本文档
├── requirements.txt            # Python依赖
├── scripts/
│   ├── collect.py             # 主收集脚本
│   ├── config_manager.py      # 配置管理
│   └── install.sh            # 安装脚本
├── templates/                  # 模板目录
│   ├── engineer.md            # 工程师模板
│   ├── manager.md             # 项目经理模板
│   ├── designer.md            # 设计师模板
│   └── sales.md               # 销售模板
└── examples/                   # 示例文件
    └── basic_usage.md         # 使用示例
```

## 📊 数据格式

### JSON 格式示例

```json
{
  "report_id": "weekly_report_20260415_143022",
  "created_at": "2026-04-15T14:30:22.123456",
  "author": "张三",
  "role": "软件工程师",
  "template": "engineer",
  "content": {
    "completed": ["任务1", "任务2"],
    "in_progress": ["任务3 (50%)"],
    "blockers": ["问题描述"],
    "next_week": ["计划1", "计划2"],
    "metrics": {"commits": 12}
  }
}
```

### 存储位置

- JSON 报告: `~/weekly-reports/[report_id].json`
- Markdown 报告: `~/weekly-reports/[report_id].md`
- 配置文件: `~/.weekly-report-collector/config.json`

## 🛠️ 开发指南

### 添加新功能

1. **添加新模板**:
   - 在 `templates/` 目录创建 `.md` 文件
   - 在 `collect.py` 中添加对应的收集方法

2. **扩展收集器**:
   - 继承 `WeeklyReportCollector` 类
   - 实现新的收集方法
   - 更新命令行参数解析

3. **集成新技能**:
   - 在 `scripts/` 目录创建集成脚本
   - 更新 `SKILL.md` 文档

### 测试

```bash
# 运行测试（需要安装pytest）
pytest tests/

# 调试模式
python3 scripts/collect.py --interactive --debug
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

- 基于 OpenClaw 技能系统开发
- 与 smart-weekly-report、email-send 技能兼容
- 感谢所有贡献者和用户

## 📞 支持

如有问题或建议：
1. 查看 `examples/basic_usage.md`
2. 使用 `--debug` 参数运行
3. 提交 Issue 或 Pull Request