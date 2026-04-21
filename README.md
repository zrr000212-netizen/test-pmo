# PMO Skills - 项目运作技能集合

此项目用于添加项目运作相关的 OpenClaw 技能。

## 包含的技能

### 1. weekly-report-collector - 周报收集器
交互式周报收集器，支持多种模板和配置管理。

**功能特性:**
- 交互式命令行界面
- 多种职业模板（工程师、项目经理等）
- 数据验证和格式化
- JSON 和 Markdown 输出
- 配置管理系统
- 邮件发送集成

**快速开始:**
```bash
cd skills/weekly-report-collector
chmod +x scripts/install.sh
./scripts/install.sh
python3 scripts/collect.py --interactive
```

### 2. email-send - 邮件发送技能
通过 SMTP 发送邮件的技能，支持多种邮件服务器配置。

**功能特性:**
- 支持多种 SMTP 服务器
- 支持附件发送
- 集成 msmtp 客户端
- 简单易用的接口
- 支持 163邮箱、Gmail 等

**配置示例:**
```bash
# 配置 163邮箱
export SMTP_HOST="smtp.163.com"
export SMTP_PORT="465"
export SMTP_USER="your-email@163.com"
export SMTP_PASS="your-auth-code"
```

### 3. smart-weekly-report - 智能周报生成器
将自然语言描述转换为结构化周报的智能生成器。

**功能特性:**
- 自然语言处理
- 多种职业角色支持
- 自动信息提炼
- 结构化输出
- 智能模板匹配

### 4. gen-week-reporter-email-automation - 周报生成与邮件发送自动化
完整的周报生成和邮件发送自动化工作流程，从生成周报到发送HTML邮件的完整流程。

**功能特性:**
- 自动生成git仓库周报
- 清理版HTML格式转换
- 自动移除不需要的元数据
- 163邮箱SMTP集成
- 完整的错误处理和日志记录
- 支持定时任务自动化

**快速开始:**
```bash
cd skills/gen-week-reporter-email-automation
python3 scripts/weekly_report_full_automation.py
```
- 支持定时任务自动化

**快速开始:**
```bash
cd skills/gen-week-reporter-email-automation
python3 scripts/weekly_report_full_automation.py
```

## 系统架构

```
周报收集 → 智能格式化 → 邮件发送 → 存储存档
   ↓            ↓           ↓         ↓
收集器技能   生成器技能   邮件技能   本地/Git存储
```

## 使用场景

### 项目经理 (PM)
1. 使用 `weekly-report-collector` 收集团队周报
2. 使用 `smart-weekly-report` 智能生成汇总报告
3. 使用 `email-send` 发送周报给相关人员

### 工程师
1. 使用工程师模板填写个人周报
2. 自动保存为 JSON/Markdown 格式
3. 可选邮件发送给项目经理

### 团队协作
1. 统一周报格式和模板
2. 自动化收集和汇总
3. 邮件通知和存档

## 安装和使用

### 方法一：逐个安装
```bash
# 安装周报收集器
openclaw skill install skills/weekly-report-collector

# 安装邮件发送技能
openclaw skill install skills/email-send

# 安装智能周报生成器
openclaw skill install skills/smart-weekly-report
```

### 方法二：批量安装
```bash
# 安装所有技能
for skill in skills/*; do
  if [ -d "$skill" ]; then
    openclaw skill install "$skill"
  fi
done
```

## 配置说明

### 环境变量
```bash
# 邮件配置
export SMTP_HOST="smtp.163.com"
export SMTP_PORT="465"
export SMTP_USER="your-email@163.com"
export SMTP_PASS="your-auth-code"

# 周报系统配置
export WEEKLY_REPORT_STORAGE="~/weekly-reports"
export WEEKLY_REPORT_DEFAULT_TEMPLATE="engineer"
export WEEKLY_REPORT_AUTO_SEND="true"
```

### 配置文件
周报收集器的配置文件位于 `~/.weekly-report-collector/config.json`:
```json
{
  "default_template": "engineer",
  "auto_save": true,
  "storage_path": "~/weekly-reports",
  "email": {
    "enabled": true,
    "smtp_host": "smtp.163.com",
    "smtp_port": 465,
    "smtp_user": "your-email@163.com",
    "default_recipient": "manager@example.com"
  },
  "notifications": {
    "enabled": true,
    "reminder_day": "friday",
    "reminder_time": "17:00"
  }
}
```

## 开发指南

### 添加新技能
1. 在 `skills/` 目录下创建新技能目录
2. 包含以下文件：
   - `SKILL.md` - 技能定义文档
   - `README.md` - 使用说明
   - `_meta.json` - 技能元数据
   - 其他必要的脚本和配置文件

### 技能结构要求
```
技能名称/
├── SKILL.md          # 技能定义（必须）
├── README.md         # 使用文档（推荐）
├── _meta.json        # 元数据（必须）
├── requirements.txt  # Python依赖（可选）
├── scripts/          # 脚本目录（推荐）
└── templates/        # 模板目录（可选）
```

### 提交规范
1. 每个技能独立目录
2. 提供完整的文档
3. 包含使用示例
4. 测试通过后再提交

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献步骤
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 联系方式

- 仓库地址: https://gitcode.com/developer-skill/pmo-skill
- 问题反馈: 请在 Issues 页面提交

---

**最后更新**: 2026-04-21
**版本**: 1.0.1
**状态**: ✅ 所有技能已完全实现并测试