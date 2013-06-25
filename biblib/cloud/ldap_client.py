#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import ldap
from biblib.service import config_service

config = config_service.config["ldap"]


def ldap_search(ldap_base_dn, ldap_filter, ldap_attrs):
    ldap_con = ldap.initialize(config["host"], config["port"])
    ldap_con.simple_bind_s(config["dn"], config["password"])
    ldap_results = ldap_con.search_s(ldap_base_dn, ldap.SCOPE_SUBTREE, ldap_filter, ldap_attrs)
    results = []
    for dn, entry in ldap_results:
        results.append(entry)
    print results
    return results


def ldap_search_user_by_identifier(identifier):
    ldap_base_dn = 'ou=Users,o=sciences-po, c=fr'
    ldap_filter = "(|(scpoLibraryNumber=*{0})(scpoBannerID=*{0})(scpoTeacherNumber=*{0})(scpoStudentNumber=*{0})(uid=*{0}))".format(identifier)
    ldap_attrs = ['uid', 'employeeType', 'scpoLibraryNumber', 'scpoBannerID', 'scpoTeacherNumber', 'scpoStudentNumber']
    ldap_search(ldap_base_dn, ldap_filter, ldap_attrs)


#ldap_search_user_by_identifier("11001829")
