#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import csv
import ldap
import logging
import os

from biblib.services import config_service

config = config_service.config["ldap"]

def ldap_search(ldap_base_dn, ldap_filter, ldap_attrs):
    ldap_con = ldap.initialize(config["host"], config["port"])
    ldap_con.simple_bind_s(config["dn"], config["password"])
    ldap_results = ldap_con.search_s(ldap_base_dn, ldap.SCOPE_SUBTREE, ldap_filter, ldap_attrs)
    results = []
    for dn, entry in ldap_results:
        results.append(entry)
    #logging.debug(results)
    return results


def ldap_search_user_by_identifier(identifier):
    ldap_base_dn = 'ou=Users,o=sciences-po, c=fr'
    ldap_filter = "(|(scpoLibraryNumber=*{0})(scpoBannerID=*{0})(scpoTeacherNumber=*{0})(scpoStudentNumber=*{0})(uid=*{0}))".format(identifier)
    ldap_attrs = ['uid', 'employeeType', 'scpoLibraryNumber', 'scpoBannerID', 'scpoTeacherNumber', 'scpoStudentNumber']
    ldap_search(ldap_base_dn, ldap_filter, ldap_attrs)


def ldap_search_user_by_employeetype(employeetype):
    ldap_base_dn = 'ou=Users,o=sciences-po, c=fr'
    ldap_filter = "(employeeType=*{0})".format(employeetype)
    ldap_attrs = ['uid', 'givenName', 'sn', 'employeeType', 'scpoActifSI', 'scpoLibraryNumber', 'scpoBannerID', 'scpoTeacherNumber', 'scpoStudentNumber', 'scpoDateEntree', 'scpoDateSortie', 'mailForwardingAddress', 'scpoBannerStatus', 'scpoSynchroBanner', 'scpoGestionnairePrincipal', 'scpoEmployeeDSP']
    results = ldap_search(ldap_base_dn, ldap_filter, ldap_attrs)
    csv_file_name = "".join(["ldap-", employeetype, ".csv"])
    csv_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data", "result", csv_file_name)
    with open(csv_file_path, "wb") as csv_file:
        fieldnames = ldap_attrs
        csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
        csvwriter.writeheader()
        for item in results:
            for key, value in item.items():
                item[key] = "; ".join(sorted(value))
            csvwriter.writerow(item)


def ldap_search_user_by_scporesearchcommunity():
    ldap_base_dn = 'ou=Users,o=sciences-po, c=fr'
    ldap_filter = "(scpoResearchCommunity=1)"
    ldap_attrs = ['uid', 'givenName', 'sn', 'employeeType', 'scpoActifSI', 'scpoLibraryNumber', 'scpoBannerID', 'scpoTeacherNumber', 'scpoStudentNumber', 'scpoResearchResearchCenter', 'scpoDateEntree', 'scpoDateSortie', 'mailForwardingAddress', 'scpoBannerStatus', 'scpoSynchroBanner', 'scpoGestionnairePrincipal', 'scpoEmployeeDSP']
    results = ldap_search(ldap_base_dn, ldap_filter, ldap_attrs)
    csv_file_name = "".join(["ldap-scporesearchcommunity.csv"])
    csv_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data", "result", csv_file_name)
    with open(csv_file_path, "wb") as csv_file:
        fieldnames = ldap_attrs
        csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
        csvwriter.writeheader()
        for item in results:
            for key, value in item.items():
                item[key] = "; ".join(sorted(value))
            csvwriter.writerow(item)


#ldap_search_user_by_identifier("11001829")
#ldap_search_user_by_employeetype("LECTEUR")
ldap_search_user_by_scporesearchcommunity()
