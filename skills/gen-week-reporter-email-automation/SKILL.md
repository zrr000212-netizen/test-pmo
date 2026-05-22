---
name: gen-week-reporter-email-automation
description: 完整的周报生成和邮件发送自动化工作流程 - 从生成周报到发送HTML邮件的完整流程
tags: [周报, 邮件, 自动化, 工作流程, gen-week-reporter]
author: zrr
version: 1.0.0
created: 2026-04-21
---

# 周报生成与邮件发送自动化工作流程

## 概述

这个技能提供了完整的周报生成和邮件发送自动化工作流程。它整合了以下功能：

1. 使用gen-week-reporter技能生成周报
2. 创建清理版HTML格式（移除不需要的元数据）
3. 发送HTML格式周报到指定邮箱
4. 完整的错误处理和日志记录

## 触发条件

当用户需要：

- 生成周报并发送邮件
- 自动化周报工作流程
- 从git仓库生成周报并发送给指定收件人

## 工作流程

### 完整工作流程

1. **检查环境**：验证git仓库、脚本文件和依赖项
2. **生成周报**：使用gen-week-reporter技能生成Markdown周报
3. **转换HTML**：创建清理版HTML格式，移除不需要的元数据
4. **发送邮件**：通过163邮箱SMTP发送HTML周报
5. **记录日志**：保存发送记录和时间戳

### 快速工作流程（已有周报文件）

1. **查找最新周报**：自动查找桌面上的最新周报文件
2. **转换HTML**：创建清理版HTML格式
3. **发送邮件**：发送HTML周报到邮箱

## 前提条件

### 1. 邮箱配置

所有邮箱配置通过环境变量设置，不要硬编码在代码中：

| 环境变量 | 说明 | 默认值 | 必需 |
|----------|------|--------|------|
| `SENDER_EMAIL` | 发件人邮箱 | `your-email@163.com` | 是 |
| `SENDER_NAME` | 发件人名称 | `your-name` | 是 |
| `SMTP_AUTH_CODE` | SMTP客户端授权码 | (无) | 是 |
| `RECEIVER_EMAIL` | 收件人邮箱 | `recipient@example.com` | 是 |
| `SMTP_SERVER` | SMTP服务器地址 | `smtp.163.com` | 否 |
| `SMTP_PORT` | SMTP端口 | `465` | 否 |

配置示例：

```bash
export SENDER_EMAIL="your-email@163.com"
export SENDER_NAME="your-name"
export SMTP_AUTH_CODE="your-auth-code"
export RECEIVER_EMAIL="recipient@example.com"
```

### 2. 文件依赖

- Python 3.x环境
- 桌面目录中的脚本文件
- Git仓库：/home/developer/my-repos/huawei-developer-demo

### 3. 脚本文件位置

所有脚本文件应位于：`/home/developer/Desktop/`

- `create_clean_report.py` - 创建清理版HTML
- `send_clean_report.py` - 发送清理版邮件

## 使用方法

### 方法1：完整自动化流程（推荐）

```bash
# 进入桌面目录
cd /home/developer/Desktop

# 运行完整自动化脚本
python3 weekly_report_automation.py
```

### 方法2：分步执行

```bash
# 步骤1：生成周报（使用gen-week-reporter技能）
# 确保在git仓库目录
cd /home/developer/my-repos/huawei-developer-demo

# 使用gen-week-reporter技能生成周报
# 技能会自动生成周报到桌面

# 步骤2：进入桌面目录
cd /home/developer/Desktop

# 步骤3：创建清理版HTML
python3 create_clean_report.py

# 步骤4：发送邮件
python3 send_clean_report.py
```

### 方法3：快速发送（已有周报文件）

```bash
# 进入桌面目录
cd /home/developer/Desktop

# 快速发送模式
python3 weekly_report_automation.py --quick
```

## 详细步骤说明

### 步骤1：生成周报（gen-week-reporter技能）

gen-week-reporter技能会自动：

1. 导航到git仓库目录
2. 检查git提交历史
3. 查看子模块状态
4. 分析各子模块最新提交
5. 统计新增/修改案例
6. 查找舆情报告文件
7. 提取核心指标数据
8. 生成Markdown格式周报文件到桌面

**输出文件**：`最佳实践与用户反馈周报_YYYY年MM月DD日_gen-week-reporter生成.md`

### 步骤2：创建清理版HTML

`create_clean_report.py`脚本会：

1. 查找最新的周报文件
2. 读取Markdown内容
3. 移除不需要的元数据：
   - 报告生成时间
   - 数据来源
   - 监控周期
   - 报告数量
   - 最佳实践案例数量
   - 风险提示
   - 后续计划
4. 转换为HTML格式
5. 添加专业CSS样式
6. 保存为清理版HTML文件

**输出文件**：`最佳实践与用户反馈周报_YYYY年MM月DD日_gen-week-reporter生成_clean.html`

### 步骤3：发送邮件

`send_clean_report.py`脚本会：

1. 读取清理版HTML文件
2. 创建邮件消息（HTML + 纯文本备用）
3. 配置发件人/收件人信息
4. 连接到163邮箱SMTP服务器
5. 发送邮件
6. 记录发送日志

**发送日志**：`/home/developer/Desktop/email_send_log.txt`

## 文件发现逻辑

### 周报文件查找

脚本会自动查找桌面目录中最新的周报文件：

1. 查找所有包含"周报"的.md文件
2. 按修改时间排序
3. 优先使用gen-week-reporter生成的文件
4. 如果不存在，使用最新的可用周报文件

### HTML文件生成

清理版HTML文件命名规则：

- 输入：`最佳实践与用户反馈周报_YYYY年MM月DD日_gen-week-reporter生成.md`
- 输出：`最佳实践与用户反馈周报_YYYY年MM月DD日_gen-week-reporter生成_clean.html`

## 脚本文件说明

### create_clean_report.py

```python
#!/usr/bin/env python3
"""
创建清理版HTML周报
移除不需要的元数据：
1. 报告生成时间
2. 数据来源
3. 监控周期
4. 报告数量
5. 最佳实践案例数量
6. 风险提示
7. 后续计划
"""

# 主要功能：
# 1. 查找最新周报文件
# 2. 读取Markdown内容
# 3. 清理元数据
# 4. 转换为HTML
# 5. 保存为清理版HTML文件
```

### send_clean_report.py

```python
#!/usr/bin/env python3
"""
发送清理版HTML周报到邮箱
已移除以下内容：
1. 报告生成时间
2. 数据来源
3. 监控周期
4. 报告数量
5. 最佳实践案例数量
6. 风险提示
7. 后续计划
"""

# 主要功能：
# 1. 读取清理版HTML文件
# 2. 创建邮件消息
# 3. 配置SMTP连接
# 4. 发送邮件
# 5. 记录日志
```

### weekly_report_automation.py

```python
#!/usr/bin/env python3
"""
周报邮件发送自动化脚本
完整的工作流程：生成清理版HTML -> 发送强调重点的邮件
"""

# 主要功能：
# 1. 检查依赖项
# 2. 查找最新周报文件
# 3. 创建清理版HTML报告
# 4. 发送邮件
# 5. 支持快速发送模式
```

## 邮件格式特点

### 清理版邮件特点

1. **简洁专业**：移除所有冗余元数据，只保留核心内容
2. **重点突出**：
   - 使用标题和副标题清晰分层
   - 关键数据加粗显示
   - 使用分隔线区分不同部分
3. **响应式设计**：适配各种设备屏幕
4. **专业排版**：
   - 合理的行间距和段落间距
   - 统一的字体和颜色方案
   - 清晰的视觉引导

### 移除的元数据说明

这些信息被移除是因为：

1. **报告生成时间**：邮件发送时间已经足够
2. **数据来源**：内部流程信息，对外不必要
3. **监控周期**：可以从报告内容推断
4. **报告数量**：不增加信息价值
5. **最佳实践案例数量**：已在内容中体现
6. **风险提示**：过于技术性，适合内部讨论
7. **后续计划**：行动计划类信息，适合内部跟踪

## 配置修改

邮箱配置通过环境变量管理，无需修改代码。设置方式：

```bash
# 设置环境变量（推荐写入 ~/.bashrc 或 .env 文件）
export SENDER_EMAIL="your-email@163.com"
export SENDER_NAME="your-name"
export SMTP_AUTH_CODE="your-auth-code"
export RECEIVER_EMAIL="recipient@example.com"
export SMTP_SERVER="smtp.163.com"
export SMTP_PORT="465"
```

或在 `templates/config.py` 中修改默认值（不推荐提交到版本控制）。

## 故障排除

### 常见问题及解决方案

#### 1. 周报文件不存在

```text
错误：未找到周报文件
解决方案：先使用gen-week-reporter技能生成周报
```

#### 2. HTML文件不存在

```text
错误：HTML周报文件不存在
解决方案：先运行create_clean_report.py生成HTML文件
```

#### 3. 发送失败：认证错误

```text
错误：SMTP认证失败
解决方案：检查客户端授权码是否正确
```

#### 4. 发送失败：连接超时

```text
错误：连接SMTP服务器超时
解决方案：检查网络连接，确认SMTP服务器地址和端口
```

#### 5. 脚本文件不存在

```text
错误：No such file or directory
解决方案：确保脚本文件在桌面目录
ls -la ~/Desktop/*.py
```

### 测试连接

```bash
# 测试SMTP连接
python3 -c "
import smtplib, ssl
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL('smtp.163.com', 465, context=context) as server:
        print('SMTP服务器连接正常')
except Exception as e:
    print(f'连接失败: {e}')
"
```

### 文件权限检查

```bash
# 检查脚本执行权限
chmod +x /home/developer/Desktop/*.py

# 检查文件是否存在
ls -la ~/Desktop/*.py
ls -la ~/Desktop/*.md | grep -i "周报"
```

## 自动化部署

### 设置定时任务（Cron Job）

每周一早上9点自动发送周报：

```bash
# 编辑crontab
crontab -e

# 添加以下行
0 9 * * 1 cd /home/developer/Desktop && python3 weekly_report_automation.py
```

### 完整自动化脚本

```bash
#!/bin/bash
# weekly_report_auto.sh

# 切换到工作目录
cd /home/developer/my-repos/huawei-developer-demo

# 生成周报（假设gen-week-reporter技能已安装）
# 这里需要根据实际技能调用方式调整

# 切换到桌面目录
cd /home/developer/Desktop

# 创建清理版HTML
python3 create_clean_report.py

# 发送邮件
python3 send_clean_report.py

# 记录日志
echo "$(date): 周报自动发送完成" >> /home/developer/Desktop/weekly_report_auto.log
```

## 日志和监控

### 发送日志

所有发送操作记录在：`/home/developer/Desktop/email_send_log.txt`
格式：`YYYY-MM-DD HH:MM:SS - 发送清理版HTML周报到 收件人邮箱 - 文件: 文件名`

### 查看日志

```bash
# 查看所有发送记录
cat /home/developer/Desktop/email_send_log.txt

# 查看最新5条记录
tail -5 /home/developer/Desktop/email_send_log.txt

# 查看今天发送的记录
grep "$(date +%Y-%m-%d)" /home/developer/Desktop/email_send_log.txt
```

## 文件结构

```text
/home/developer/Desktop/
├── 最佳实践与用户反馈周报_2026年04月21日_gen-week-reporter生成.md    # 原始Markdown周报
├── 最佳实践与用户反馈周报_2026年04月21日_gen-week-reporter生成_clean.html  # 清理版HTML
├── create_clean_report.py      # 创建清理版HTML脚本
├── send_clean_report.py        # 发送清理版周报脚本
├── send_optimized_report.py    # 发送优化版周报脚本
├── send_weekly_report.py       # 发送标准版周报脚本
├── weekly_report_automation.py # 完整自动化脚本
├── email_send_log.txt          # 发送日志
└── 周报发送完成总结_清理版.md   # 使用说明文档
```

## 扩展功能

### 1. 多收件人支持

```python
# 修改send_clean_report.py
receiver_emails = ["${RECEIVER_EMAIL}", "other@example.com"]
```

### 2. 附件功能

支持添加PDF或Word版本附件

### 3. 模板系统

支持多种邮件模板选择

### 4. 发送统计

统计发送成功率和打开率

### 5. 错误重试

发送失败时自动重试

### 6. 内容验证

发送前检查邮件内容完整性

## 最佳实践

### 1. 定期清理

```bash
# 清理旧的周报文件（保留最近7天）
find ~/Desktop -name "*周报*" -type f -mtime +7 -delete
```

### 2. 备份重要文件

```bash
# 备份发送日志
cp /home/developer/Desktop/email_send_log.txt \
  /home/developer/Desktop/email_send_log_$(date +%Y%m%d).txt
```

### 3. 监控发送状态

```bash
# 检查最近发送状态
tail -10 /home/developer/Desktop/email_send_log.txt
```

### 4. 测试发送

```bash
# 测试发送到测试邮箱
# 修改receiver_email为测试邮箱地址
```

## 参考文档

- [gen-week-reporter 技能 (smart-weekly-report) — 周报生成技能
- [email-send 技能 (email-send) — 邮件发送技能
- [msmtp 官方文档](https://marlam.de/msmtp/) — SMTP 客户端
- [Python smtplib](https://docs.python.org/3/library/smtplib.html) — 邮件发送库

## 更新日志

### v1.0 (2026-04-21)

- 初始版本发布
- 完整的周报生成和邮件发送工作流程
- 自动清理元数据功能
- 专业HTML邮件格式
- 完整的错误处理和日志记录
- 支持快速发送模式

## 联系支持

如有问题或建议，请联系：

- 作者：zrr
- 邮箱：通过 SENDER_EMAIL 环境变量配置
- 更新时间：2026年04月21日