#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8


def chrono_trace(name, before_date, after_date, count):
    time = after_date - before_date
    microseconds = time.days * 3600 * 24 * 1000000 + time.seconds * 1000000 + time.microseconds
    print "# {}: {} milliseconds ({} days, {} seconds, {} microseconds)".format(name, str(microseconds / 1000), str(time.days), str(time.seconds), str(time.microseconds))
    if count:
        print "# {}: for {} items : {} microseconds per item".format(name, count, str(microseconds / count))
