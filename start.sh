#!/bin/bash

# PYTHONPATH 설정
export PYTHONPATH=$PYTHONPATH:$(pwd)

# --now 옵션 확인
if [ "$1" = "--now" ]; then
    # 즉시 작업 실행
    python src/collect_news.py
    python src/generate_report.py
    python src/send_report.py
else
    # 스케줄러 실행
    python src/scheduler.py
fi 