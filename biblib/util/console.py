#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import codecs
import locale
import logging
import sys


# UTF-8 troubles...
def setup_console(sys_enc="utf-8"):
    """
    Set sys.defaultencoding to `sys_enc` and update stdout/stderr writers to corresponding encoding
    For Win32 the OEM console encoding will be used istead of `sys_enc`
    """
    reload(sys)
    try:
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        #locale.setlocale(locale.LC_ALL, '')

        if sys.platform.startswith("win"):
            import ctypes
            enc = "cp%d" % ctypes.windll.kernel32.GetOEMCP()
            #TODO: win64/python64 implementation
        else:
            enc = (sys.stdout.encoding if sys.stdout.isatty() else
                   sys.stderr.encoding if sys.stderr.isatty() else
                   sys.getfilesystemencoding() or sys_enc)

        sys.setdefaultencoding(sys_enc)

        # redefine stdout/stderr in console
        if sys.stdout.isatty() and sys.stdout.encoding != enc:
            sys.stdout = codecs.getwriter(enc)(sys.stdout, 'replace')

        if sys.stderr.isatty() and sys.stderr.encoding != enc:
            sys.stderr = codecs.getwriter(enc)(sys.stderr, 'replace')

    except:
        pass

    logging.debug("setup_console")
    logging.debug("sys.getdefaultencoding() = {0}".format(sys.getdefaultencoding()))
    logging.debug("locale.getdefaultlocale() = {0}".format(locale.getdefaultlocale()))
    logging.debug("locale.getlocale() = {0}".format(locale.getlocale()))
