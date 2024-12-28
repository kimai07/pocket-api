#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class MyPocket:
    """
    "list"
    "item_id"
    "resolved_title"
    "given_url"
    """

    def __init__(self, p):
        self.__p = p

    def search_request(self, search_word: str):
        """ """
        res = self.__p.get(
            offset=0,
            count=500,
            search=search_word,
            sort="newest",
            total=1,
            since=1732978800,  # 2024-12-01 00:00:00
        )
        return res[0]["list"]

    def tag_request(
        self,
        tag_name: str,
    ):
        res = self.__p.get(
            offset=0,
            count=500,
            tag=tag_name,
            sort="newest",
            total=1,
            since=1732978800,  # 2024-12-01 00:00:00
        )
        return res[0]["list"]

    def handle_get_request(self, search_word: str, tag_name: str, deleted: bool):
        """ """
        if search_word != "":
            items = self.search_request(search_word)
        else:
            items = self.tag_request(tag_name)

        self.__handle_items_in_response(items, deleted)

    def __handle_items_in_response(self, items: dict, deleted: bool):
        """ """

        print("件数：%d件" % len(items))
        has_deleted_items = False
        cnt = 0
        for k in items:
            item = items[k]
            item_id, title, url, status = MyPocket.get_item_info(item)
            if status == "2":
                continue

            if deleted:  # 削除
                if item_id:
                    has_deleted_items = True
                    self.__p.delete(item_id)
                    print("deleted [%s](%s)" % (title, url))
                    cnt += 1
            else:
                if title or url:
                    print("* [%s](%s)" % (title, url))
                    cnt += 1

        print("有効件数：%d件" % cnt)

        if deleted and has_deleted_items:  # 削除コミット
            self.__p.commit()

    @staticmethod
    def get_item_info(item):
        """ """

        item_id = item["item_id"]
        status = "2"
        title = ""
        url = ""
        if "status" in item:
            status = item["status"]
        if "resolved_title" in item:
            title = item["resolved_title"]
        if "given_url" in item:
            url = item["given_url"]

        if re.match(r"^https://qiita.com/.*\?utm_campaign=popular_items.*", url):
            # memo: ?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items
            url = re.sub(r"\?.*", "", url)

        return item_id, title, url, status
