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

        for k in items:
            item = items[k]
            item_id, title, url = MyPocket.get_item_info(item)
            if deleted:  # 削除
                self.__p.delete(item_id)
                print("deleted [%s](%s)" % (title, url))
            else:
                print("* [%s](%s)" % (title, url))

        if deleted:  # 削除コミット
            self.__p.commit()

    @staticmethod
    def get_item_info(item):
        """ """

        item_id = item["item_id"]
        title = ""
        if "resolved_title" in item:
            title = item["resolved_title"]
        url = item["given_url"]
        if re.match(r"^https://qiita.com/.*\?utm_campaign=popular_items.*", url):
            # memo: ?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items
            url = re.sub(r"\?.*", "", url)

        return item_id, title, url
