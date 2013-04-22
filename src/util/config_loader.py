#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import json


def load_config():
    print("config_loader.load_config")
    locations = [
        os.getcwd(),
        os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
        os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir)),
        os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir)),
        os.path.expanduser("~"),
        "/etc/referencemanager",
        os.environ.get("REFMAN_CONF")
    ]
    for location in locations:
        try:
            config_location = os.path.join(location, "config.json")
            print(config_location)
            with open(config_location, 'r') as config_file:
                return json.load(config_file)
        except IOError as e:
            print 'ERROR: Could not open config.json file : ', e
            pass
        except ValueError as e:
            print 'ERROR: Config file is not valid JSON', e
            return False

config = load_config()
