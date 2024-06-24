#!/bin/bash

# 检查是否传递了提交信息参数
if [ -z "$1" ]; then
  echo "Error: Commit message is required."
  echo "Usage: $0 <commit-message>"
  exit 1
fi

# 获取提交信息参数
COMMIT_MESSAGE=$1

# 暂存所有文件
git add *

# 提交更改
git commit -m "$COMMIT_MESSAGE"

# 推送到远程仓库
git push origin main

# 打印推送时间
echo "Push completed at: $(date)"
