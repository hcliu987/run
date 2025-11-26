# 定时执行Python脚本示例

这个仓库演示了如何使用 GitHub Actions 定期执行 Python 脚本。

## 工作原理

1. 使用 GitHub Actions 的 `schedule` 事件触发工作流
2. 在 Ubuntu 虚拟环境中设置 Python 环境
3. 执行 Python 脚本
4. 将执行结果提交并推送到仓库

## 定时配置

默认配置为每天 UTC 时间 0 点、10 点和 16 点执行（即北京时间早上 8 点、下午 18 点和凌晨 0 点）。

您可以根据需要修改 [.github/workflows/scheduled-python-script.yml](.github/workflows/scheduled-python-script.yml) 中的 cron 表达式：

```yaml
schedule:
  # 每天UTC时间0点执行（即北京时间早上8点）
  - cron: '0 0 * * *'
  # 每天UTC时间10点执行（即北京时间18点）
  - cron: '0 10 * * *'
  # 每天UTC时间16点执行（即北京时间凌晨0点）
  - cron: '0 16 * * *'
```

## 双色球开奖通知

还有一个专门用于双色球开奖通知的脚本 [lottery_notifier.py](lottery_notifier.py)，它会在开奖后自动检查您的号码是否中奖并通过 Bark 发送通知。

该脚本配置为每周二、四、日晚上执行（北京时间），因为这是双色球的常规开奖时间。

## 依赖管理

项目使用 [requirements.txt](requirements.txt) 文件来管理 Python 依赖。GitHub Actions 工作流会自动安装这些依赖。

要添加新的依赖，请在 [requirements.txt](requirements.txt) 文件中添加相应的包名和版本号。

## Cron 表达式参考

Cron 表达式格式为：`分钟 小时 日 月 星期`

常用示例：
- `0 0 * * *` - 每天 UTC 0点执行（北京时间 8点）
- `0 10 * * *` - 每天 UTC 10点执行（北京时间 18点）
- `0 16 * * *` - 每天 UTC 16点执行（北京时间 次日凌晨 0点）
- `15 14 * * 1,3,6` - 每周二、四、日晚上10:15执行（UTC时间）
- `0 8 * * *` - 每天 UTC 8点执行（北京时间 16点）
- `0 0 * * 0` - 每周日 UTC 0点执行
- `0 0 1 * *` - 每月第一天 UTC 0点执行
- `*/30 * * * *` - 每 30 分钟执行一次

## 手动触发

除了自动定时执行外，还可以通过 GitHub 界面手动触发工作流：

1. 进入仓库的 "Actions" 标签页
2. 选择相应的工作流
3. 点击 "Run workflow" 按钮

## 推送到 GitHub

要将此代码推送到您自己的 GitHub 仓库，请按照以下步骤操作：

1. 在 GitHub 上创建一个新的仓库（不要初始化 README、.gitignore 或许可证）
2. 复制您的仓库 URL（格式为：`https://github.com/yourusername/your-repo-name.git`）
3. 编辑 [push_to_github.sh](push_to_github.sh) 文件，将 `GITHUB_REPO_URL` 变量替换为您的仓库 URL
4. 运行推送脚本：
   ```bash
   ./push_to_github.sh
   ```

或者，您也可以手动执行以下命令：
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

## 自定义脚本

要使用自己的 Python 脚本，请替换相应的 Python 文件内容，并根据需要修改工作流中的依赖安装部分。