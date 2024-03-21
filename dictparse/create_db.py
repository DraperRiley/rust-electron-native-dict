import sqlite3
import os
from dictenum import *
from fillkwtables import ParseKW
from optparse import OptionParser

class CreateDB:
    
    @staticmethod
    def create_db(delete_db=False):

        os.chdir('.')

        if os.path.exists(EJMDict.DBFILE):
            print("DB file already exists")
            if delete_db:
                print("Deleting DB file ", EJMDict.DBFILE)
                os.remove(EJMDict.DBFILE)
            

        conn = sqlite3.connect(EJMDict.DBFILE)
        cursor = conn.cursor()

        CreateDB.create_kw_tables(conn)

        # Create ENTR table TOP LEVEL TABLE
        conn.execute(
            '''CREATE TABLE ENTR (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SRC INTEGER,
                STAT INTEGER,
                SEQ INTEGER,
                DFRM INTEGER,
                UNAP INTEGER,
                SRCNOTE TEXT,
                NOTES TEXT,
                IDX INTEGER,
                FOREIGN KEY(SRC) REFERENCES KWSRC(ID),
                FOREIGN KEY(STAT) REFERENCES KWSTAT(ID)
            )'''
        )

        # CREATE SECOND LEVEL TABLES

        conn.execute(
            '''CREATE TABLE SENS (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                NOTES TEXT,
                PRIMARY KEY (ENTR, SENS),
                FOREIGN KEY(ENTR) REFERENCES ENTR(SRC)
            )'''
        )

        conn.execute(
            '''CREATE TABLE KANJ (
                ENTR INTEGER NOT NULL,
                KANJ INTEGER NOT NULL,
                TXT TEXT,
                PRIMARY KEY(ENTR, KANJ),
                FOREIGN KEY(ENTR) REFERENCES ENTR(SRC)
            )'''
        )

        conn.execute(
            '''CREATE TABLE RDNG (
                ENTR INTEGER NOT NULL,
                RDNG INTEGER NOT NULL,
                PRIMARY KEY(ENTR, RDNG),
                FOREIGN KEY(ENTR) REFERENCES ENTR(SRC)
            )'''
        )

        # We will not be creating the change history table
        # CREATE THIRD LEVEL TABLES

        conn.execute(
            '''CREATE TABLE GLOSS (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                GLOSS INTEGER NOT NULL,
                LANG INTEGER,
                GINF INTEGER,
                TXT TEXT,
                PRIMARY KEY(ENTR, SENS, GLOSS),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(LANG) REFERENCES KWLANG(ID),
                FOREIGN KEY(GINF) REFERENCES KWGINF(ID)
            )'''
        )

        # CREATE ATTRIBUTE LIST TABLES

        conn.execute(
            '''CREATE TABLE KINF (
                ENTR INTEGER NOT NULL,
                KANJ INTEGER NOT NULL,
                ORD INTEGER,
                KW INTEGER NOT NULL,
                PRIMARY KEY(ENTR, KANJ, KW),
                FOREIGN KEY(ENTR) REFERENCES KANJ(ENTR),
                FOREIGN KEY(KANJ) REFERENCES KANJ(KANJ),
                FOREIGN KEY(KW) REFERENCES KWKINF(ID)
            )'''
        )

        conn.execute(
            '''CREATE TABLE FREQ (
                ENTR INTEGER NOT NULL,
                RDNG INTEGER NOT NULL,
                KANJ INTEGER NOT NULL,
                KW INTEGER NOT NULL,
                PRIMARY KEY(ENTR, RDNG, KANJ, KW),
                FOREIGN KEY(ENTR) REFERENCES KANJ(ENTR),
                FOREIGN KEY(ENTR) REFERENCES RDNG(ENTR),
                FOREIGN KEY(KANJ) REFERENCES KANJ(KANJ),
                FOREIGN KEY(KW) REFERENCES KWFREQ(ID)
            )'''
        )

        conn.execute(
            '''CREATE TABLE RINF (
                ENTR INTEGER NOT NULL,
                RDNG INTEGER NOT NULL,
                ORD INTEGER,
                KW INTEGER,
                PRIMARY KEY(ENTR, RDNG, KW),
                FOREIGN KEY(ENTR) REFERENCES RDNG(ENTR),
                FOREIGN KEY(RDNG) REFERENCES RDNG(RDNG),
                FOREIGN KEY(KW) REFERENCES KWRINF(ID)
            )'''
        )

        conn.execute(
            '''CREATE TABLE POS (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                ORD INTEGER,
                KW INTEGER NOT NULL,
                PRIMARY KEY(ENTR, SENS, KW),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(KW) REFERENCES KWPOS(ID)
            )'''
        )

        conn.execute(
            '''CREATE TABLE MISC (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                ORD INTEGER,
                KW INTEGER NOT NULL,
                PRIMARY KEY(ENTR, SENS, KW),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(KW) REFERENCES KWMISC(ID)
            )'''
        )

        conn.execute(
            '''CREATE TABLE FLD (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                ORD INTEGER,
                KW INTEGER NOT NULL,
                PRIMARY KEY(ENTR, SENS, KW),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(KW) REFERENCES KWFLD(ID)
            )'''
        )

        conn.execute(
            '''CREATE TABLE DIAL (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                ORD INTEGER,
                KW INTEGER NOT NULL,
                PRIMARY KEY(ENTR, SENS, KW),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(KW) REFERENCES KWDIAL(ID)    
            )'''
        )

        conn.execute(
            '''CREATE TABLE LSOURCE (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                ORD INTEGER,
                LANG INTEGER NOT NULL,
                TXT TEXT NOT NULL,
                PART INTEGER,
                WASEI INTEGER,
                PRIMARY KEY(ENTR, SENS, LANG, TXT),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(LANG) REFERENCES KWLANG(ID)
            )'''
        )

        # CREATE RESTRICTION TABLES

        conn.execute(
            '''CREATE TABLE STAGK (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                KANJ INTEGER NOT NULL,
                PRIMARY KEY(ENTR, SENS, KANJ),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(ENTR) REFERENCES KANJ(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(KANJ) REFERENCES KANJ(KANJ)
            )'''
        )

        conn.execute(
            '''CREATE TABLE STAGR (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                RDNG INTEGER NOT NULL,
                PRIMARY KEY(ENTR, SENS, RDNG),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(ENTR) REFERENCES RDNG(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(RDNG) REFERENCES RDNG(RDNG)
            )'''
        )

        conn.execute(
            '''CREATE TABLE RESTR (
                ENTR INTEGER NOT NULL,
                RDNG INTEGER NOT NULL,
                KANJ INTEGER NOT NULL,
                PRIMARY KEY(ENTR, RDNG, KANJ),
                FOREIGN KEY(ENTR) REFERENCES RDNG(ENTR),
                FOREIGN KEY(ENTR) REFERENCES KANJ(ENTR),
                FOREIGN KEY(RDNG) REFERENCES RDNG(RDNG),
                FOREIGN KEY(KANJ) REFERENCES KANJ(KANJ)
            )'''
        )

        # CREATE CROSS-REFERENCE TABLES

        conn.execute(
            '''CREATE TABLE XREF (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                XREF INTEGER NOT NULL,
                TYP INTEGER,
                XENTR INTEGER NOT NULL,
                XSENS INTEGER NOT NULL,
                RDNG INTEGER,
                KANJ INTEGER,
                NOTES TEXT,
                NOSENS INTEGER,
                LOWPRI INTEGER,
                PRIMARY KEY(ENTR, SENS, XREF, XENTR, XSENS),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(TYP) REFERENCES KWXREF(ID),
                FOREIGN KEY(XENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(XENTR) REFERENCES RDNG(ENTR),
                FOREIGN KEY(XENTR) REFERENCES KANJ(ENTR),
                FOREIGN KEY(XSENS) REFERENCES SENS(SENS),
                FOREIGN KEY(RDNG) REFERENCES RDNG(RDNG),
                FOREIGN KEY(KANJ) REFERENCES KANJ(KANJ)
            )'''
        )

        conn.execute(
            '''CREATE TABLE XRESOLV (
                ENTR INTEGER NOT NULL,
                SENS INTEGER NOT NULL,
                ORD INTEGER NOT NULL,
                TYP INTEGER NOT NULL,
                RTXT TEXT,
                KTXT TEXT,
                TSENS INTEGER,
                VSRC INTEGER,
                VSEQ INTEGER,
                NOTES TEXT,
                PRIO INTEGER,
                PRIMARY KEY(ENTR, SENS, ORD, TYP),
                FOREIGN KEY(ENTR) REFERENCES SENS(ENTR),
                FOREIGN KEY(SENS) REFERENCES SENS(SENS),
                FOREIGN KEY(TYP) REFERENCES KWXREF(KW)
            )'''
        )

        return 0

    def create_kw_tables(conn):

        # CREATE KEYWORD TABLES

        sql_blank = '''CREATE TABLE {table} (
                ID INTEGER PRIMARY KEY NOT NULL,
                KW TEXT,
                DESCR TEXT
            )'''


        for kw in KW:
            if kw == KW.SRC:
                continue

            conn.execute(
                sql_blank.format(table=kw.value)
            )
    
        conn.execute(
            '''CREATE TABLE KWSRC (
                ID INTEGER PRIMARY KEY NOT NULL,
                KW TEXT,
                DESCR TEXT,
                DT TEXT,
                NOTES TEXT,
                SEQ TEXT NOT NULL,
                SINC INTEGER,
                SMIN INTEGER,
                SMAX INTEGER,
                SRCT INTEGER NOT NULL,
                FOREIGN KEY(SRCT) REFERENCES KWSRCT(ID)
            )'''
        )

        return

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-d",
                      "--delete",
                      action="store_true",
                      dest="delete",
                      help="Delete existing .db file"
        )

    (options, args) = parser.parse_args()

    CreateDB.create_db(options.delete)
    conn = sqlite3.connect(EJMDict.DBFILE)
    ParseKW.fill_kw_tables(conn)

    # TODO: Parse the entire XML file

