#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from lxml import etree
from oaipmh.client import Client
from oaipmh.metadata import MetadataReader
from oaipmh.metadata import MetadataRegistry
from oaipmh.common import Metadata
from referencemanager.services import crosswalks_service


class CustomMetadataReader(MetadataReader):

    def __call__(self, element):
        map = {}
        # create XPathEvaluator for this element
        xpath_evaluator = etree.XPathEvaluator(element, namespaces=self._namespaces)

        e = xpath_evaluator.evaluate
        # now extra field info according to xpath expr
        for field_name, (field_type, expr) in self._fields.items():
            if field_type == 'bytes':
                value = str(e(expr))
            elif field_type == 'bytesList':
                value = [str(item) for item in e(expr)]
            elif field_type == 'text':
                # make sure we get back unicode strings instead
                # of lxml.etree._ElementUnicodeResult objects.
                value = unicode(e(expr))
            elif field_type == 'textList':
                # make sure we get back unicode strings instead
                # of lxml.etree._ElementUnicodeResult objects.
                value = [unicode(v) for v in e(expr)]
            elif field_type == 'firstText':
                value = e(expr)
                if isinstance(value, list):
                    if len(value) > 0:
                        value = unicode(value[0])
                    else:
                        value = None
                else:
                    value = unicode(value)
            elif field_type == 'lxmlelement':
                if expr is not None:
                    value = e(expr)
                    if isinstance(value, list):
                        if len(value) > 0:
                            value = value[0]
                        else:
                            value = None
                else:
                    value = element
            elif field_type == 'xmlstring':
                value = e(expr)
                if isinstance(value, list):
                    if len(value) > 0:
                        value = etree.tostring(value[0], encoding="UTF-8")
                    else:
                        value = None
                else:
                    value = etree.tostring(value, encoding="UTF-8")
            elif isinstance(field_type, MetadataReader):
                value = e(expr)
                if isinstance(value, list):
                    value = [field_type(v) for v in value]
                else:
                    value = field_type(value)
            else:
                raise "Unknown field type: %s" % field_type
            map[field_name] = value
        return Metadata(map)

custom_namespaces = {
    'oai-pmh': 'http://www.openarchives.org/OAI/2.0/',
    'didl': 'urn:mpeg:mpeg21:2002:02-DIDL-NS',
    'dii': 'urn:mpeg:mpeg21:2002:01-DII-NS',
    'dip': 'urn:mpeg:mpeg21:2005:01-DIP-NS',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'mods': 'http://www.loc.gov/mods/v3',
    'marc': 'http://www.loc.gov/MARC21/slim',
    'dai': 'info:eu-repo/dai http://www.surfgroepen.nl/sites/oai/metadata/Shared%20Documents/dai-extension.xsd',
    'xlink': 'http://www.w3.org/1999/xlink'
}

oai_dc_reader = CustomMetadataReader(
    fields={'orig': ('xmlstring', 'oai_dc:dc')},
    namespaces=custom_namespaces
)

mods_reader = CustomMetadataReader(
    fields={'orig': ('xmlstring', 'mods:mods')},
    namespaces=custom_namespaces
)

didl_reader = CustomMetadataReader(
    fields={'orig': ('xmlstring', 'didl:DIDL')},
    namespaces=custom_namespaces
)

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
registry.registerReader('mods', mods_reader)
registry.registerReader('didl', didl_reader)


def convert_identifiy(identify):
    if identify is not None:
        result = {}
        result['repositoryName'] = identify.repositoryName()
        result['baseURL'] = identify.baseURL()
        result['protocolVersion'] = identify.protocolVersion()
        result['earliestDatestamp'] = identify.earliestDatestamp().isoformat()
        result['deletedRecord'] = identify.deletedRecord()
        result['granularity'] = identify.granularity()
        result['adminEmails'] = identify.adminEmails()
        result['compression'] = identify.compression()
        result['description'] = identify.descriptions()
        return result


def convert_metadata_formats(metadata_formats):
    if metadata_formats:
        result = {}
        result['metadataPrefix'] = metadata_formats[0]
        result['schema'] = metadata_formats[1]
        result['metadataNamespace'] = metadata_formats[2]
        return result


def convert_setspec(setspec):
    if setspec:
        result = {}
        result['setSpec'] = setspec[0].encode('utf-8')
        result['setName'] = setspec[1].encode('utf-8')
        #result['setDescription'] = setspec[2].encode('utf-8')
        return result


def convert_header(header):
    if header is not None:
        result = {}
        result['identifier'] = header.identifier()
        result['datestamp'] = header.datestamp().isoformat()
        result['setspecs'] = header.setSpec()
        result['deleted'] = header.isDeleted()
    return result


def convert_record(record, metadata_prefix_orig, source):
    result = {}
    result.update(convert_header(record[0]))
    result['meta_orig_prefix'] = metadata_prefix_orig
    meta_orig_value = record[1].getField("orig")
    result['meta_orig_value'] = meta_orig_value.encode('utf-8')
    metajson_list = crosswalks_service.convert_document(result['meta_orig_value'], result['meta_orig_prefix'], 'metajson', source)
    if metajson_list:
        result['metajson'] = metajson_list[0]
    return result


def identifiy(target):
    if target is not None:
        client = Client(target['url'], registry)
        identify = client.identify()
        return convert_identifiy(identify)


def list_identifiers(target, date_from, date_until, setspec):
    if target is not None:
        client = Client(target['url'], registry)
        headers = client.listIdentifiers(metadataPrefix=target['metadata_prefix'], from_=date_from, until=date_until, set=setspec)
        results = []
        if headers is not None:
            for header in headers:
                results.append(convert_header(header))
        return results


def list_metadata_formats(target, identifier):
    if target is not None:
        client = Client(target['url'], registry)
        metadata_formats = client.listMetadataFormats(identifier=identifier)
        results = []
        if metadata_formats is not None:
            for metadata_format in metadata_formats:
                results.append(convert_metadata_formats(metadata_format))
        return results


def list_sets(target):
    if target is not None:
        client = Client(target['url'], registry)
        setspecs = client.listSets()
        results = []
        if setspecs is not None:
            for setspec in setspecs:
                results.append(convert_setspec(setspec))
        return results


def get_record(target, identifier):
    if target is not None:
        client = Client(target['url'], registry)
        record = client.getRecord(identifier=identifier, metadataPrefix=target['metadata_prefix'])
        return convert_record(record, target['metadata_prefix'], target['title'])


def list_records(target, date_from, date_until, setspec):
    if target is not None:
        client = Client(target['url'], registry)
        # todo : clean this, find simplified cases
        if date_from is not None and date_until is not None and setspec is not None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], from_=date_from, until=date_until, set=setspec)
        elif date_from is not None and date_until is not None and setspec is None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], from_=date_from, until=date_until)
        elif date_from is not None and date_until is None and setspec is not None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], from_=date_from, set=setspec)
        elif date_from is None and date_until is not None and setspec is not None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], until=date_until, set=setspec)
        elif date_from is not None and date_until is None and setspec is None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], from_=date_from)
        elif date_from is None and date_until is not None and setspec is None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], until=date_until)
        elif date_from is None and date_until is None and setspec is not None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'], set=setspec)
        elif date_from is None and date_until is None and setspec is None:
            records = client.listRecords(metadataPrefix=target['metadata_prefix'])

        results = []
        if records is not None:
            results = []
            for record in records:
                results.append(convert_record(record, target['metadata_prefix'], target['title']))
        return results
