import psycopg2

def ensure_connection_db(func):
    def inner(*args,**kwargs):
        conn=psycopg2.connect(
                database='defaultdb',
                user='doadmin',
                password='u85usbgmpbenekvu',
                host='db-postgresql-nyc1-86075-do-user-8476308-0.b.db.ondigitalocean.com',
                port='25060',
                sslmode='require'
                )
        kwargs['conn'] = conn
        res=func(*args,**kwargs)
        return res
    return inner

# con=psycopg2.connect(
#     database='defaultdb',
#     user='doadmin',
#     password='u85usbgmpbenekvu',
#     host='db-postgresql-nyc1-86075-do-user-8476308-0.b.db.ondigitalocean.com',
#     port='25060',
#     sslmode='require'
# )

# cur=con.cursor()
# cur.execute( """ CREATE TABLE orders (
#                     id     INTEGER PRIMARY KEY,
#                     users    INTEGER,
#                     time_n    TEXT,
#                     zakaz   TEXT
#                     )
#                 """) 
# con.commit()

# cur=con.cursor()
# cur.execute( """INSERT INTO orders  VALUES(1 ,2, 'test', 'test2')
#                 """) 
# con.commit()
# con.close()

@ensure_connection_orders
def init_coctails(conn, force:bool=False):
    c=conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS cocktails')

    c.execute(""" CREATE TABLE cocktails
                (
                id              INTEGER PRIMARY KEY NOT NULL,             
                type            TEXT  NOT NULL,           
                name            TEXT  NOT NULL,           
                url_photo       TEXT  NOT NULL,      
                description     TEXT  NOT NULL,    
                price05         REAL  NOT NULL,        
                price03         REAL  NOT NULL   
                )
            """)
    conn.commit()

if __name__=='__main__':
    init_coctails(conn='',force=True)