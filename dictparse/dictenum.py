from enum import Enum

class EJMDict:

    # STANDARD STUFF
    FILE = "../etc/JMdict_e"
    DBFILE = "../etc/jmedict.db"

    # FOR STOP
    XMLHEAD = "<JMdict>"

class KWHeader:

    # FOR PARSING
    DIAL = "<dial> (dialect)"
    FIELD = "<field> entities"
    KEINF = "<ke_inf> (kanji info)"
    MISC = "<misc> (miscellaneous)"
    POS = "<pos> (part-of-speech)"
    REINF = "<re_inf> (reading info)"