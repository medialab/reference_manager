#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8


def csv_dict_reader_to_metasjon_list(csv_dict_reader, input_format, source, only_first_record):
    for csv_row in csv_dict_reader:
        # todo input_format case
        yield csv_dict_reader_to_metasjon(csv_row, source)


def csv_dict_reader_to_metasjon(csv_row, source):
    # todo
    return None
