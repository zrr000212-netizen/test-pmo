---
name: weekly-report-collector
description: "周报收集器 - 交互式收集周报内容，支持多种输入方式和模板。与 smart-weekly-report 和 email-send 技能集成，实现完整的周报管理流程。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["python3"] },
        "recommends": { "skills": ["smart-weekly-report", "email-send"] },
        "install": [],
      },
  }
---

# 周报收集器技能

## 功能概述

周报收集器是一个交互式工具，帮助用户收集、整理和结构化周报内容。支持多种输入方式，可与现有的 smart-weekly-report 和 email-send 技能无缝集成。

## 使用场景

1. **交互式收集** - 通过对话方式收集周报内容
2. **模板驱动** - 使用预定义或自定义模板
3. **文件导入** - 从 Markdown、JSON、CSV 文件导入
4. **Git集成** - 从 Git 提交记录自动提取工作内容

## 快速开始

### 交互式收集
```bash
# 启动交互式周报收集
python3 scripts/collect.py --interactive

# 使用特定模板
python3 scripts/collect.py --template engineer

# 从文件导入
python3 scripts/collect.py --file weekly_work.md
```

### 命令行参数
```bash
python3 scripts/collect.py --help
```

## 模板系统

### 内置模板
- `engineer` - 工程师周报模板
- `manager` - 项目经理周报模板  
- `designer` - 设计师周报模板
- `sales` - 销售周报模板

### 自定义模板
在 `templates/` 目录下创建 `.md` 文件，格式参考 `templates/engineer.md`。

## 数据结构

收集的周报数据保存为 JSON 格式：
```json
{
  "report_id": "2026-04-15_weekly",
  "created_at": "2026-04-15T20:15:00Z",
  "author": "用户名",
  "role": "engineer",
  "template": "engineer",
  "content": {
    "completed": ["任务1", "任务2"],
    "in_progress": ["任务3 (50%)"],
    "blockers": ["问题描述"],
    "next_week": ["计划1", "计划2"],
    "metrics": {"commits": 12, "prs": 3}
  },
  "metadata": {
    "source": "interactive",
    "file_path": "/path/to/report.json"
  }
}
```

## 与 smart-weekly-report 集成

收集的数据可以直接传递给 smart-weekly-report 技能进行格式化：

```bash
# 收集周报数据
python3 scripts/collect.py --interactive --output raw_data.json

# 使用 smart-weekly-report 格式化
# (假设 smart-weekly-report 支持 JSON 输入)
cat raw_data.json | smart-weekly-report --format markdown > formatted_report.md
```

## 与 email-send 集成

格式化后的周报可以通过 email-send 技能发送：

```bash
# 发送周报邮件
python3 scripts/send_report.py --report formatted_report.md --to "manager@example.com"
```

## 配置

### 环境变量
```bash
export WEEKLY_REPORT_STORAGE="$HOME/weekly-reports"
export WEEKLY_REPORT_DEFAULT_TEMPLATE="engineer"
export WEEKLY_REPORT_AUTO_SAVE="true"
```

### 配置文件
`~/.weekly-report-collector/config.json`:
```json
{
  "default_template": "engineer",
  "auto_save": true,
  "storage_path": "$HOME/weekly-reports",
  "git_integration": false,
  "notifications": {
    "enabled": true,
    "reminder_day": "friday",
    "reminder_time": "17:00"
  }
}
```

## 示例

### 示例 1: 基本使用
```bash
# 交互式收集周报
python3 scripts/collect.py --interactive

# 输出:
# 请选择角色: [1] 工程师 [2] 项目经理 [3] 设计师
# 请输入本周完成的工作: 完成了用户登录模块重构，修复了5个bug
# 请输入遇到的问题: 第三方API响应慢，需要优化
# 请输入下周计划: 开发支付功能，优化性能
```

### 示例 2: 使用模板
```bash
# 使用工程师模板
python3 scripts/collect.py --template engineer --output my_report.json

# 预览收集的数据
cat my_report.json | jq .
```

### 示例 3: 完整流程
```bash
# 1. 收集周报
python3 scripts/collect.py --interactive --output raw.json

# 2. 格式化周报
# (这里需要 smart-weekly-report 技能支持 JSON 输入)
# python3 scripts/format.py --input raw.json --output formatted.md

# 3. 发送周报
# (这里需要 email-send 技能配置)
# python3 scripts/send.py --report formatted.md --to "team@example.com"
```

## 开发指南

### 添加新模板
1. 在 `templates/` 目录创建新模板文件
2. 更新 `scripts/templates.py` 中的模板注册
3. 测试模板使用

### 扩展输入源
1. 在 `scripts/collect.py` 中添加新的收集器类
2. 实现 `collect()` 方法
3. 更新命令行参数解析

### 集成其他技能
1. 查看目标技能的 API 文档
2. 在 `scripts/integration.py` 中添加适配器
3. 测试集成功能

## 故障排除

### 常见问题
1. **模板找不到**: 检查 `templates/` 目录是否存在对应文件
2. **权限错误**: 确保有写入 `storage_path` 的权限
3. **导入失败**: 检查文件格式是否符合要求

### 调试模式
```bash
python3 scripts/collect.py --debug --interactive
```

## 更新日志

### v1.0.0
- 初始版本发布
- 支持交互式收集
- 支持模板系统
- 支持文件导入
- 基础数据验证

## 许可证
MIT