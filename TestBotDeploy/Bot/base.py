import sqlite3
import json
import pickle
import time
import psycopg2
from psycopg2.extras import DictCursor

 
# def adapt_list_to_JSON(lst):
#     return json.dumps(lst).encode('utf-8')
# def convert_JSON_to_list(data):
#     return json.load(data.decode('utf-8'))

# sqlite3.register_adapter(list, adapt_list_to_JSON)
# sqlite3.register_converter("json", convert_JSON_to_list)

# def adapt_table_to_pikle(table):
#     return pickle.dumps(table, protocol=0)
#def convert_

# def ensure_connection_ord(func):
#     def inner(*args,**kwargs):
#         with sqlite3.connect('ord.db') as conn:
#             conn.row_factory = sqlite3.Row
#             kwargs['conn'] = conn
#             res=func(*args,**kwargs)
#         return res
       
#     return inner


# def ensure_connection_cocktails(func):
#     def inner(*args,**kwargs):
#         with sqlite3.connect('menu.db') as conn:
#             conn.row_factory = sqlite3.Row
#             kwargs['conn'] = conn
#             res=func(*args,**kwargs)
#         return res
       
#     return inner

# def ensure_connection_users(func):
#     def inner(*args,**kwargs):
#         with sqlite3.connect('users.db') as conn:
#             conn.row_factory = sqlite3.Row
#             kwargs['conn'] = conn
#             res=func(*args,**kwargs)
            
#         return res
    
    
#     return inner

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
        conn.cursor(cursor_factory=DictCursor)
        kwargs['conn'] = conn
        res=func(*args,**kwargs)
        return res
    return inner



@ensure_connection_db
def init_db_ord (conn, force:bool=False):
    c=conn.cursor(cursor_factory=DictCursor)

    if force:
        c.execute('DROP TABLE IF EXISTS ord')

    c.execute(""" CREATE TABLE ord (
                    id     SERIAL UNIQUE,
                    users    INTEGER,
                    time_n    TEXT,
                    zakaz   TEXT
                    )
                """)
    conn.commit()
@ensure_connection_db
def init_db_cocktail (conn, force:bool=False):
    c=conn.cursor(cursor_factory=DictCursor)

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
    cocktails=[
        ('1','Signature Cocktails','Forks Of Flame','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127178575_167561488434254_7863771113045448844_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=LJsBI9AdBFMAX9AdqO7&_nc_ht=scontent.ftlv1-1.fna&oh=b7f1ed3c3ce405dcee191f981fd40232&oe=5FFBF7D3',
        'Basil flavored, spicy herbal refreshing drink on tequila.\nTequila\nBasil\nJalapenon\nLemon juice\nCardamon syrup\nGinger syrup','130','68'),
        ('2','Signature Cocktails','From Madrid to Meico','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127090082_167561438434259_3305127272068609117_o.jpg?_nc_cat=100&ccb=2&_nc_sid=0debeb&_nc_ohc=ajz8CmsIZCgAX_YNnTm&_nc_ht=scontent.ftlv1-1.fna&oh=8ab7a0439314b390848314c6f9920b7a&oe=5FFCF111',
        'Strong, sweet and spicy-bitter smoked tequila drink.\nMezcal\nOrange bitter\nAllspice\nRed vermouth\nCampari','130','68'),
        ('3','Classic Coktails','Espresso martini(vanilla)','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127081831_167567928433610_6078215503493713555_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=9yTM-Uq1-goAX9Az29R&_nc_ht=scontent.ftlv1-1.fna&oh=a3b92f50644b652506a031379fd369ba&oe=60055613',
        'Carefully balanced coffee and vanilla flavored twist on famous classic cocktail.\nVodka vanilla\nEspresso\nKahlua','130','68'),
        ('4','Signature Cocktails','Asian Fizz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127054347_167561728434230_4404559794589276451_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=-_U1PGUque0AX8aY3ZX&_nc_ht=scontent.ftlv8-1.fna&oh=9273eed41dccf10a6a290cce918519bf&oe=6005DC17',
        'Great combination of tarragon and yuzu sake, citrusy-herbal fizzy drink.\nEstragon infused vodka\nOrange juice\nLemon juice\nSimple syrup\nSoda water','140','78'),
        ('5','Signature Cocktails','Shinobi','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127138798_167563258434077_6964723702178916982_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=hY_AZJwWKwgAX9nI-4-&_nc_ht=scontent.ftlv8-1.fna&oh=6f6ff51aa4ede83f22df99a522813320&oe=6007650D',
        'Combination of Japanese gin, sake yuzu and wasabi. Sweet, sour, citrusy with interesting spicy aftertaste.\nVodka\nWasabi\nSake yuzu\nLemon juice\nSugar syrup','130','68'),
        ('6','Signature Cocktails','Slutty Berry','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127052309_167561991767537_699485905314967217_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=XIHm-gjkya8AX8iEmw7&_nc_ht=scontent.ftlv8-1.fna&oh=ffb6c0cd30666bfb476c30e457164ca6&oe=600651DA',
        'Refreshing berry rum drink.\nSpiced rum\nLemon juice\nBerries syrup\nAgave syrup\nLime cordial','130','68'),
        ('7','Signature Cocktails','Sweet&sour=)','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127097609_167565098433893_1232703510494097278_o.jpg?_nc_cat=109&ccb=2&_nc_sid=0debeb&_nc_ohc=chAnzB59naoAX_OHcyt&_nc_oc=AQmbE_1_uoO1-1HukY4C_HnXsXnjZ22fh93xfDSiE0pvLtdgTIyot8NuWOKPE65GKkE&_nc_ht=scontent.ftlv8-1.fna&oh=84ce4261f4cdd4eaa448fc9bbca09634&oe=6004A219',
        'Well-balanced combination of gin, lime, fresh mint and sweetness.\nGin Rangpur\nLemon juice\nSimple syrup\nMint ','130','68'),
        ('8','Signature Cocktails','Raffaello','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127041380_167566178433785_6236730150685643410_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=BVmdFRw5iCoAX8Pd9vb&_nc_ht=scontent.ftlv8-1.fna&oh=fc7e0e1af2dd0cce2804aac69e27106f&oe=60073C87',
        'Dessert, delicate and sweet, nutty vanilla drink.\nWhite rum\nAlmond liquor\nVanilla syrup\nCoconut cream','130','68'),
        ('9','Classic Coktails','Coke-Fashioned','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127035649_167564045100665_8973953467406726760_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=z3IIZoWsn54AX-r-B6F&_nc_ht=scontent.ftlv8-1.fna&oh=cc94214c50ec4299e9cb104c6eb7e30a&oe=6004D7D3',
        'Strong, sweet-herbal and coca-cola flavored view on classic whiskey serving.\nBourbon\nCoke syrup\nBitters','130','68'),
        ('10','Classic Coktails','Banana Daiquiri','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127209815_167567791766957_6855694425986110389_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=NV7SG24ZcPMAX_fbJik&_nc_ht=scontent.ftlv8-1.fna&oh=7fe53fa6e745a0b8a465abe68a069788&oe=6005DB4B',
        'Well-balanced banana flavored sweet and sour rum drink.\nRum\nBanana liquor\nLemon juice','130','68'),
        ('11','Classic Coktails','Tropical Mule','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033835_167563621767374_7131661679747232016_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=GOamDBoEBLkAX8fKSl1&_nc_ht=scontent.ftlv8-1.fna&oh=6665e9928ffbbeb7e67989b6c9e5be4c&oe=600786AE',
        'Tropical combination of citrus, ginger and pineapple, refreshing-fruity fizzy drink.\nPineapple vodka\nTropical bitters\nGinger beer','140','78'),
        ('12','Classic Coktails','Bloody Mary','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033139_167567681766968_8861941791192976825_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=efYTFS-kH4QAX_KqiAU&_nc_ht=scontent.ftlv8-1.fna&oh=7eb15060eff4d6126eb556ce6fd081af&oe=6007A3BC',
        'Deep flavored, spicy tomato famous drink\nVodka\nTomato juice\nSalt\nPepper\nTobacco\nWorcestershire sauce\nCelery\nOlives juice','130','68'),
        ('13','Classic Coktails','Midori sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127027570_167566758433727_1978145568158997735_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=8tihI8spyoMAX-JvUYP&_nc_ht=scontent.ftlv8-1.fna&oh=1021694206b9d5418cc5d198442f5ea2&oe=6006B90C',
        'Sweet and sour like she loves it!\nMidori\nLemon juice\nSugar syrup','130','68'),
        ('14','Classic Coktails','Amaretto Sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127048073_167567028433700_6171345533816315299_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=jmp4UC5d8JYAX997Z9n&_nc_ht=scontent.ftlv8-1.fna&oh=3da99d4104d1600f86d23f03b3ca6387&oe=60075FA1',
        'Balanced sour, almond flavored drink which you most likely know.\nAmaretto\nLemon juice\nSugar syrup','130','68'),
        ('15','Gin&Tonic','G&T Rose','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127141915_167562598434143_8646030941808843264_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=kMGuC_DiWfgAX-wd9VY&_nc_ht=scontent.ftlv8-1.fna&oh=5663c4bcae0bc717c308cc515a43eaac&oe=6006B28F',
        'Grape gin with homemade rose tonic water','140','78'),
        ('16','Gin&Tonic','G&T Lavender','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127190154_167562798434123_4004239542483254563_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=7kgVey5uOUcAX9yqM7B&_nc_ht=scontent.ftlv8-1.fna&oh=7f1f7f3d73134c0de0a8ef0a770d4414&oe=600686F6',
        'Gin with homemade lavender tonic','140','78'),
        ('17','Gin&Tonic','G&T Jasmine','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127065963_167563325100737_6234644096169092399_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=oOzuagDEmuUAX_ZzcGU&_nc_ht=scontent.ftlv8-1.fna&oh=7122f996327b46dce338860255589c13&oe=6004D87F',
        'Grape gin with homemade jasmine tonic','140','78'),
        ('18','Spritz','Aperol spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126989826_167563401767396_6919537105507990360_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=ZD1x3XJiAu8AX-2zkn0&_nc_ht=scontent.ftlv8-1.fna&oh=70ca9023329c339a36df11bf3e103d78&oe=60067A87',
        'Aperol, Prosecco, Soda water','140','78'),
        ('19','Spritz','Aperol lavender spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127024724_167564791767257_917433651836645455_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=tOMHa7Zazt8AX9RMg__&_nc_ht=scontent.ftlv8-1.fna&oh=ee8dbc890b8880968094ac45d8ca6faf&oe=60085788',
        'Aperol, lavender water, prosecco','140','78'),
        ('20','Spritz','Aperol rose spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126455444_167565461767190_866255374477690978_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=MSNLvgDDpKwAX8QXxDZ&_nc_ht=scontent.ftlv8-1.fna&oh=a50a06788f8964c365e32c296b893db6&oe=6006BCF8',
        'Aperol, orange juice, hibiscus soda, prosecco','140','78'),
        ('21','Negronis','Negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042700_167562361767500_3009746689503111905_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=JhlVHKDWtvYAX9lOIFv&_nc_ht=scontent.ftlv8-1.fna&oh=3f48be947c5fdea4978b9bee29f37d85&oe=6004C447',
        'Gin, red vermouth, campari','130','68'),
        ('22','Negronis','Peach negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042619_167566398433763_6362628151006800018_o.jpg?_nc_cat=110&ccb=2&_nc_sid=0debeb&_nc_ohc=vZvf_0F_acYAX9x_Lux&_nc_ht=scontent.ftlv8-1.fna&oh=93845c731bcfb8a31834f02bbbbd6096&oe=60079079',
        'Peach infused gin, red vermouth, campari','130','68'),
        ('23','Negronis','White negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127021870_167566891767047_2595835501233676947_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=E5M6_G9L7PsAX9xBLFq&_nc_ht=scontent.ftlv8-1.fna&oh=5a0ad18928e09b50afa8464f9250bd63&oe=6006DD79',
        'Gin, suze, lillet blanc','130','68')         
              ]
    c.executemany('INSERT INTO cocktails VALUES(%s,%s,%s,%s,%s,%s,%s)',cocktails)
    conn.commit()

@ensure_connection_db
def up_cocktail (conn):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute ('SELECT name, type, url_photo, description, price05, price03 FROM cocktails')# WHERE type = %s',(tip,))
    return c.fetchall()

@ensure_connection_db
def up_cocktail_type (conn):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute ('SELECT DISTINCT type FROM cocktails')
    return c.fetchall()


@ensure_connection_db
def init_db_users(conn, force:bool=False):
    c=conn.cursor(cursor_factory=DictCursor)
    if force:
        c.execute('DROP TABLE IF EXISTS users')
    
    c.execute (''' 
        CREATE TABLE IF NOT EXISTS users(
            user_id      INTEGER PRIMARY KEY NOT NULL,
            name         TEXT DEFAULT 'name',
            phone        TEXT,
            addres       TEXT DEFAULT  'addres',
            ord          TEXT,
            favorites    TEXT
         )
     ''')
    conn.commit()
# @ensure_connection_db
# def add_user(conn, user_id:int, name:str):
#     c=conn.cursor(cursor_factory=DictCursor)
#     c.execute ('INSERT INTO users (user_id,name) VALUES(%s,%s)',(user_id, name))
#     conn.commit()

@ensure_connection_db
def init_user(conn):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT user_id FROM users')
    return c.fetchall()

# @ensure_connection_db
# def add_to_basket(conn, user_id, basket):
#     c=conn.cursor(cursor_factory=DictCursor)
#     c.execute('UPDATE users SET basket = %s WHERE user_id = %s',(basket, user_id))
#     conn.commit()
@ensure_connection_db
def up_users(conn):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT user_id, name, phone, addres, ord FROM users')
    return c.fetchall()

@ensure_connection_db
def update_users(conn, name, phone, addres, ord, user_id):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('UPDATE users SET name=%s, phone=%s, addres=%s, ord=%s WHERE user_id=%s',(name, phone, addres, ord, user_id, ))
    conn.commit()


@ensure_connection_db
def add_user(conn, user_id:int, name:str):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute ('INSERT INTO users (user_id,name) VALUES(%s,%s)',(user_id, name))
    conn.commit()

@ensure_connection_db
def add_name (conn, name:str, user_id:int):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('UPDATE users SET name = %s WHERE user_id = %s',(name, user_id))
    conn.commit()

@ensure_connection_db
def up_name(conn, user_id):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT name FROM users WHERE user_id = %s',(user_id,))
    return c.fetchone()

@ensure_connection_db
def add_phone(conn, user_id, phone):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('UPDATE users SET phone = %s WHERE user_id = %s',(phone, user_id))
    conn.commit()

@ensure_connection_db
def up_phone(conn, user_id):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT phone FROM users WHERE user_id = %s',(user_id,))
    return c.fetchone()

@ensure_connection_db
def add_addres(conn, user_id, addres):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('UPDATE users SET addres = %s WHERE user_id = %s',(addres, user_id))
    conn.commit()

@ensure_connection_db
def up_addres(conn, user_id):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT addres FROM users WHERE user_id = %s',(user_id,))
    return c.fetchone()

@ensure_connection_db
def add_order(conn, user_id, order):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('UPDATE users SET ord =%s WHERE user_id=%s',(order, user_id))
    conn.commit()

@ensure_connection_db
def up_order(conn, user_id):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT ord FROM users WHERE user_id = %s',(user_id,))
    return c.fetchone()
#-------------------------------------------------------------------------------------------------------------------------
@ensure_connection_db
def add_ord(conn,user_id,zakaz):
    c=conn.cursor(cursor_factory=DictCursor)
    a = time.ctime(time.time())
    c.execute('INSERT INTO ord (users,time_n,zakaz) VALUES(%s,%s,%s)',(user_id,a,zakaz))
    conn.commit()
# @ensure_connection_db
# def get_ord(conn):
#     c=conn.cursor(cursor_factory=DictCursor)
#     c.execute('SELECT time_n, zakaz FROM ord WHERE users=%s ORDER BY id DESC LIMIT %s',(user_id, limit,))
#     return c.fetchall()
@ensure_connection_db
def get_ord(conn):
    c=conn.cursor(cursor_factory=DictCursor)
    c.execute('SELECT users, time_n, zakaz FROM ord ORDER BY id DESC')
    return c.fetchall()

if __name__=='__main__':
    # a=up_cocktail_type(conn='')
    # for i in a:
    #     print(i)
    #init_db_users(conn='',force=False)
    # init_db_users(conn='',force=True)
   init_db_cocktail(conn='',force=True)
    # add_user(conn='',user_id=12,name='test')
    # add_ord(conn='',user_id=12, zakaz='weofhiewoif')
    # add_ord(conn='',user_id=12, zakaz='dscdscsdcdsc')
    # #a=up_name(conn='',user_id=12)
    # a=get_ord(conn='',user_id=12, limit=10)
    # #text='\n'.join([f'{time_n}\n{zakaz}' for time_n, zakaz in a])
    # text='\n'.join([f'{m} {d}' for m, d in a])
    # print(text)
    
    # basket=(1, 2, 3)
    # #print (basket)
    # a=adapt_table_to_pikle(basket)
    # print(a)
    # #a=sqlite3.register_adapter(basket, adapt_list_to_JSON(basket))
    # # print(a)
    # add_to_basket(conn='',basket=a, user_id=12)
    # print(load_from_basket(conn='',user_id=12)[0])
    # b=load_from_basket(conn='',user_id=12)
    # print(convert_JSON_to_list(b[0]))

    #tip='Signature Cocktails'
    # m=up_cocktail(conn='',tip='Signature Cocktails')
    # for coсktail in m:
    #     url=coсktail['url_photo']
    #     print (url)
    #    (
    #             id             INTEGER PRIMARY KEY,
    #             type           TEXT NOT NULL,
    #             name           TEXT NOT NULL,
    #             ulr_photo      TEXT NOT NULL,
    #             description    TEXT NOT NULL,
    #             price05        REAL,
    #             price03        REAL
    #             )