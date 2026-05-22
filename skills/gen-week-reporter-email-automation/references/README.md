# 周报生成与邮件发送自动化系统

## 概述

这是一个完整的周报生成和邮件发送自动化工作流程系统。它整合了以下功能：

1. 使用gen-week-reporter技能生成周报
2. 创建清理版HTML格式（移除不需要的元数据）
3. 发送HTML格式周报到指定邮箱
4. 完整的错误处理和日志记录

## 功能特点

- ✅ **一键自动化**：从生成周报到发送邮件的完整流程
- ✅ **智能文件发现**：自动查找最新周报文件
- ✅ **清理版HTML**：移除不需要的元数据，保留核心内容
- ✅ **专业邮件格式**：响应式设计，适配各种设备
- ✅ **完整日志记录**：所有操作都有详细日志
- ✅ **多种使用模式**：完整流程、快速发送、仅生成HTML、仅发送邮件
- ✅ **错误处理**：完善的错误检测和提示
- ✅ **测试模式**：支持测试环境检查

## 快速开始

### 方法1：完整工作流程

```bash
cd /home/developer/Desktop
python3 weekly_report_full_automation.py
```

### 方法2：使用快速启动脚本

```bash
# 完整工作流程
./weekly_report_quick_start.sh full

# 快速发送模式（已有HTML文件）
./weekly_report_quick_start.sh quick

# 仅创建HTML
./weekly_report_quick_start.sh html

# 仅发送邮件
./weekly_report_quick_start.sh send

# 显示系统状态
./weekly_report_quick_start.sh status

# 查看发送日志
./weekly_report_quick_start.sh logs

# 测试模式
./weekly_report_quick_start.sh test
```

### 方法3：分步执行

```bash
# 步骤1：生成周报（使用gen-week-reporter技能）
cd /home/developer/my-repos/huawei-developer-demo
# 调用gen-week-reporter技能

# 步骤2：创建清理版HTML
cd /home/developer/Desktop
python3 create_clean_report.py

# 步骤3：发送邮件
python3 send_clean_report.py
```

## 文件结构

```text
/home/developer/Desktop/
├── 最佳实践与用户反馈周报_YYYY年MM月DD日_gen-week-reporter生成.md    # 原始Markdown周报
├── 最佳实践与用户反馈周报_YYYY年MM月DD日_gen-week-reporter生成_clean.html  # 清理版HTML
├── create_clean_report.py      # 创建清理版HTML脚本
├── send_clean_report.py        # 发送清理版周报脚本
├── weekly_report_full_automation.py # 完整自动化脚本
├── weekly_report_quick_start.sh    # 快速启动脚本
├── email_send_log.txt          # 发送日志
└── usage_guide.py             # 使用指南脚本
```

## 工作流程

### 完整工作流程

1. **检查环境**：验证git仓库、脚本文件和依赖项
2. **生成周报**：使用gen-week-reporter技能生成Markdown周报
3. **转换HTML**：创建清理版HTML格式，移除不需要的元数据
4. **发送邮件**：通过163邮箱SMTP发送HTML周报
5. **记录日志**：保存发送记录和时间戳

### 快速发送模式

1. **查找HTML文件**：自动查找最新的清理版HTML周报文件
2. **发送邮件**：直接发送已生成的HTML周报

## 移除的元数据

清理版HTML会移除以下元数据：

1. ❌ 报告生成时间
2. ❌ 数据来源
3. ❌ 监控周期
4. ❌ 报告数量
5. ❌ 最佳实践案例数量
6. ❌ 风险提示
7. ❌ 后续计划

## 邮箱配置

默认配置：

- **发件人**：zrr <${SENDER_EMAIL}>
- **收件人**：${RECEIVER_EMAIL}
- **SMTP服务器**：smtp.163.com:465 (SSL)
- **客户端授权码**：${SMTP_AUTH_CODE}

修改配置：编辑脚本文件中的相关变量。

## 故障排除

### 常见问题

1. **周报文件不存在**

   ```text
   解决方案：先使用gen-week-reporter技能生成周报
   ```

2. **HTML文件不存在**

   ```text
   解决方案：先运行create_clean_report.py生成HTML文件
   ```

3. **发送失败：认证错误**

   ```text
   解决方案：检查客户端授权码是否正确
   ```

4. **发送失败：连接超时**

   ```text
   解决方案：检查网络连接，确认SMTP服务器地址和端口
   ```

### 测试命令

```bash
# 测试SMTP连接
python3 -c "
import smtplib, ssl
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL('smtp.163.com', 465, context=context) as server:
        print('✅ SMTP服务器连接正常')
except Exception as e:
    print(f'❌ 连接失败: {e}')
"

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
0 9 * * 1 cd /home/developer/Desktop && python3 weekly_report_full_automation.py
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

## 扩展功能

### 1. 多收件人支持

修改脚本支持多个收件人

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

## 更新日志

### v1.0 (2026-04-21)

- 初始版本发布
- 完整的周报生成和邮件发送工作流程
- 自动清理元数据功能
- 专业HTML邮件格式
- 完整的错误处理和日志记录
- 支持快速发送模式
- 提供快速启动脚本
- 详细的故障排除指南

## 联系支持

如有问题或建议，请联系：

- 作者：zrr
- 邮箱：${SENDER_EMAIL}
- 更新时间：2026年04月21日