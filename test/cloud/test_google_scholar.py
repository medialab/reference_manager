#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
from biblib.cloud import google_scholar


def test():
    base_dir = os.path.join(os.getcwd(), "data")
    print "base_dir: " + base_dir

    query = "whole always smaller than parts"
    print google_scholar.query_and_retrieve_metadata(query, False)
