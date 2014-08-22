#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import argparse
import logging
import os

from biblib.services import config_service
from biblib.services import corpus_service
from biblib.services import crosswalks_service
from biblib.services import io_service
from biblib.util import console
from biblib.util import constants

# usage:
# python biblib clean -c aime
# python biblib conf -c aime -d aime
# python biblib import -c aime -f endnotexml -i data/endnotexml/endnote-aime.xml
# python biblib export -c aime -f metajson -o data/result/result_aime_metajson.json
# python biblib convert -f endnotexml -i data/endnotexml/endnote-aime.xml -r metajson -o data/result/result_aime_metajson.json
# python biblib harvest 

console.setup_console()
default_corpus = config_service.config["default_corpus"]

# Supported input and output formats
INPUT_FORMATS = [constants.FORMAT_BIBTEX, constants.FORMAT_CSV_METAJSON, constants.FORMAT_DIDL, constants.FORMAT_ENDNOTEXML, constants.FORMAT_METAJSON, constants.FORMAT_MODS, constants.FORMAT_RESEARCHERML, constants.FORMAT_RIS, constants.FORMAT_SUMMONJSON, constants.FORMAT_UNIMARC, constants.FORMAT_UNIXREF]
OUTPUT_FORMATS = [constants.FORMAT_METAJSON, constants.FORMAT_MODS, constants.FORMAT_REPEC]
OUTPUT_STYLES = [constants.STYLE_MLA]


def clean_corpus(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    logging.info("corpus: {}".format(corpus))
    corpus_service.clean_corpus(corpus)


def conf_corpus(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    logging.info("corpus: {}".format(corpus))
    corpus_conf_dir_name = args.corpus_conf_dir_name
    logging.info("corpus_conf_dir_name: {}".format(corpus_conf_dir_name))
    corpus_service.conf_corpus(corpus, corpus_conf_dir_name)


def import_metadatas(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    logging.info("corpus: {}".format(corpus))
    input_format = args.input_format
    logging.info("input_format: {}".format(input_format))
    input_file_path = args.input_file_path
    logging.info("input_file_path: {}".format(input_file_path))
    source = args.source
    logging.info("source: {}".format(source))
    rec_id_prefix = args.rec_id_prefix
    logging.info("rec_id_prefix: {}".format(rec_id_prefix))
    corpus_service.import_metadata_file(corpus, input_file_path, input_format, source, rec_id_prefix, True, None)


def validate_corpus(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    logging.info("corpus: {}".format(corpus))
    error_file_name = "".join(["validation-", corpus, ".txt"])
    error_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "log", error_file_name)
    logging.info("error_file_path: {}".format(error_file_path))
    corpus_service.validate_corpus(corpus, error_file_path)


def export_metadatas(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    logging.info("corpus: {}".format(corpus))
    output_format = args.output_format
    logging.info("output_format: {}".format(output_format))
    output_file_path = args.output_file_path
    logging.info("output_file_path: {}".format(output_file_path))
    all_in_one_file = True
    corpus_service.export_corpus(corpus, output_file_path, output_format, all_in_one_file)


def format_metadatas(args):
    corpus = args.corpus
    if not corpus:
        corpus = default_corpus
    logging.info("corpus: {}".format(corpus))
    output_style = args.output_style
    logging.info("output_style: {}".format(output_style))
    output_file_path = args.output_file_path
    logging.info("output_file_path: {}".format(output_file_path))
    output_title = args.output_title
    logging.info("output_title: {}".format(output_title))
    corpus_service.format_corpus(corpus, output_title, output_file_path, output_style)


def convert_metadatas(args):
    input_format = args.input_format
    logging.info("input_format: {}".format(input_format))
    input_file_path = args.input_file_path
    logging.info("input_file_path: {}".format(input_file_path))
    output_format = args.output_format
    logging.info("output_format: {}".format(output_format))
    output_file_path = args.output_file_path
    logging.info("output_file_path: {}".format(output_file_path))
    # error_file
    all_in_one_file = True
    # convert
    results = crosswalks_service.parse_and_convert_file(input_file_path, input_format, output_format, None, "", False, all_in_one_file)
    # export
    io_service.write_items_in_one_file(None, None, results, output_file_path, output_format)


# Doc :
# http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/argparse/index.html

# parser
parser = argparse.ArgumentParser(description='Metadata management tool',
                                 epilog="That's how you should be using biblib")
parser.add_argument('--version',
                    action='version',
                    version='%(prog)s ' + constants.BIBLIB_VERSION)

subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='Choose one of theses functions')

# clean
clean_parser = subparsers.add_parser('clean',
                                     help="Be careful! Create the mongodb database of the specified corpus if not already existing, erase all data and create the indexes inside this corpus database.")
clean_parser.set_defaults(func=clean_corpus)
clean_parser.add_argument('-c',
                          '--corpus',
                          dest='corpus',
                          help='corpus identifier like : aime, forccast...')

# conf
conf_parser = subparsers.add_parser('conf',
                                    help='Insert or update in the corpus the types and user interface fields located in the "conf" folder')
conf_parser.set_defaults(func=conf_corpus)
conf_parser.add_argument('-c',
                         '--corpus',
                         dest='corpus',
                         help='corpus identifier like : aime, forccast...')
conf_parser.add_argument('-d',
                         '--corpus_conf_dir_name',
                         dest='corpus_conf_dir_name',
                         help='corpus directory name inside the conf/corpus : aime, forccast...')

# import
import_parser = subparsers.add_parser('import',
                                      help='Import a metadata file')
import_parser.set_defaults(func=import_metadatas)
import_parser.add_argument('-c',
                           '--corpus',
                           dest='corpus',
                           help='corpus identifier like : aime, forccast...')
import_parser.add_argument('-f',
                           '--input_format',
                           dest='input_format',
                           choices=INPUT_FORMATS,
                           help='input file format')
import_parser.add_argument('-i',
                           '--input_file_path',
                           dest='input_file_path',
                           #type=argparse.FileType('r'),
                           help='input file path')

import_parser.add_argument('-s',
                           '--source',
                           dest='source',
                           help='Source name')

import_parser.add_argument('-p',
                           '--rec_id_prefix',
                           dest='rec_id_prefix',
                           help='Record Identifier Prefix')

# export
export_parser = subparsers.add_parser('export',
                                      help='Export as a metadata file')
export_parser.set_defaults(func=export_metadatas)
export_parser.add_argument('-c',
                           '--corpus',
                           dest='corpus',
                           help='corpus identifier like : aime, forccast...')
export_parser.add_argument('-f',
                           '--output_format',
                           dest='output_format',
                           choices=OUTPUT_FORMATS,
                           help='output file format')
export_parser.add_argument('-o',
                           '--output_file_path',
                           dest='output_file_path',
                           #type=argparse.FileType('r'),
                           help='output file path')

# format
format_parser = subparsers.add_parser('format',
                                      help='Format in an HTML file')
format_parser.set_defaults(func=format_metadatas)
format_parser.add_argument('-c',
                           '--corpus',
                           dest='corpus',
                           help='corpus identifier like : aime, forccast...')
format_parser.add_argument('-t',
                           '--output_title',
                           dest='output_title',
                           help='output title')
format_parser.add_argument('-s',
                           '--output_style',
                           dest='output_style',
                           choices=OUTPUT_STYLES,
                           help='output style')
format_parser.add_argument('-o',
                           '--output_file_path',
                           dest='output_file_path',
                           #type=argparse.FileType('r'),
                           help='output file path')

# convert
convert_parser = subparsers.add_parser('convert',
                                       help='Convert a metadata file to another format')
convert_parser.set_defaults(func=convert_metadatas)
convert_parser.add_argument('-f',
                            '--input_format',
                            dest='input_format',
                            choices=INPUT_FORMATS,
                            help='input file format')
convert_parser.add_argument('-i',
                            '--input_file_path',
                            dest='input_file_path',
                            #type=argparse.FileType('r'),
                            help='input file path')
convert_parser.add_argument('-r',
                            '--output_format',
                            dest='output_format',
                            choices=OUTPUT_FORMATS,
                            help='output file format')
convert_parser.add_argument('-o',
                            '--output_file_path',
                            dest='output_file_path',
                            #type=argparse.FileType('r'),
                            help='output file path')

# validate
validate_parser = subparsers.add_parser('validate',
                                     help="Validate the corpus metadata.")
validate_parser.set_defaults(func=validate_corpus)
validate_parser.add_argument('-c',
                          '--corpus',
                          dest='corpus',
                          help='corpus identifier like : aime, forccast...')

args = parser.parse_args()
args.func(args)
