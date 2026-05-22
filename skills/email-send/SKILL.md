---
name: email-send
description: "Send email via SMTP using msmtp without a full mail client."
tags: [email, smtp, msmtp]
version: 1.0.0
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["msmtp"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "msmtp",
              "bins": ["msmtp"],
              "label": "Install msmtp (dnf)",
            },
          ],
      },
  }
---

# Email Send Skill

## 概述

通过 SMTP 快速发送邮件，无需打开完整的邮件客户端。
依赖 `msmtp` 命令行工具。

需要以下环境变量：

- `SMTP_HOST` -- SMTP 服务器地址
- `SMTP_PORT` -- SMTP 服务器端口
- `SMTP_USER` -- SMTP 登录用户名
- `SMTP_PASS` -- SMTP 登录密码

## 前置条件

- 已安装 `msmtp` 工具
- 已配置 `~/.msmtprc` 或环境变量中的 SMTP 凭据
- 网络可访问 SMTP 服务器

安装方式：

```bash
sudo dnf install msmtp
```

## 核心命令

### 发送基本邮件

```bash
echo "Meeting at 3pm tomorrow." \
  | msmtp recipient@example.com
```

### 发送带主题的邮件

```bash
printf "To: recipient@example.com\n" \
  "Subject: Quick update\n\n" \
  "Hey, the deploy is done." \
  | msmtp recipient@example.com
```

### 常用选项

- `--cc` -- 抄送收件人
- `--bcc` -- 密送收件人
- `--attach <file>` -- 附加文件

## 参数确认

| 参数 | 说明 | 示例 |
|------|------|------|
| 收件人 | 邮件接收地址 | `recipient@example.com` |
| `SMTP_HOST` | SMTP 服务器地址 | `smtp.example.com` |
| `SMTP_PORT` | SMTP 服务器端口 | `587` |
| `SMTP_USER` | 登录用户名 | `user@example.com` |
| `SMTP_PASS` | 登录密码 | `********` |

## 参考文档

- [msmtp 官方文档](https://marlam.de/msmtp/)
- [msmtp 手册页](https://man.archlinux.org/man/msmtp.1)
