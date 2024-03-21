from dictenum import EJMDict
from dictenum import KWHeader
import re

class ParseKW:

    # like <!ENTITY ornith "ornithology">
    entity_re = "<!ENTITY\\s([a-zA-Z0-9\-]+)\\s\"(.+)\""
    insert_str = '''INSERT INTO 
        {table} (
            KW, DESCR
        ) 
        VALUES (
            "{val1}", "{val2}"
        )'''

    @staticmethod
    def fill_kw_tables(conn):
        file = open(EJMDict.FILE, encoding="utf8")

        # like a state machine
        current = 0
        dial = 1
        field = 2
        ke_inf = 3
        misc = 4
        pos = 5
        re_inf = 6

        while True:

            line = file.readline()
            if not line:
                break
            
            if KWHeader.DIAL in line:
                current = dial
            elif KWHeader.FIELD in line:
                current = field
            elif KWHeader.KEINF in line:
                current = ke_inf
            elif KWHeader.MISC in line:
                current = misc
            elif KWHeader.POS in line:
                current = pos
            elif KWHeader.REINF in line:
                current = re_inf
            elif EJMDict.XMLHEAD in line:
                return

            if "!ENTITY" not in line:
                continue

            res = re.findall(ParseKW.entity_re, line)
            x = None

            if current == dial:
                x = ParseKW.insert_str.format(table="KWDIAL", val1=res[0][0], val2=res[0][1])
                print(x)
                conn.execute(x)

            elif current == field:
                x = ParseKW.insert_str.format(table="KWFLD", val1=res[0][0], val2=res[0][1])
                conn.execute(x)

            elif current == ke_inf:
                x = ParseKW.insert_str.format(table="KWKINF", val1=res[0][0], val2=res[0][1])
                conn.execute(x)

            elif current == misc:
                x = ParseKW.insert_str.format(table="KWMISC", val1=res[0][0], val2=res[0][1])
                conn.execute(x)

            elif current == pos:
                x = ParseKW.insert_str.format(table="KWPOS", val1=res[0][0], val2=res[0][1])
                conn.execute(x)

            elif current == re_inf:
                x = ParseKW.insert_str.format(table="KWRINF", val1=res[0][0], val2=res[0][1])
                conn.execute(x)

            else:
               print("Error")    

            
            conn.commit()
        return 0