#!/bin/bash

TAGS=(
    "一般"
    "_untagged_" ### 1回じゃ全部取得できない
)

for tag in ${TAGS[@]}; do
    echo $tag
    ###
    # 上限注意
    ###

    poetry run python main.py --tag=$tag >~/pocket/$tag.md

    sleep 1
done
