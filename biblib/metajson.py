#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

REC_METAJSON = 1

STYLE_GIVEN_FAMILY = "given_family"
STYLE_FAMILY_COMMA_GIVEN = "family_comma_given"

TITLE_NON_SORT = {
    "en": [
        "a",
        "about",
        "above",
        "across",
        "after",
        "again",
        "against",
        "almost",
        "along",
        "always",
        "am",
        "an",
        "and",
        "another",
        "any",
        "anybody",
        "anything",
        "anyway",
        "anywhere",
        "are",
        "around",
        "as",
        "aside",
        "at",
        "away",
        "be",
        "because",
        "been",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "between",
        "beyond",
        "both",
        "but",
        "can",
        "cannot",
        "could",
        "did",
        "do ",
        "does",
        "done",
        "down",
        "during",
        "each",
        "else",
        "elsewhere",
        "enough",
        "even",
        "ever",
        "every",
        "everything",
        "everywhere",
        "followed",
        "following",
        "for",
        "forever",
        "forward",
        "from",
        "further",
        "furthermore",
        "had",
        "has",
        "have",
        "he",
        "hence",
        "her",
        "here",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "i",
        "if",
        "in",
        "inside",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "like",
        "me",
        "mine",
        "more",
        "my",
        "myself",
        "never",
        "no",
        "nor",
        "not",
        "nothing",
        "of",
        "on",
        "or",
        "other",
        "others",
        "otherwise",
        "our",
        "ourselves",
        "out",
        "outside",
        "over",
        "overall",
        "shall",
        "she",
        "should",
        "since",
        "so",
        "some",
        "somebody",
        "somehow",
        "sometimes",
        "somewhat",
        "somewhere",
        "that",
        "the",
        "their",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "thus",
        "till",
        "to",
        "too",
        "toward",
        "towards",
        "under",
        "until",
        "upon",
        "very",
        "was",
        "we",
        "were",
        "what",
        "whatever",
        "when",
        "where",
        "whereas",
        "whereby",
        "wherein",
        "wherever",
        "whether",
        "which",
        "while",
        "who",
        "whom",
        "whose",
        "with",
        "within",
        "without",
        "would",
        "yet",
        "you",
        "your",
        "yours",
        "yourself"
    ],
    "fr": [
        "à",
        "au",
        "auprès",
        "autre",
        "autres",
        "aux",
        "avec",
        "c",
        "ce",
        "celle",
        "celles",
        "ces",
        "cet",
        "cette",
        "ceux",
        "chez",
        "d",
        "dans",
        "de",
        "derrière",
        "des",
        "devant",
        "dont",
        "du",
        "elle",
        "elles",
        "en",
        "et",
        "eux",
        "il",
        "ils",
        "je",
        "l",
        "la",
        "le",
        "les",
        "m",
        "ma",
        "me",
        "mes",
        "mon",
        "n",
        "ne",
        "ni",
        "nous",
        "on",
        "ou",
        "où",
        "par",
        "pendant",
        "pour",
        "près",
        "qu",
        "que",
        "quel",
        "quelle",
        "quelles",
        "quelqu",
        "quelque",
        "quelques",
        "quels",
        "qui",
        "s",
        "sa",
        "sans",
        "se",
        "ses",
        "suivi",
        "suivie",
        "suivies",
        "suivis",
        "sur",
        "t",
        "ta",
        "te",
        "tes",
        "tu",
        "un",
        "une",
        "uns",
        "vous",
        "y"
    ],
    "de": [
        "ab",
        "alle",
        "allem",
        "allen",
        "aller",
        "alles",
        "als",
        "am",
        "an",
        "andere",
        "anderem",
        "anderen",
        "anderer",
        "anderes",
        "auf",
        "aufs",
        "bei",
        "beim",
        "bevor",
        "bis",
        "das",
        "dass",
        "dein",
        "deine",
        "deinem",
        "deinen",
        "deiner",
        "deines",
        "dem",
        "den",
        "denen",
        "der",
        "deren",
        "derer",
        "des",
        "dessen",
        "die",
        "dies",
        "diese",
        "diesen",
        "dieser",
        "dieses",
        "durch",
        "ein",
        "eine",
        "einem",
        "einen",
        "einer",
        "eines",
        "er",
        "es",
        "euch",
        "euer",
        "eure",
        "eurem",
        "euren",
        "eurer",
        "eures",
        "für",
        "fürs",
        "gegen",
        "gemäss",
        "ihm",
        "ihn",
        "ihnen",
        "ihr",
        "ihre",
        "ihrem",
        "ihren",
        "ihrer",
        "ihres",
        "im",
        "in",
        "insbesondere",
        "irgenwelche",
        "irgenwelchem",
        "irgenwelcher",
        "irgenwelches",
        "jede",
        "jedem",
        "jeden",
        "jeder",
        "jedes",
        "jene",
        "jenem",
        "jenen",
        "jener",
        "jenes",
        "kein",
        "keine",
        "keinem",
        "keinen",
        "keiner",
        "keines",
        "manch",
        "manche",
        "manchem",
        "mancher",
        "manches",
        "mein",
        "meine",
        "meinem",
        "meinen",
        "meiner",
        "meines",
        "mit",
        "oder",
        "ohne",
        "sein",
        "seine",
        "seinem",
        "seinen",
        "seiner",
        "seines",
        "seit",
        "sie",
        "sondern",
        "sowie",
        "über",
        "überm",
        "übers",
        "um",
        "und",
        "uns",
        "unser",
        "unsere",
        "unserem",
        "unseren",
        "unserer",
        "unseres",
        "unserm",
        "unsern",
        "unsers",
        "unter",
        "verschieden",
        "verschiedene",
        "verschiedenem",
        "verschiedenen",
        "verschiedener",
        "verschiedenes",
        "vom",
        "von",
        "vor",
        "wegen",
        "welch",
        "welche",
        "welchem",
        "welchen",
        "welcher",
        "welches",
        "wem",
        "wen",
        "wenn",
        "were",
        "zu",
        "zum",
        "zur"
    ],
    "it": [
        "agli",
        "ai",
        "al",
        "all",
        "alla",
        "alle",
        "allo",
        "altra",
        "altre",
        "altri",
        "altro",
        "c",
        "che",
        "chi",
        "ci",
        "ciò",
        "cioè",
        "codesta",
        "codeste",
        "codesti",
        "codesto",
        "cogli",
        "coi",
        "col",
        "colà",
        "coll",
        "coloro",
        "come",
        "con",
        "contro",
        "cosi",
        "costà",
        "costei",
        "costi",
        "costoro",
        "costui",
        "cui",
        "d",
        "da",
        "dagli",
        "dal",
        "dall",
        "dalla",
        "dalle",
        "dallo",
        "davanti",
        "del",
        "dell",
        "della",
        "delle",
        "dello",
        "dentro",
        "di",
        "dietro",
        "dopo",
        "dove",
        "durante",
        "egli",
        "ella",
        "essa",
        "esse",
        "essi",
        "esso",
        "fra",
        "gl",
        "gli",
        "gliela",
        "gliele",
        "glielo",
        "gliene",
        "il",
        "in",
        "io",
        "l",
        "la",
        "là",
        "le",
        "lei",
        "li",
        "lo",
        "loro",
        "lui",
        "ma",
        "me",
        "menos",
        "mi",
        "mia",
        "miei",
        "mientras",
        "moi",
        "ne",
        "nè",
        "negli",
        "nei",
        "nel",
        "nell",
        "nella",
        "nelle",
        "nello",
        "no",
        "noi",
        "non",
        "nostra",
        "nostre",
        "nostri",
        "nostro",
        "ovvero",
        "percio",
        "pero",
        "piu",
        "qua",
        "qual",
        "quale",
        "quali",
        "quanta",
        "quante",
        "quanti",
        "quanto",
        "quegli",
        "quei",
        "quel",
        "quell",
        "quella",
        "quelle",
        "quelli",
        "quello",
        "quest",
        "questa",
        "queste",
        "questi",
        "questo",
        "qui",
        "se",
        "sè",
        "si",
        "sopra",
        "sotto",
        "su",
        "sua",
        "sue",
        "sugli",
        "sui",
        "sul",
        "sull",
        "sulla",
        "sulle",
        "sullo",
        "suo",
        "suoi",
        "tanto",
        "ti",
        "tras",
        "tu",
        "tua",
        "tue",
        "tuo",
        "tuoi",
        "un",
        "un",
        "una",
        "uno",
        "v",
        "vi",
        "voi",
        "vostra",
        "vostre",
        "vostri",
        "vostro"
    ],
    "ru": [
        "â",
        "bez",
        "dlâ",
        "gde",
        "ili",
        "iz",
        "kak",
        "kotoraâ",
        "kotoroë",
        "kotorye",
        "kotoryj",
        "moâ",
        "moë",
        "moi",
        "moj",
        "my",
        "na",
        "nekotoraâ",
        "nekotoroë",
        "nekotorye",
        "nekotoryj",
        "ob",
        "odin",
        "odna",
        "odni",
        "okolo",
        "on",
        "ona",
        "oni",
        "ot",
        "pered",
        "posie",
        "pri",
        "protiv",
        "svoâ",
        "svoë",
        "svoi",
        "svoj",
        "tvoâ",
        "tvoë",
        "tvoi",
        "tvoj",
        "ty",
        "v tecenie",
        "vy",
        "za"
    ],
    "es": [
        "acà",
        "adónde",
        "adónde",
        "afuera",
        "ahí",
        "ahora",
        "al",
        "alguien",
        "algún",
        "alguna",
        "alguno",
        "ante",
        "antes",
        "apenas",
        "aquél",
        "aquélla",
        "aquéllas",
        "aquello",
        "aquéllos",
        "aquí",
        "así",
        "aún",
        "aunque",
        "bajo",
        "bastante ",
        "cada",
        "calquier",
        "calquiera",
        "casi",
        "cómo",
        "con",
        "conmigo",
        "consigo",
        "contigo",
        "cuàl",
        "cuales",
        "cualesquier",
        "cualesquiera",
        "cuàn",
        "cuando",
        "cuanta",
        "cuantas",
        "cuanto",
        "cuantos",
        "cuya",
        "cuyas",
        "cuyo",
        "cuyos",
        "de",
        "del",
        "demás",
        "demasiada",
        "demasiadas",
        "demasiado",
        "demasiados",
        "desde",
        "después",
        "detrás",
        "dondequiere",
        "durante",
        "él",
        "ella",
        "ellas",
        "ello",
        "ellos",
        "en",
        "entonces",
        "entre",
        "ésa",
        "ésas",
        "ése",
        "eso",
        "ésos",
        "ésta",
        "éstas",
        "éste",
        "esto",
        "éstos",
        "fuera",
        "hasta",
        "jamás",
        "la",
        "las",
        "le",
        "lejos",
        "les",
        "lo",
        "los",
        "luego",
        "más",
        "menos",
        "mí",
        "mía",
        "mías",
        "mientras",
        "mío",
        "míos",
        "mis",
        "misma",
        "mismas",
        "mismo",
        "mismos",
        "mucha",
        "muchas",
        "mucho",
        "muchos",
        "muy",
        "nada",
        "ningún",
        "ninguna",
        "ninguno",
        "no",
        "nos",
        "nosotras",
        "nosotros",
        "nuestra",
        "nuestras",
        "nuestro",
        "nuestros",
        "otra",
        "otras",
        "otro",
        "otros",
        "para",
        "pero",
        "poca",
        "pocas",
        "poco",
        "pocos",
        "por",
        "porque",
        "pues",
        "que",
        "quién",
        "quiénes",
        "quienesquiera",
        "quienquiera",
        "se",
        "sí",
        "siempre",
        "sin",
        "so",
        "sobre",
        "su",
        "sus",
        "suya",
        "suyas",
        "suyo",
        "suyos",
        "tal",
        "también",
        "tampoco",
        "tan",
        "tanta",
        "tantas",
        "tanto",
        "tantos",
        "te",
        "ti",
        "toda",
        "todas",
        "todavía",
        "todo",
        "todos",
        "tras",
        "tú",
        "tus",
        "tuya",
        "tuyo",
        "tuyos",
        "un",
        "una",
        "unas",
        "uno",
        "unos",
        "vos",
        "vosotras",
        "vosotros",
        "vuestra",
        "vuestras",
        "vuestro",
        "vuestros",
        "ya",
        "yo"
    ]
}


# Common
class Common(dict):
    def set_key_if_not_none(self, key, value):
        if value:
            self[key] = value

    def set_key_with_value_type_in_list(self, key, value, my_type):
        if value:
            tmp = {"type": my_type, "value": value}
            try:
                self[key].append(tmp)
            except:
                self[key] = [tmp]

    def set_key_with_value_language_in_list(self, key, value, language):
        if value:
            tmp = {"language": language, "value": value}
            try:
                self[key].append(tmp)
            except:
                self[key] = [tmp]

    def add_items_to_key(self, items, key):
        if items is not None and len(items) != 0:
            for item in items:
                self.add_item_to_key(item, key)

    def add_item_to_key(self, item, key):
        if item:
            try:
                self[key].append(item)
            except:
                self[key] = [item]


# Collection
class Collection(Common):
    pass


# Creator
class Creator(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "agent" in self:
            agent = self["agent"]
            if agent and "rec_class" in agent:
                rec_class = agent["rec_class"]
                if "Person" == rec_class:
                    self["agent"] = Person(self["agent"])
                elif "Orgunit" == rec_class:
                    self["agent"] = Orgunit(self["agent"])
                elif "Event" == rec_class:
                    self["agent"] = Event(self["agent"])
                elif "Family" == rec_class:
                    self["agent"] = Family(self["agent"])

    def formatted_name(self, style=STYLE_FAMILY_COMMA_GIVEN):
        if "agent" in self:
            agent = self["agent"]
            if agent and "rec_class" in agent:
                rec_class = agent["rec_class"]
                if "Person" == rec_class:
                    return agent.formatted_name(style)
                elif "Orgunit" == rec_class:
                    return agent.formatted_name()
                elif "Event" == rec_class:
                    return agent.formatted_name()
                elif "Family" == rec_class:
                    return agent.formatted_name()


# Field
class Field(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Field"


# Document
class Document(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Document"
        if "creators" in self:
            self["creators"] = [Creator(x) for x in self["creators"]]
        if "has_parts" in self:
            self["has_parts"] = [Document(x) for x in self["has_parts"]]
        if "is_part_ofs" in self:
            self["is_part_ofs"] = [Document(x) for x in self["is_part_ofs"]]
        if "is_referenced_bys" in self:
            self["is_referenced_bys"] = [Document(x) for x in self["is_referenced_bys"]]
        if "originals" in self:
            self["originals"] = [Document(x) for x in self["originals"]]
        if "projects" in self:
            self["projects"] = [Project(x) for x in self["projects"]]
        if "references" in self:
            self["references"] = [Document(x) for x in self["references"]]
        if "requires" in self:
            self["requires"] = [Document(x) for x in self["requires"]]
        if "resources" in self:
            self["resources"] = [Resource(x) for x in self["resources"]]
        if "review_ofs" in self:
            self["review_ofs"] = [Document(x) for x in self["review_ofs"]]
        if "rightss" in self:
            self["rightss"] = [Rights(x) for x in self["rightss"]]
        if "seriess" in self:
            self["seriess"] = [Document(x) for x in self["seriess"]]

    def add_creators(self, creators):
        self.add_items_to_key(creators, "creators")

    def get_creators_by_role(self, role):
        results = []
        if "creators" in self:
            for creator in self["creators"]:
                if creator["role"] == role:
                    results.append(creator)
        return results

    def get_date(self):
        date = self.get_property_from_all_level("date_issued")
        if date is None:
            date = self.get_property_from_all_level("date_issued_first")
        if date is None:
            date = self.get_property_from_all_level("date_created")
        if date is None:
            date = self.get_property_from_all_level("date_defence")
        if date is None:
            date = self.get_property_from_all_level("date_captured")
        if date is None:
            date = self.get_property_from_all_level("date_accepted")
        if date is None:
            date = self.get_property_from_all_level("date_submitted")
        if date is None:
            date = self.get_property_from_all_level("date_available")
        if date is None:
            date = self.get_property_from_all_level("date_other")
        return date

    def get_edition(self):
        return self.get_property_from_all_level("edition")

    def get_extent_pages(self):
        return self.get_property_from_all_level("extent_pages")

    def get_extent_volumes(self):
        return self.get_property_from_all_level("extent_volumes")

    def get_part_issue(self):
        return self.get_property_from_all_level("part_issue")

    def get_part_name(self):
        return self.get_property_from_all_level("part_name")

    def get_part_page_start(self):
        return self.get_property_from_all_level("part_page_start")

    def get_part_page_end(self):
        return self.get_property_from_all_level("part_page_end")

    def get_part_volume(self):
        return self.get_property_from_all_level("part_volume")

    def get_publishers(self):
        return self.get_property_from_all_level("publishers")

    def get_publication_countries(self):
        return self.get_property_from_all_level("publication_countries")

    def get_publication_places(self):
        return self.get_property_from_all_level("publication_places")

    def get_publication_states(self):
        return self.get_property_from_all_level("publication_states")

    def get_series_title(self):
        return self.get_property_in_first_object_in_list_from_all_level("seriess", "title")

    def get_type_degree(self):
        return self.get_property_from_all_level("type_degree")

    def get_property_from_all_level(self, my_property):
        if my_property in self and self[my_property]:
            return self[my_property]
        if "is_part_ofs" in self:
            if my_property in self["is_part_ofs"][0] and self["is_part_ofs"][0][my_property]:
                return self["is_part_ofs"][0][my_property]
            if "is_part_ofs" in self["is_part_ofs"][0] and my_property in self["is_part_ofs"][0]["is_part_ofs"][0] and self["is_part_ofs"][0]["is_part_ofs"][0][my_property]:
                return self["is_part_ofs"][0]["is_part_ofs"][0][my_property]

    def get_property_in_object_from_all_level(self, my_object, my_property):
        if my_object in self and my_property in self[my_object] and self[my_object][my_property]:
            return self[my_object][my_property]
        if "is_part_ofs" in self:
            if my_object in self["is_part_ofs"][0] and my_property in self["is_part_ofs"][0][my_object] and self["is_part_ofs"][0][my_object][my_property]:
                return self["is_part_ofs"][0][my_object][my_property]
            if "is_part_ofs" in self["is_part_ofs"][0] and my_object in self["is_part_ofs"][0]["is_part_ofs"][0] and my_property in self["is_part_ofs"][0]["is_part_ofs"][0][my_object] and self["is_part_ofs"]["is_part_ofs"][my_object][my_property]:
                return self["is_part_ofs"][0]["is_part_ofs"][0][my_object][my_property]

    def get_property_in_first_object_in_list_from_all_level(self, my_list, my_property):
        if my_list in self and len(self[my_list]) > 0 and my_property in self[my_list][0] and self[my_list][0][my_property]:
            return self[my_list][0][my_property]
        if "is_part_ofs" in self and len(self["is_part_ofs"]) > 0:
            if my_list in self["is_part_ofs"][0] and len(self["is_part_ofs"][0][my_list]) > 0 and my_property in self["is_part_ofs"][0][my_list][0] and self["is_part_ofs"][0][my_list][0][my_property]:
                return self["is_part_ofs"][0][my_list][0][my_property]
            if "is_part_ofs" in self["is_part_ofs"][0] and len(self["is_part_ofs"][0]["is_part_ofs"]) > 0 and my_list in self["is_part_ofs"][0]["is_part_ofs"][0] and len(self["is_part_ofs"][0]["is_part_ofs"][0][my_list]) > 0 and my_property in self["is_part_ofs"][0]["is_part_ofs"][0][my_list][0] and self["is_part_ofs"][0]["is_part_ofs"][0][my_list][0][my_property]:
                return self["is_part_ofs"][0]["is_part_ofs"][0][my_list][0][my_property]

    def get_first_value_for_type_in_list_from_all_level(self, my_list, my_type):
        if my_list in self:
            my_value = self.get_first_value_for_type_in_list(self[my_list], my_type)
            if my_value:
                return my_value
        if "is_part_ofs" in self:
            if my_list in self["is_part_ofs"][0]:
                my_value = self.get_first_value_for_type_in_list(self["is_part_ofs"][0][my_list], my_type)
                if my_value:
                    return my_value
            if "is_part_ofs" in self["is_part_ofs"][0] and my_list in self["is_part_ofs"][0]["is_part_ofs"][0]:
                my_value = self.get_first_value_for_type_in_list(self["is_part_ofs"][0]["is_part_ofs"][0][my_list], my_type)
                if my_value:
                    return my_value

    def get_first_value_for_type_in_list(self, my_list, my_type):
        if len(my_list) > 0:
            for item in my_list:
                    if "type" in item and "value" in item and item["value"]:
                        if item["type"] == my_type:
                            return item["value"]

    def get_property_for_item_in_list(self, my_list, my_property):
        if len(my_list) > 0:
            for item in my_list:
                if my_property in item and item[my_property]:
                    return item[my_property]


# Event
class Event(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Event"

    def formatted_name(self):
        if "title" in self:
            return self["title"]


# Family
class Family(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Family"

    def formatted_name(self):
        if "name_family" in self:
            return self["name_family"]


# Identifier
class Identifier(Common):
    pass


# Identifier util
# todo : move it to the Identifier constructor
def create_identifier(id_type, id_value):
    if id_value:
        identifier = Identifier()
        identifier["value"] = id_value
        if id_type:
            identifier["id_type"] = id_type
        return identifier


# Orgunit
class Orgunit(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Orgunit"

    def formatted_name(self):
        if "name" in self:
            return self["name"]


# Person
class Person(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Person"

    def formatted_name(self, style=STYLE_FAMILY_COMMA_GIVEN):
        result = ""
        if style == STYLE_FAMILY_COMMA_GIVEN:
            if "name_family" in self and self["name_family"]:
                result += self["name_family"]
            if "name_given" in self and self["name_given"]:
                result += ", " + self["name_given"]
        else:
            if "name_given" in self and self["name_given"]:
                result += self["name_given"] + " "
            if "name_family" in self and self["name_family"]:
                result += self["name_family"]
        return result


# Project
class Project(Common):
    pass


# Resource
class Resource(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Resource"


# Rights
class Rights(Common):
    pass


# SearchQuery
class SearchQuery(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "SearchQuery"


# SearchResponse
class SearchResponse(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "SearchResponse"


# Subject
class Subject(Common):
    pass


# Target
class Target(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Target"


# Type
class Type(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Type"


# Warpper
class Warpper(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = REC_METAJSON
        if "rec_class" not in self:
            self["rec_class"] = "Warpper"
