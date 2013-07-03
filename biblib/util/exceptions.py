#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

search_error_message = {
    0: "Empty request",
    40: "Stupid request",
    100: "Invalid request"
}


class search_error(Exception):
    pass
