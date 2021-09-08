import sqlite3 as sq


def test():
    with sq.connect('test.db') as con:
        cur = con.cursor()

        #cur.execute('''CREATE TABLE Lists (
        #id INTEGER,
        #lists TEXT
        #)''')

        # cur.execute('''DROP TABLE lists''')

        cur.execute('''SELECT lists FROM lists''')
        res = cur.fetchall()
        for el in res[0]:
            print(type(el))
        print(res[0])


with sq.connect('test.db') as con:
    cur = con.cursor()