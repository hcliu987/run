#!/bin/bash

# 推送代码到 GitHub 的脚本

# 请将下面的 URL 替换为您自己的 GitHub 仓库 URL
GITHUB_REPO_URL="https://github.com/yourusername/your-repo-name.git"

echo "设置远程仓库..."
git remote add origin $GITHUB_REPO_URL

echo "设置主分支..."
git branch -M main

echo "推送代码到 GitHub..."
git push -u origin main

echo "推送完成！"