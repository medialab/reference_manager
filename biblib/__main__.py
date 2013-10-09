#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import argparse

from biblib.services import config_service
from biblib.services import corpus_service
from biblib.services import crosswalks_service
from biblib.services import export_service
from biblib.services import import_service
from biblib.util import console
from biblib.util import constants

# usage:
# python biblib clean -c aime
# python biblib conf -c aime
# python biblib import -c aime -f endnotexml -i data/endnotexml/endnote-aime.xml
# python biblib export -c aime -f metajson -o data/result/result_aime_metajson.json
# python biblib convert -f endnotexml -i data/endnotexml/endnote-aime.xml -r metajson -o data/result/result_aime_metajson.json

console.setup_console()
default_corpus = config_service.config["default_corpus"]

# Supported input and output formats
INPUT_FORMATS = [constants.FORMAT_BIBTEX, constants.FORMAT_DIDL, constants.FORMAT_ENDNOTEXML, constants.FORMAT_METAJSON, constants.FORMAT_MODS, constants.FORMAT_RESEARCHERML, constants.FORMAT_RIS, constants.FORMAT_SUMMONJSON, constants.FORMAT_UNIXREF]
OUTPUT_FORMATS = [constants.FORMAT_HTML, constants.FORMAT_METAJSON, constants.FORMAT_REPEC]


def clean_corpus(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    print "corpus: {}".format(corpus)
    corpus_service.clean_corpus(corpus)


def conf_corpus(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    print "corpus: {}".format(corpus)
    corpus_service.conf_corpus(corpus)


def import_metadatas(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    print "corpus: {}".format(corpus)
    input_format = args.input_format
    print "input_format: {}".format(input_format)
    input_file_path = args.input_file_path
    print "input_file_path: {}".format(input_file_path)
    error_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "data", "result", "result_import_errors.txt")
    print "error_file_path: {}".format(error_file_path)
    with open(error_file_path, "w") as error_file:
        import_service.import_metadata_file(corpus, input_file_path, input_format, error_file, "EndNote XML File", True, None)


def export_metadatas(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    print "corpus: {}".format(corpus)
    output_format = args.output_format
    print "output_format: {}".format(output_format)
    output_file_path = args.output_file_path
    print "output_file_path: {}".format(output_file_path)
    # error_file
    error_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "data", "result", "result_export_errors.txt")
    print "error_file_path: {}".format(error_file_path)
    with open(error_file_path, "w") as error_file:
        export_service.export_corpus(corpus, output_file_path, output_format, error_file)


def convert_metadatas(args):
    input_format = args.input_format
    print "input_format: {}".format(input_format)
    input_file_path = args.input_file_path
    print "input_file_path: {}".format(input_file_path)
    output_format = args.output_format
    print "output_format: {}".format(output_format)
    output_file_path = args.output_file_path
    print "output_file_path: {}".format(output_file_path)
    # error_file
    error_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "data", "result", "result_export_errors.txt")
    print "error_file_path: {}".format(error_file_path)
    # convert
    results = crosswalks_service.convert_file(input_file_path, input_format, output_format, None, False)
    # export
    with open(error_file_path, "w") as error_file:
        export_service.export(None, None, results, output_file_path, output_format, error_file)


# Doc :
# http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/argparse/index.html

# parser
parser = argparse.ArgumentParser(description='Metadata management tool',
                                 epilog="That's how you should be using biblib")
parser.add_argument('--version',
                    action='version',
                    version='%(prog)s ' + constants.VERSION)

subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='Choose one of theses functions')

# clean
clean_parser = subparsers.add_parser('clean',
                                     help="Be careful! Create the mongodb database of the specified corpus if not already existing, erase all data and create the indexes inside this corpus database.")
clean_parser.set_defaults(func=clean_corpus)
clean_parser.add_argument('-c',
                          dest='corpus',
                          help='corpus identifier like : aime, forccast...')

# conf
conf_parser = subparsers.add_parser('conf',
                                    help='Insert or update in the corpus the types and user interface fields located in the "conf" folder')
conf_parser.set_defaults(func=conf_corpus)
conf_parser.add_argument('-c',
                         dest='corpus',
                         help='corpus identifier like : aime, forccast...')

# import
import_parser = subparsers.add_parser('import',
                                      help='Import a metadata file')
import_parser.set_defaults(func=import_metadatas)
import_parser.add_argument('-c',
                           dest='corpus',
                           help='corpus identifier like : aime, forccast...')
import_parser.add_argument('-f',
                           dest='input_format',
                           choices=INPUT_FORMATS,
                           help='input file format')
import_parser.add_argument('-i',
                           dest='input_file_path',
                           #type=argparse.FileType('r'),
                           help='input file path')

# export
export_parser = subparsers.add_parser('export',
                                      help='Export as a metadata file')
export_parser.set_defaults(func=export_metadatas)
export_parser.add_argument('-c',
                           dest='corpus',
                           help='corpus identifier like : aime, forccast...')
export_parser.add_argument('-f',
                           dest='output_format',
                           choices=OUTPUT_FORMATS,
                           help='output file format')
export_parser.add_argument('-o',
                           dest='output_file_path',
                           #type=argparse.FileType('r'),
                           help='output file path')

# convert
convert_parser = subparsers.add_parser('convert',
                                       help='Convert a metadata file to another format')
convert_parser.set_defaults(func=convert_metadatas)
convert_parser.add_argument('-f',
                            dest='input_format',
                            choices=INPUT_FORMATS,
                            help='input file format')
convert_parser.add_argument('-i',
                            dest='input_file_path',
                            #type=argparse.FileType('r'),
                            help='input file path')
convert_parser.add_argument('-r',
                            dest='output_format',
                            choices=OUTPUT_FORMATS,
                            help='output file format')
convert_parser.add_argument('-o',
                            dest='output_file_path',
                            #type=argparse.FileType('r'),
                            help='output file path')

args = parser.parse_args()
args.func(args)
