#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pocket import Pocket
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
    parser.add_argument('--tag', default='python')
    parser.add_argument('--deleted', action='store_true')
    args = parser.parse_args()
    tag = args.tag
    deleted = args.deleted

    if 'POCKET_CONSUMER_KEY' not in os.environ or 'POCKET_ACCESS_TOKEN' not in os.environ:
        print(
            "[ERR] no set POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN environment variables.")
        exit()

    p = Pocket(
        consumer_key=os.environ['POCKET_CONSUMER_KEY'],
        access_token=os.environ['POCKET_ACCESS_TOKEN'],
    )
    res = p.get(
        offset=0,
        count=500,
        tag=tag,
    )

    li = res[0]['list']
    for k in li:
        v = li[k]
        item_id, title, url = get_item_info(v)
        if deleted:  # 削除
            p.delete(item_id)
            print("deleted [%s](%s)" % (title, url))
        else:
            print("* [%s](%s)" % (title, url))

    if deleted:  # 削除コミット
        p.commit()


if __name__ == '__main__':
    main()
