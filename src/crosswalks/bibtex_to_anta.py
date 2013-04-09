#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import csv, re
from pybtex.database.input import bibtex

def get_field(entry, field) :
  if field in entry.fields and entry.fields[field] :
    tmp = unicode(entry.fields[field]).encode('utf-8')
    tmp = tmp.replace("{","").replace("}","").replace("\&","and").replace("\\","")
    return tmp
  else :
    return None

def get_authors(entry) :
  if "author" in entry.persons :
    authors_list = []
    authors = entry.persons["author"]
    for author in authors :
      tmp = unicode(author).encode('utf-8')
      tmp = tmp.replace("{","").replace("}","")
      authors_list.append(tmp)
    return ",".join(authors_list)
  else :
    return None

def convert_bibtext_to_dict(entry) :
  result = {}
  result["author"] = get_authors(entry)
  result["title"] = get_field(entry, 'title')
  result["date"] = get_field(entry, 'year')
  result["journal"] = get_field(entry, 'journal')
  result["language"] = "en"
  result["description"] = get_field(entry, 'abstract')

  my_file = get_field(entry, 'file')
  format_index=my_file.rfind(":")
  if format_index!=-1 :
    my_file=my_file[:format_index]
  slash_index=my_file.rfind("/")
  if slash_index!=-1 :
    my_file=my_file[slash_index+1:]
    my_file=my_file.replace(" ","_").replace(",","_").replace("’","_").replace("(","_").replace(")","_").replace("\&","_")

  result["file"] = my_file
  
  keyword_list = re.split(r',',get_field(entry, 'keywords').lower())

  # corpus
  corpus_list = []
  if "1" in keyword_list :
    corpus_list.append("1")
    keyword_list.remove("1")
  if "2" in keyword_list :
    corpus_list.append("2")
    keyword_list.remove("2")
  if "3" in keyword_list :
    corpus_list.append("3")
    keyword_list.remove("3")
  result["corpus"] = ",".join(corpus_list)

  # type
  my_type = ""
  if "sp" in keyword_list :
    my_type = "Scientific Papers"
    keyword_list.remove("sp")
  elif "gl" in keyword_list :
    my_type = "Grey Literature"
    keyword_list.remove("gl")
  elif "or" in keyword_list :
    my_type = "Official Reports"
    keyword_list.remove("or")
  result["type"] = my_type

  # actors
  actors_list = []
  if "dc" in keyword_list :
    actors_list.append("Developing Countries")
    keyword_list.remove("dc")
  if "ic" in keyword_list :
    actors_list.append("Industrialized Countries")
    keyword_list.remove("ic")
  if "ec" in keyword_list :
    actors_list.append("Emerging Countries")
    keyword_list.remove("ec")
  if "international organizations" in keyword_list :
    actors_list.append("International organizations")
    keyword_list.remove("international organizations")
  if "national stakeholder" in keyword_list :
    actors_list.append("National stakeholder")
    keyword_list.remove("national stakeholder")
  if "ngo (including ingo)" in keyword_list :
    actors_list.append("NGO")
    keyword_list.remove("ngo (including ingo)")
  if "private sector" in keyword_list :
    actors_list.append("Private sector")
    keyword_list.remove("private sector")
  if "scientists" in keyword_list :
    actors_list.append("Scientists")
    keyword_list.remove("scientists")
  if "media" in keyword_list :
    actors_list.append("Media")
    keyword_list.remove("media")
  # actors bonus from data
  if "decision-makers" in keyword_list :
    actors_list.append("Decision-makers")
    keyword_list.remove("decision-makers")
  if "social scientists" in keyword_list :
    actors_list.append("Social scientists")
    keyword_list.remove("social scientists")
  if "impacts scientists" in keyword_list :
    actors_list.append("Impacts scientists")
    keyword_list.remove("impacts scientists")
  if "climatologists" in keyword_list :
    actors_list.append("Climatologists")
    keyword_list.remove("climatologists")

  result["actors"] = ",".join(actors_list)

  # topics
  topics_list = []
  if "mitigation" in keyword_list :
    topics_list.append("Mitigation")
    keyword_list.remove("mitigation")
  if "vulnerability" in keyword_list :
    topics_list.append("Vulnerability")
    keyword_list.remove("vulnerability")
  if "adaptive capacity" in keyword_list :
    topics_list.append("Adaptive capacity")
    keyword_list.remove("adaptive capacity")
  if "policy" in keyword_list :
    topics_list.append("Policy")
    keyword_list.remove("policy")
  if "project" in keyword_list :
    topics_list.append("Project")
    keyword_list.remove("project")
  if "plan" in keyword_list :
    topics_list.append("Plan")
    keyword_list.remove("plan")
  # topics bonus from data
  if "efficiency" in keyword_list :
    topics_list.append("Efficiency")
    keyword_list.remove("efficiency")
  if "equity" in keyword_list :
    topics_list.append("Equity")
    keyword_list.remove("equity")
  if "glaciology" in keyword_list :
    topics_list.append("Glaciology")
    keyword_list.remove("glaciology")
  if "ice sheets" in keyword_list :
    topics_list.append("Ice sheets")
    keyword_list.remove("ice sheets")
  if "sea level" in keyword_list :
    topics_list.append("Sea level")
    keyword_list.remove("sea level")
  if "adaptation" in keyword_list :
    topics_list.append("Adaptation")
    keyword_list.remove("adaptation")
  if "climate uncertainty" in keyword_list :
    topics_list.append("Climate uncertainty")
    keyword_list.remove("climate uncertainty")
  if "maladaptation" in keyword_list :
    topics_list.append("Maladaptation")
    keyword_list.remove("maladaptation")
  if "criteria" in keyword_list :
    topics_list.append("Criteria")
    keyword_list.remove("criteria")
  if "indicator" in keyword_list :
    topics_list.append("Indicator")
    keyword_list.remove("indicator")

  result["topics"] = ",".join(topics_list)

  # result
  if "failure" in keyword_list and "success" in keyword_list :
    result["result"]="Success and failure"
    keyword_list.remove("failure")
    keyword_list.remove("success")
  elif "failure" in keyword_list and "succes" in keyword_list :
    result["result"]="Success and failure"
    keyword_list.remove("failure")
    keyword_list.remove("succes")
  elif "failure" in keyword_list :
    result["result"]="Failure"
    keyword_list.remove("failure")
  elif "success" in keyword_list :
    result["result"]="Success"
    keyword_list.remove("success")
  elif "succes" in keyword_list :
    result["result"]="Success"
    keyword_list.remove("succes")
  else :
    result["result"]="NA"

  result["keyword"] = ",".join(keyword_list)

  return result


def convert_bibtex_file_to_antacsv(bibtex_filename) :
  with open('anta_ref.csv', 'wb') as csvfile :
    csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["corpus","file","author","title","date","language","description","type","actors","topics","result"])
    bibtexparser = bibtex.Parser()
    bib_data = bibtexparser.parse_file(bibtex_filename) 
    for key in bib_data.entries.keys() :
      result = convert_bibtext_to_dict(bib_data.entries[key])
      csvwriter.writerow([result["corpus"],result["file"],result["author"],result["title"],result["date"],result["language"],result["description"],result["type"],result["actors"],result["topics"],result["result"]])



    

convert_bibtex_file('anta_ref.bib')

  #title
  #date
  #language
  #description
  #keyword
  #type -> SP (Scientific Papers), GL: pour Grey Literature, OR: pour Official Reports


#   1. Nature of documents:
#     * SP: Scientific Papers
#     * GL: pour Grey Literature
#     * OR: pour Official Reports
# 2. Concerned actors
#     * DC (for Developing Countries)
#     * IC (for Industrialized Countries)
#     * EC (for Emerging Countries)
#     * International organizations
#     * National stakeholder
#     * NGO (including INGO)
#     * Private sector
#     * Scientists
#     * Media
# 3. Topic of the document
#     * Mitigation
#     * Vulnerability
#     * Adaptive capacity
#     * Policy
#     * Project
#     * Plan