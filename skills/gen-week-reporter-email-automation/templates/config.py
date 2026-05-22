# 周报生成与邮件发送自动化系统配置
# 配置文件模板
import os

# ======================
# 环境变量说明
# ======================
# SENDER_EMAIL   - 发件人邮箱地址（默认: your-email@163.com）
# SENDER_NAME    - 发件人显示名称（默认: your-name）
# RECEIVER_EMAIL - 收件人邮箱地址（默认: recipient@example.com）
# SMTP_AUTH_CODE - SMTP客户端授权码（默认: 空，必须设置才能发送邮件）

# ======================
# 邮箱配置
# ======================

# 发件人邮箱配置
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "your-email@163.com")
SENDER_NAME = os.environ.get("SENDER_NAME", "your-name")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "recipient@example.com")

# 客户端授权码（需要保密，通过环境变量 SMTP_AUTH_CODE 传入）
PASSWORD = os.environ.get("SMTP_AUTH_CODE", "")

# SMTP服务器配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465  # SSL端口

# ======================
# 文件路径配置
# ======================

# 桌面目录路径
DESKTOP_PATH = "/home/developer/Desktop"

# Git仓库路径
GIT_REPO_PATH = "/home/developer/my-repos/huawei-developer-demo"

# 周报文件命名模式
REPORT_PATTERN = "周报"
CLEAN_SUFFIX = "_clean.html"

# 发送日志文件
LOG_FILE = "/home/developer/Desktop/email_send_log.txt"

# ======================
# 脚本文件配置
# ======================

# 脚本文件名称
CREATE_CLEAN_REPORT_SCRIPT = "create_clean_report.py"
SEND_CLEAN_REPORT_SCRIPT = "send_clean_report.py"
WEEKLY_REPORT_AUTOMATION_SCRIPT = "weekly_report_full_automation.py"

# ======================
# 邮件内容配置
# ======================

# 邮件主题前缀
EMAIL_SUBJECT_PREFIX = "最佳实践与用户反馈周报"

# 邮件正文配置
INCLUDE_PLAIN_TEXT = True  # 是否包含纯文本版本
INCLUDE_HTML = True        # 是否包含HTML版本

# 移除的元数据内容
REMOVED_METADATA = [
    "报告生成时间",
    "数据来源", 
    "监控周期",
    "报告数量",
    "最佳实践案例数量",
    "风险提示",
    "后续计划"
]

# ======================
# 自动化配置
# ======================

# 自动查找最新文件
AUTO_FIND_LATEST_REPORT = True

# 文件保留天数（0表示不自动删除）
FILE_RETENTION_DAYS = 7

# 发送失败重试次数
MAX_RETRY_COUNT = 3

# 重试间隔（秒）
RETRY_INTERVAL = 10

# ======================
# 日志配置
# ======================

# 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# 日志格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 是否记录详细日志
VERBOSE_LOGGING = True

# ======================
# 测试配置
# ======================

# 测试模式（不实际发送邮件）
TEST_MODE = False

# 测试收件人（测试模式下使用）
TEST_RECEIVER_EMAIL = "test@example.com"

# ======================
# 使用说明
# ======================

# 1. 复制此文件为 config.py
# 2. 修改邮箱配置（特别是密码）
# 3. 根据需要调整其他配置
# 4. 确保脚本有执行权限: chmod +x /home/developer/Desktop/*.py
# 5. 运行完整工作流程: python3 weekly_report_full_automation.py

# 注意：密码等敏感信息应妥善保管，不要提交到版本控制系统