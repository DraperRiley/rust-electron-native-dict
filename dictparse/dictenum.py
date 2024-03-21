from enum import Enum

class EJMDict:

    # Files
    FILE = "../etc/JMdict_e"
    DBFILE = "../etc/jmedict.db"

    # For stop
    XMLHEAD = "<JMdict>"

class KWHeader:

    # For parsing
    DIAL = "<dial> (dialect)"
    FIELD = "<field> entities"
    KEINF = "<ke_inf> (kanji info)"
    MISC = "<misc> (miscellaneous)"
    POS = "<pos> (part-of-speech)"
    REINF = "<re_inf> (reading info)"

class KW(Enum):

    # KW Table Names
    DIAL = "KWDIAL"
    FLD = "KWFLD"
    KINF = "KWKINF"
    MISC = "KWMISC"
    POS = "KWPOS"
    RINF = "KWRINF"
    LANG = "KWLANG"
    XREF = "KWXREF"
    GINF = "KWGINF"
    FREQ = "KWFREQ"
    SRCT = "KWSRCT"
    STAT = "KWSTAT"
    SRC = "KWSRC"
