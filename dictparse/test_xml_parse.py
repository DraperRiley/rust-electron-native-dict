import xml.etree.ElementTree as ET
import logging
import sqlite3
import re
from create_db import CreateDB

logging.basicConfig(level=logging.DEBUG)

def main():

    # CreateDB.create_db()

    conn = sqlite3.connect('jmedict.db')

    xmlfile = 'JMdict_e'
    tree = ET.parse(xmlfile)

    jmdict = tree.getroot()
    items = []

    # print(jmdict.tag)

    # HERES HOW TO DO IT
    # ent_seq is a primary key
    # just concatenate kebs
    # concatenate rebs
    # concatenate pos
    # concatenate gloss
    # use comma as a separator
    # concatenate ke_pri
    # commit to db

    # unique identifier for entries
    ent_seq = "NULL"

    count = 0
    for entry in jmdict:

        # unique identifier for entries
        ent_seq = ""

        # k_ele data
        keb = ""
        ke_inf = ""
        ke_pri = ""

        # r_ele data
        reb = ""
        re_nokanji = ""
        re_restr = ""
        re_inf = ""
        re_pri = ""

        # sense data
        stagk = ""
        stagr = ""
        pos = ""
        xref = ""
        ant = ""
        field = ""
        misc = ""
        s_inf = ""
        lsource = ""
        dial = ""
        gloss = ""

        # FIXED - PROBLEM : THROWING AWAY A LOT OF DATA - VARIABLES BELOW GET REASSIGNED ON ACCIDENT

        for child in entry:

            if child.tag == 'ent_seq':
                ent_seq = child.text

            elif child.tag == 'k_ele':
                temp = parse_k_ele(child)
                keb += temp[0]
                ke_inf += temp[1]
                ke_pri += temp[2]

            elif child.tag == 'r_ele':
                temp = parse_r_ele(child)
                reb += temp[0]
                re_nokanji += temp[1]
                re_restr += temp[2]
                re_inf += temp[3]
                re_pri += temp[4]

            elif child.tag == 'sense':
                temp = parse_sense(child)
                stagk += temp[0]
                stagr += temp[1]
                pos += temp[2]
                xref += temp[3]
                ant += temp[4]
                field += temp[5]
                misc += temp[6]
                s_inf += temp[7]
                lsource += temp[8]
                dial += temp[9]
                gloss += temp[10]

        keb = "NULL" if keb == "" else keb
        ke_inf = "NULL" if ke_inf == "" else ke_inf
        ke_pri = "NULL" if ke_pri == "" else ke_pri
        reb = "NULL" if reb == "" else reb
        re_nokanji = "NULL" if re_nokanji == "" else re_nokanji
        re_restr = "NULL" if re_restr == "" else re_restr
        re_inf = "NULL" if re_inf == "" else re_inf
        re_pri = "NULL" if re_pri == "" else re_pri
        stagk = "NULL" if stagk == "" else stagk
        stagr = "NULL" if stagr == "" else stagr
        pos = "NULL" if pos == "" else pos
        xref = "NULL" if xref == "" else xref
        ant = "NULL" if ant == "" else ant
        field = "NULL" if field == "" else field
        misc = "NULL" if misc == "" else misc
        s_inf = "NULL" if s_inf == "" else s_inf
        lsource = "NULL" if lsource == "" else lsource
        dial = "NULL" if dial == "" else dial
        gloss = "NULL" if gloss == "" else gloss

        #print("ent_seq={0}, keb={1}, ke_inf={2}, ke_pri={3}, reb={4}, re_nokanji={5}, re_restr={6}, re_inf={7}, re_pri={8}, stagk={9}, "
        #      "stagr={10}, pos={11}, xref={12}, ant={13}, field={14}, misc={15}, s_inf={16}, lsource={17}, dial={18}, gloss={19}".format(
        #    ent_seq, keb, ke_inf, ke_pri, reb, re_nokanji, re_restr, re_inf, re_pri, stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss
        #))

        try:

            conn.execute("INSERT INTO K_ELE (ENT_SEQ, KEB, KE_INF, KE_PRI) \
                         VALUES ({}, \'{}\', \'{}\', \'{}\');".format(ent_seq, keb, ke_inf, ke_pri))

            conn.execute("INSERT INTO R_ELE (ENT_SEQ, REB, RE_NOKANJI, RE_RESTR, RE_INF, RE_PRI) \
                        VALUES ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(ent_seq, reb, re_nokanji, re_restr, re_inf, re_pri))

            conn.execute("INSERT INTO SENSE (ENT_SEQ, STAGK, STAGR, POS, XREF, ANT, FIELD, MISC, S_INF, LSOURCE, DIAL, GLOSS) \
                        VALUES ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(ent_seq, stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss))

            conn.commit()

        except Exception as e:
            logging.debug(e)
            logging.debug(gloss)
            exit(1)

        if count % 10 == 0:
            logging.debug("Checkpoint: entry {0}".format(count))
        count += 1

    conn.close()
    return 0


def parse_k_ele(child):

    keb = ""
    ke_inf = ""
    ke_pri = ""

    for ele in child:

        if ele.text is None:
            continue

        if ele.tag == 'keb':
            keb += ele.text + ","
        elif ele.tag == 'ke_inf':
            ke_inf += ele.text + ","
        elif ele.tag == 'ke_pri':
            ke_pri += ele.text + ","

    '''
    keb = "NULL" if keb == "" else keb
    ke_inf = "NULL" if ke_inf == "" else ke_inf
    ke_pri = "NULL" if ke_pri == "" else ke_pri
    '''

    keb = remove_quote(keb)
    ke_inf = remove_quote(ke_inf)
    ke_pri = remove_quote(ke_pri)

    return [keb, ke_inf, ke_pri]


def parse_r_ele(child):

    reb = ""
    re_nokanji = ""
    re_restr = ""
    re_inf = ""
    re_pri = ""

    for ele in child:

        if ele.text is None:
            continue

        if ele.tag == 'reb':
            reb += ele.text + ","
        elif ele.tag == 're_nokanji':
            re_nokanji += ele.text + ","
        elif ele.tag == 're_restr':
            re_restr += ele.text + ","
        elif ele.tag == 're_inf':
            re_inf += ele.text + ","
        elif ele.tag == 're_pri':
            re_pri += ele.text + ","

    '''
    reb = "NULL" if reb == "" else reb
    re_nokanji = "NULL" if re_nokanji == "" else re_nokanji
    re_restr = "NULL" if re_restr == "" else re_restr
    re_inf = "NULL" if re_inf == "" else re_inf
    re_pri = "NULL" if re_pri == "" else re_pri
    '''

    reb = remove_quote(reb)
    re_nokanji = remove_quote(re_nokanji)
    re_restr = remove_quote(re_restr)
    re_inf = remove_quote(re_inf)
    re_pri = remove_quote(re_pri)

    return [reb, re_nokanji, re_restr, re_inf, re_pri]


def parse_sense(child):

    # sense data
    stagk = ""
    stagr = ""
    pos = ""
    xref = ""
    ant = ""
    field = ""
    misc = ""
    s_inf = ""
    lsource = ""
    dial = ""
    gloss = ""

    for ele in child:

        if ele.text is None:
            continue

        if ele.tag == 'stagk':
            stagk += ele.text + ","
        elif ele.tag == 'stagr':
            stagr += ele.text + ","
        elif ele.tag == 'pos':
            pos += ele.text + ","
        elif ele.tag == 'xref':
            xref += ele.text + ","
        elif ele.tag == 'ant':
            ant += ele.text + ","
        elif ele.tag == 'field':
            field += ele.text + ","
        elif ele.tag == 'misc':
            misc += ele.text + ","
        elif ele.tag == 's_inf':
            s_inf += ele.text + ","
        elif ele.tag == 'lsource':
            lsource += ele.text + ","
        elif ele.tag == 'dial':
            dial += ele.text + ","
        elif ele.tag == 'gloss':
            gloss += ele.text + ","

    '''
    stagk = "NULL" if stagk == "" else stagk
    stagr = "NULL" if stagr == "" else stagr
    pos = "NULL" if pos == "" else pos
    xref = "NULL" if xref == "" else xref
    ant = "NULL" if ant == "" else ant
    field = "NULL" if field == "" else field
    misc = "NULL" if misc == "" else misc
    s_inf = "NULL" if s_inf == "" else s_inf
    lsource = "NULL" if lsource == "" else lsource
    dial = "NULL" if dial == "" else dial
    gloss = "NULL" if gloss == "" else gloss
    '''

    stagk = remove_quote(stagk)
    stagr = remove_quote(stagr)
    pos = remove_quote(pos)
    xref = remove_quote(xref)
    ant = remove_quote(ant)
    field = remove_quote(field)
    misc = remove_quote(misc)
    s_inf = remove_quote(s_inf)
    lsource = remove_quote(lsource)
    dial = remove_quote(dial)
    gloss = remove_quote(gloss)

    return [stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss]


def remove_quote(string):
    return re.sub("(\')| (\")", "\'\'", string)


if __name__ == '__main__':
    main()
