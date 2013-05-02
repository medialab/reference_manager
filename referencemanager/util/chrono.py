#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import sys
import codecs
import locale


def chrono_trace(name, before_date, after_date, count):
    time = after_date - before_date
    print "# {}: total: {} milliseconds: {} microseconds".format(name, str(time.microseconds / 1000), str(time.microseconds))
    if count:
        print "# {}: per reference: {} microseconds".format(name, str(time.microseconds / count))
