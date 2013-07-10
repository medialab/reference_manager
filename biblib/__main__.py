#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
import argparse

from biblib.services import export_service
from biblib.services import import_service
from biblib.services import repository_service
from biblib.services import config_service
from biblib.services import corpus_service
from biblib.util import chrono
from biblib.util import console

# usage:
# python biblib init -c aime
# python biblib import -c aime -f endnotexml -i data/endnotexml/endnote-aime.xml

console.setup_console()
default_corpus = config_service.config["mongodb"]["default_corpus"]


def init(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    corpus_service.init_corpus(corpus)


def import_references(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    print corpus
    input_file = args.input_file
    print input_file
    input_format = args.input_format
    print input_format
    error_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "data", "result", "result_validation_errors.txt")
    with open(error_file_path, "w") as error_file:
        import_service.import_metadata_file(corpus, input_file, input_format, error_file, "EndNote XML File", True)


def convert(args):
    #todo
    print "hello convert"
    print args


def inject(args):
    #todo
    print "hello inject"
    print args


def export(args):
    #todo
    print "hello export"
    print args


def old(corpus):
    print("import_references")
    #base_dir = os.getcwd()
    base_dir = os.path.dirname(__file__)
    print "base_dir: " + base_dir
    base_dir = os.path.join(base_dir, os.pardir, "data")
    print "base_dir: " + base_dir

    #filenames = ["endnote-aime.xml", "endnote-ref.xml", "endnote-bib.xml"]
    filenames = ["endnote-aime.xml"]
    errors_file = os.path.join(base_dir, "result", "result_validation_errors.txt")
    result_mla = os.path.join(base_dir, "result", "result_mla.html")
    result_metajson = os.path.join(base_dir, "result", "result_aime_metajson.json")

    # import
    date_start = datetime.datetime.now()
    input_files = []
    for filename in filenames:
        input_file = os.path.join(base_dir, "endnotexml", filename)
        input_files.append(input_file)

    import_service.import_metadata_files(corpus, input_files, "endnotexml", errors_file, "EndNote XML File", True)

    date_import = datetime.datetime.now()
    chrono.chrono_trace("import", date_start, date_import, None)

    # fetch
    metajson_list = repository_service.get_documents(corpus)

    date_fetch = datetime.datetime.now()
    chrono.chrono_trace("fetch", date_import, date_fetch, len(metajson_list))

    # export citations
    export_service.export_html_webpage(metajson_list, result_mla)

    date_citations = datetime.datetime.now()
    chrono.chrono_trace("citations", date_fetch, date_citations, len(metajson_list))

    # export json
    export_service.export_metajson_collection("aime", "AIME references", metajson_list, result_metajson)

    date_json = datetime.datetime.now()
    chrono.chrono_trace("json", date_citations, date_json, len(metajson_list))


# old way
#corpus_service.init_corpus(default_corpus)
#old(default_corpus)

# http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/argparse/index.html

# parser
parser = argparse.ArgumentParser(description='Metadata tool',
                                 epilog="That's how you should be using biblib")
parser.add_argument('--version',
                    action='version',
                    version='%(prog)s 1.0')

subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='Choose one of theses functions')

# init
init_parser = subparsers.add_parser('init',
                                    help='Empty the store and insert the configuration properties')
init_parser.set_defaults(func=init)
init_parser.add_argument('-c',
                         dest='corpus',
                         help='corpus identifier like : aime, forccast...')

# import
import_parser = subparsers.add_parser('import',
                                      help='Import a bibliographic file')
import_parser.set_defaults(func=import_references)
import_parser.add_argument('-c',
                           dest='corpus',
                           help='corpus identifier like : aime, forccast...')
import_parser.add_argument('-f',
                           dest='input_format',
                           help='input file format')
import_parser.add_argument('-i',
                           dest='input_file',
                           #type=argparse.FileType('r'),
                           help='input file path')

# convert
convert_parser = subparsers.add_parser('convert',
                                       help='Convert a bibliographic file')
convert_parser.set_defaults(func=convert)
convert_parser.add_argument('-f',
                            dest='input_format',
                            help='input file format')
convert_parser.add_argument('-i',
                            dest='input_file',
                            #type=argparse.FileType('r'),
                            help='input file path')
convert_parser.add_argument('-r',
                            dest='output_format',
                            help='output file format')
convert_parser.add_argument('-o',
                            dest='output_file',
                            #type=argparse.FileType('r'),
                            help='output file path')

args = parser.parse_args()
args.func(args)
