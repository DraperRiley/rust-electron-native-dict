import sqlite3
import os

class CreateDB:

    @staticmethod
    def create_db():

        os.chdir('.')
        db_file = '..\\etc\\jmedict.db'

        if os.path.exists(db_file):
            os.remove(db_file)

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # create k_ele table THIS IS THE PRIMARY TABLE
        conn.execute('''CREATE TABLE K_ELE(
        ENT_SEQ INTEGER PRIMARY KEY NOT NULL,
        KEB TEXT,
        KE_INF TEXT,
        KE_PRI TEXT);''')

        conn.execute('''CREATE TABLE R_ELE(
        ENT_SEQ INTEGER NOT NULL,
        REB TEXT,
        RE_NOKANJI TEXT,
        RE_RESTR TEXT,
        RE_INF TEXT,
        RE_PRI TEXT,
        FOREIGN KEY(ENT_SEQ) REFERENCES K_ELE(ENT_SEQ));''')

        conn.execute('''CREATE TABLE SENSE
        (ENT_SEQ INTEGER NOT NULL,
        STAGK TEXT,
        STAGR TEXT,
        POS TEXT,
        XREF TEXT,
        ANT TEXT,
        FIELD TEXT,
        MISC TEXT,
        S_INF TEXT,
        LSOURCE TEXT,
        DIAL TEXT,
        GLOSS TEXT,
        FOREIGN KEY(ENT_SEQ) REFERENCES K_ELE(ENT_SEQ));''')

        return 0
    
if __name__ == '__main__':
    CreateDB.create_db()

