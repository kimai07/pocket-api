#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pocket import Pocket
import argparse
import os

from app.my_pocket import MyPocket


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", default="")
    parser.add_argument("--tag", default="python")
    parser.add_argument("--deleted", action="store_true")

    args = parser.parse_args()
    search_word = args.search
    tag_name = args.tag
    deleted = args.deleted

    if (
        "POCKET_CONSUMER_KEY" not in os.environ
        or "POCKET_ACCESS_TOKEN" not in os.environ
    ):
        print(
            "[ERR] no set POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN environment variables."
        )
        exit()

    p = Pocket(
        consumer_key=os.environ["POCKET_CONSUMER_KEY"],
        access_token=os.environ["POCKET_ACCESS_TOKEN"],
    )

    my_pocket = MyPocket(p)
    my_pocket.handle_get_request(search_word, tag_name, deleted)


if __name__ == "__main__":
    main()
