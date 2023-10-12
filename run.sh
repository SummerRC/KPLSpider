#!/bin/bash

# kill any existing scrapyd process if any
kill -9 $(pidof scrapyd)

# 同时执行，无需等待前一个执行结束就可以继续输入下一个命令
scrapyd & scrapydweb & logparser -dir ./logs

# just keep this script running
while [[ true ]]; do
    sleep 1
done