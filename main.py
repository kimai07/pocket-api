#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
from pocket import Pocket, PocketException
import argparse
import os
import re


def get_item_info(v):
    item_id = v['item_id']
    title = ""
    if 'resolved_title' in v:
        title = v['resolved_title']
    url = v['given_url']
    if re.match('^https://qiita.com/.*\?utm_campaign=popular_items.*', url):
        # memo: ?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items
        url = re.sub('\?.*', '', url)

    return item_id, title, url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deleted', action='store_true')
    args = parser.parse_args()
    deleted = args.deleted

    p = Pocket(
     consumer_key=os.environ["POCKET_CONSUMER_KEY"],
     access_token=os.environ["POCKET_ACCESS_TOKEN"],
    )
    res = p.retrieve(
        offset=0,
        count=100,
        tag="python",
    )

    li = res['list']
    for k in li:
        v = li[k]
        item_id, title, url = get_item_info(v)
        if deleted:  # 削除
            p.delete(item_id)
            print("deleted [%s](%s)" % (title, url))
        else:
            print("- [%s](%s)" % (title, url))

    if deleted:  # 削除コミット
        p.commit()


if __name__ == '__main__':
    main()
