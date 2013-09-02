#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import re

re_html_tags = re.compile(r'<.*?>')


def strip_html_tags(html):
    if html:
        return re_html_tags.sub('', html)
