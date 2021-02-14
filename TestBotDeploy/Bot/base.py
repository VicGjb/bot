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
        'Basil flavored, spicy herbal refreshing drink on tequila.\n\nTequila\nBasil\nJalapenon\nLemon juice\nCardamon syrup\nGinger syrup','129','78'),
        ('2','Signature Cocktails','From Madrid to Mexico','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127090082_167561438434259_3305127272068609117_o.jpg?_nc_cat=100&ccb=2&_nc_sid=0debeb&_nc_ohc=ajz8CmsIZCgAX_YNnTm&_nc_ht=scontent.ftlv1-1.fna&oh=8ab7a0439314b390848314c6f9920b7a&oe=5FFCF111',
        'Strong, sweet and spicy-bitter smoked tequila drink.\n\nMezcal\nOrange bitter\nAllspice\nRed vermouth\nCampari','129','78'),
        ('3','Classic Coktails','Espresso martini(vanilla)','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127081831_167567928433610_6078215503493713555_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=9yTM-Uq1-goAX9Az29R&_nc_ht=scontent.ftlv1-1.fna&oh=a3b92f50644b652506a031379fd369ba&oe=60055613',
        'Carefully balanced coffee and vanilla flavored twist on famous classic cocktail.\n\nVodka vanilla\nEspresso\nKahlua','129','78'),
        ('4','Signature Cocktails','Asian Fizz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127054347_167561728434230_4404559794589276451_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=-_U1PGUque0AX8aY3ZX&_nc_ht=scontent.ftlv8-1.fna&oh=9273eed41dccf10a6a290cce918519bf&oe=6005DC17',
        'Great combination of tarragon and yuzu sake, citrusy-herbal fizzy drink.\n\nEstragon infused vodka\nOrange juice\nLemon juice\nSimple syrup\nSoda water','140','86'),
        ('5','Signature Cocktails','Shinobi','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127138798_167563258434077_6964723702178916982_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=hY_AZJwWKwgAX9nI-4-&_nc_ht=scontent.ftlv8-1.fna&oh=6f6ff51aa4ede83f22df99a522813320&oe=6007650D',
        'Combination of Japanese gin, sake yuzu and wasabi. Sweet, sour, citrusy with interesting spicy aftertaste.\n\nVodka\nWasabi\nSake yuzu\nLemon juice\nSugar syrup','129','78'),
        ('6','Signature Cocktails','Slutty Berry','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127052309_167561991767537_699485905314967217_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=XIHm-gjkya8AX8iEmw7&_nc_ht=scontent.ftlv8-1.fna&oh=ffb6c0cd30666bfb476c30e457164ca6&oe=600651DA',
        'Refreshing berry rum drink.\n\nSpiced rum\nLemon juice\nBerries syrup\nAgave syrup\nLime cordial','129','78'),
        ('7','Signature Cocktails','Sweet&sour=)','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127097609_167565098433893_1232703510494097278_o.jpg?_nc_cat=109&ccb=2&_nc_sid=0debeb&_nc_ohc=chAnzB59naoAX_OHcyt&_nc_oc=AQmbE_1_uoO1-1HukY4C_HnXsXnjZ22fh93xfDSiE0pvLtdgTIyot8NuWOKPE65GKkE&_nc_ht=scontent.ftlv8-1.fna&oh=84ce4261f4cdd4eaa448fc9bbca09634&oe=6004A219',
        'Well-balanced combination of gin, lime, fresh mint and sweetness.\n\nGin Rangpur\nLemon juice\nSimple syrup\nMint','129','78'),
        ('8','Signature Cocktails','Raffaello','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127041380_167566178433785_6236730150685643410_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=BVmdFRw5iCoAX8Pd9vb&_nc_ht=scontent.ftlv8-1.fna&oh=fc7e0e1af2dd0cce2804aac69e27106f&oe=60073C87',
        'Dessert, delicate and sweet, nutty vanilla drink.\n\nWhite rum\nAlmond liquor\nVanilla syrup\nCoconut cream','129','78'),
        
        ('9','Classic Coktails','Coke-Fashioned','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127035649_167564045100665_8973953467406726760_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=z3IIZoWsn54AX-r-B6F&_nc_ht=scontent.ftlv8-1.fna&oh=cc94214c50ec4299e9cb104c6eb7e30a&oe=6004D7D3',
        'Strong, sweet-herbal and coca-cola flavored view on classic whiskey serving.\n\nBourbon\nCoke syrup\nBitters','129','78'),
        ('10','Classic Coktails','Banana Daiquiri','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127209815_167567791766957_6855694425986110389_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=NV7SG24ZcPMAX_fbJik&_nc_ht=scontent.ftlv8-1.fna&oh=7fe53fa6e745a0b8a465abe68a069788&oe=6005DB4B',
        'Well-balanced banana flavored sweet and sour rum drink.\n\nRum\nBanana liquor\nLemon juice','129','78'),
        ('11','Classic Coktails','Tropical Mule','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033835_167563621767374_7131661679747232016_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=GOamDBoEBLkAX8fKSl1&_nc_ht=scontent.ftlv8-1.fna&oh=6665e9928ffbbeb7e67989b6c9e5be4c&oe=600786AE',
        'Tropical combination of citrus, ginger and pineapple, refreshing-fruity fizzy drink.\n\nPineapple vodka\nTropical bitters\nGinger beer','140','86'),
        ('12','Classic Coktails','Bloody Mary','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033139_167567681766968_8861941791192976825_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=efYTFS-kH4QAX_KqiAU&_nc_ht=scontent.ftlv8-1.fna&oh=7eb15060eff4d6126eb556ce6fd081af&oe=6007A3BC',
        'Deep flavored, spicy tomato famous drink.\n\nVodka\nTomato juice\nSalt\nPepper\nTobacco\nWorcestershire sauce\nCelery\nOlives juice','129','78'),
        ('13','Classic Coktails','Midori sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127027570_167566758433727_1978145568158997735_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=8tihI8spyoMAX-JvUYP&_nc_ht=scontent.ftlv8-1.fna&oh=1021694206b9d5418cc5d198442f5ea2&oe=6006B90C',
        'Sweet and sour like she loves it!\n\nMidori\nLemon juice\nSugar syrup','129','78'),
        ('14','Classic Coktails','Amaretto Sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127048073_167567028433700_6171345533816315299_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=jmp4UC5d8JYAX997Z9n&_nc_ht=scontent.ftlv8-1.fna&oh=3da99d4104d1600f86d23f03b3ca6387&oe=60075FA1',
        'Balanced sour, almond flavored drink which you most likely know.\n\nAmaretto\nLemon juice\nSugar syrup','129','78'),

        ('15','Gin&Tonic','G&T Rose','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127141915_167562598434143_8646030941808843264_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=kMGuC_DiWfgAX-wd9VY&_nc_ht=scontent.ftlv8-1.fna&oh=5663c4bcae0bc717c308cc515a43eaac&oe=6006B28F',
        'Flowery, with the scent of wild rose and grape, sweet with light bitterness of classic G&T.\n\nFrench gin\nHomemade rose tonic water','140','86'),
        ('16','Gin&Tonic','G&T Lavender','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127190154_167562798434123_4004239542483254563_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=7kgVey5uOUcAX9yqM7B&_nc_ht=scontent.ftlv8-1.fna&oh=7f1f7f3d73134c0de0a8ef0a770d4414&oe=600686F6',
        'Spicy, flowery with the scent of lavender and citrus with light bitterness of classic G&T.\n\nGin\nHomemade lavender tonic water','140','86'),
        ('17','Gin&Tonic','G&T Jasmine','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127065963_167563325100737_6234644096169092399_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=oOzuagDEmuUAX_ZzcGU&_nc_ht=scontent.ftlv8-1.fna&oh=7122f996327b46dce338860255589c13&oe=6004D87F',
        'Refreshing and restorative with scent of jasmine grapes and citrus.\n\nFrench gin\nHomemade jasmine tonic water','140','86'),
        
        ('18','Spritz','Aperol spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126989826_167563401767396_6919537105507990360_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=ZD1x3XJiAu8AX-2zkn0&_nc_ht=scontent.ftlv8-1.fna&oh=70ca9023329c339a36df11bf3e103d78&oe=60067A87',
        'Classic fizzy and citrusy drink.\n\nAperol\nProsecco\nSoda water','140','86'),
        ('19','Spritz','Aperol lavender spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127024724_167564791767257_917433651836645455_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=tOMHa7Zazt8AX9RMg__&_nc_ht=scontent.ftlv8-1.fna&oh=ee8dbc890b8880968094ac45d8ca6faf&oe=60085788',
        'Sweet, fizzy with flowery bitterness of lavander.\n\nAperol\nLavender water\nProsecco','140','86'),
        ('20','Spritz','Aperol rose spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126455444_167565461767190_866255374477690978_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=MSNLvgDDpKwAX8QXxDZ&_nc_ht=scontent.ftlv8-1.fna&oh=a50a06788f8964c365e32c296b893db6&oe=6006BCF8',
        'Spicy, flowery-citrusy and fizzy.\n\nAperol\nOrange juice\nHibiscus soda\nProsecco','140','86'),


        ('21','Negronis','Negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042700_167562361767500_3009746689503111905_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=JhlVHKDWtvYAX9lOIFv&_nc_ht=scontent.ftlv8-1.fna&oh=3f48be947c5fdea4978b9bee29f37d85&oe=6004C447',
        'Classic, bitter-sweet and strong.\n\nGin\nRed vermouth\nCampari','140','86'),
        ('22','Negronis','Peach negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042619_167566398433763_6362628151006800018_o.jpg?_nc_cat=110&ccb=2&_nc_sid=0debeb&_nc_ohc=vZvf_0F_acYAX9x_Lux&_nc_ht=scontent.ftlv8-1.fna&oh=93845c731bcfb8a31834f02bbbbd6096&oe=60079079',
        'Bitter-sweet, strong with fruity aftertaste.\n\nPeach infused gin\nRed vermouth\nCampari','140','86'),
        ('23','Negronis','White negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127021870_167566891767047_2595835501233676947_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=E5M6_G9L7PsAX9xBLFq&_nc_ht=scontent.ftlv8-1.fna&oh=5a0ad18928e09b50afa8464f9250bd63&oe=6006DD79',
        'Flowery-bitter, sweet and strong.\n\nGin\nSuze\nLillet blanc','140','86'),



        ('25','קוקטיילים הבית','Forks Of Flame','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127178575_167561488434254_7863771113045448844_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=LJsBI9AdBFMAX9AdqO7&_nc_ht=scontent.ftlv1-1.fna&oh=b7f1ed3c3ce405dcee191f981fd40232&oe=5FFBF7D3',
        "בטעם בזיליקום, צמחי, פיקנטי  ומרענן.\n\nטקילה\nבזיליק\nחלפניו\nמיץ לימון\nסירופ הל\n סירופ ג'ינג'ר\n ",'129','78'),   
        ('26','קוקטיילים הבית','From Madrid to Mexico','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127090082_167561438434259_3305127272068609117_o.jpg?_nc_cat=100&ccb=2&_nc_sid=0debeb&_nc_ohc=ajz8CmsIZCgAX_YNnTm&_nc_ht=scontent.ftlv1-1.fna&oh=8ab7a0439314b390848314c6f9920b7a&oe=5FFCF111',
        "טעם חריף מתוק, חזק ומתובל, מעושן עם טעם של טקילה מורגש.\n\nמזקל\nביטר הדרים\nתבלינים\nורמוט אדום\nסירופ הל\nקמפרי\n ",'129','78'),
        ('27','קוקטיילים הבית','Asian Fizz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127054347_167561728434230_4404559794589276451_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=-_U1PGUque0AX8aY3ZX&_nc_ht=scontent.ftlv8-1.fna&oh=9273eed41dccf10a6a290cce918519bf&oe=6005DC17',
        "שילוב מצויין של אסטראגון ויוזו,טעם הדרי וצמחי, מוגז.\n\nאינפוזיה וודקה על אסטרגון\nמיץ תפוזים\nמיץ לימון\nמי סוכר\nסודה\n ",'129','78'),
        ('28','קוקטיילים הבית','Shinobi','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127138798_167563258434077_6964723702178916982_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=hY_AZJwWKwgAX9nI-4-&_nc_ht=scontent.ftlv8-1.fna&oh=6f6ff51aa4ede83f22df99a522813320&oe=6007650D',
        "שילוב של ג'ין יפני, סאקה יוזו ווואסאבי. חמוץ מתוק, הדרי עם טעם שאחרי פיקנטי ומקורי.\n\nוודקה\nוואסבי\nסאקה יוזו\nמי סוכר\nמיץ לימון\n ",'129','78'),
        ('29','קוקטיילים הבית','Slutty Berry','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127052309_167561991767537_699485905314967217_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=XIHm-gjkya8AX8iEmw7&_nc_ht=scontent.ftlv8-1.fna&oh=ffb6c0cd30666bfb476c30e457164ca6&oe=600651DA',
        "רום, פירות יער מרענן ומתוק.\n\nרום מתובל\nסירופ פירות יער\nמיץ לימון\nסירופ אגבה\nקורדיאל ליים\n ",'129','78'),
        ('30','קוקטיילים הבית','Sweet&sour=)','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127097609_167565098433893_1232703510494097278_o.jpg?_nc_cat=109&ccb=2&_nc_sid=0debeb&_nc_ohc=chAnzB59naoAX_OHcyt&_nc_oc=AQmbE_1_uoO1-1HukY4C_HnXsXnjZ22fh93xfDSiE0pvLtdgTIyot8NuWOKPE65GKkE&_nc_ht=scontent.ftlv8-1.fna&oh=84ce4261f4cdd4eaa448fc9bbca09634&oe=6004A219',
        "שילוב מאוזן בקפידה, של ג'ין, ליים, נענע טרייה ומתיקות מעודנת.\n\nאינפוזיה ג'ין על ליים\nנענע\nמיץ לימון\nמי סוכר\n ",'129','78'),
        ('31','קוקטיילים הבית','Raffaello','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127041380_167566178433785_6236730150685643410_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=BVmdFRw5iCoAX8Pd9vb&_nc_ht=scontent.ftlv8-1.fna&oh=fc7e0e1af2dd0cce2804aac69e27106f&oe=60073C87',
        "קינוחי, עדין ומתוק, שילוב של אגוז ווניל.\n\nרום\nליקר שקדים\nסירופ וניל\nקרם קוקוס\n ",'129','78'),
        
        ('32','קוקטיילים קלאסיים','Espresso martini(vanilla)','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127081831_167567928433610_6078215503493713555_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=9yTM-Uq1-goAX9Az29R&_nc_ht=scontent.ftlv1-1.fna&oh=a3b92f50644b652506a031379fd369ba&oe=60055613',
        "מאוזן בקפידות  שילוב של קפה  ווניל, טוויסט של קוקטייל קלסי ידועה.\n\nוודקה וניל\nאספרסו\nליקר קלואה\n ",'129','78'),
        ('33','קוקטיילים קלאסיים','Coke-Fashioned','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127035649_167564045100665_8973953467406726760_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=z3IIZoWsn54AX-r-B6F&_nc_ht=scontent.ftlv8-1.fna&oh=cc94214c50ec4299e9cb104c6eb7e30a&oe=6004D7D3',
        "חזק, צמחי ומתקתק, צורת הגשה חדשנית  של וויסקי הקלאסי.\n\nבורבון\nסירופ קולה\nביטרים\n ",'129','78'),
        ('34','קוקטיילים קלאסיים','Banana Daiquiri','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127209815_167567791766957_6855694425986110389_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=NV7SG24ZcPMAX_fbJik&_nc_ht=scontent.ftlv8-1.fna&oh=7fe53fa6e745a0b8a465abe68a069788&oe=6005DB4B',
        "רום ובננה בטעם חמוץ מאוזן.\n\nרום\nליקר בננה\nמיץ לימון\n ",'129','78'),
        ('35','קוקטיילים קלאסיים','Tropical Mule','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033835_167563621767374_7131661679747232016_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=GOamDBoEBLkAX8fKSl1&_nc_ht=scontent.ftlv8-1.fna&oh=6665e9928ffbbeb7e67989b6c9e5be4c&oe=600786AE',
        "שילוב טרופי והדרי עם ג'ינג'ר ואננס עסיסי, פירותי מרענן ותוסס.\n\nוודקה אננס\nביטרים טרופיים\nג'ינג'ר בייר\n ",'140','86'),
        ('36','קוקטיילים קלאסיים','Bloody Mary','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033139_167567681766968_8861941791192976825_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=efYTFS-kH4QAX_KqiAU&_nc_ht=scontent.ftlv8-1.fna&oh=7eb15060eff4d6126eb556ce6fd081af&oe=6007A3BC',
        "טעם עשיר, של עגבניה פיקנטית משקה מפורסם שכולם מכירים.\n\nוודקה\nמיץ עגבניות\nמלח\nפלפל\nטבסקו\nרוטב וורצ'סטר\nסלרי\nמרינדת זיתים\n ",'140','86'),
        ('37','קוקטיילים קלאסיים','Midori sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127027570_167566758433727_1978145568158997735_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=8tihI8spyoMAX-JvUYP&_nc_ht=scontent.ftlv8-1.fna&oh=1021694206b9d5418cc5d198442f5ea2&oe=6006B90C',
        "חמוץ מתוק כמו שהיא אוהבת.\n\nמידורי\nמיץ לימון\nמי סוכר\n ",'129','78'),
        ('38','קוקטיילים קלאסיים','Amaretto Sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127048073_167567028433700_6171345533816315299_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=jmp4UC5d8JYAX997Z9n&_nc_ht=scontent.ftlv8-1.fna&oh=3da99d4104d1600f86d23f03b3ca6387&oe=60075FA1',
        "חמוץ מאוזן בטעם שקדים,  אתם בתוח מכירים אותו!\n\nאמרטו\nמיץ לימון\nמי סוכר\n",'129','78'),

        ('39',"ג'ין וטוניק",'G&T Rose','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127141915_167562598434143_8646030941808843264_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=kMGuC_DiWfgAX-wd9VY&_nc_ht=scontent.ftlv8-1.fna&oh=5663c4bcae0bc717c308cc515a43eaac&oe=6006B28F',
        "טעם פרחי עם ארומה של ורד בר וענבים, מתוק עם מרירות עדינה של ג'ין טוניק הקלאסי.\n\nג'ין צרפתי\nטוניק הבית\n",'140','86'),
        ('40',"ג'ין וטוניק",'G&T Lavender','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127190154_167562798434123_4004239542483254563_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=7kgVey5uOUcAX9yqM7B&_nc_ht=scontent.ftlv8-1.fna&oh=7f1f7f3d73134c0de0a8ef0a770d4414&oe=600686F6',
        "טעם מתובל פרחי עם ארומה של לוונדר ופרי הדר ועם טעם המרירות הקלאסי של ג'ין טוניק.\n\nג'ין\nטוניק הבית\n",'140','86'),
        ('41',"ג'ין וטוניק",'G&T Jasmine','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127065963_167563325100737_6234644096169092399_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=oOzuagDEmuUAX_ZzcGU&_nc_ht=scontent.ftlv8-1.fna&oh=7122f996327b46dce338860255589c13&oe=6004D87F',
        "מרענן ומעודד עם ארומה של יסמין ,ענבים ופרי הדר.\n\nג'ין צרפתי\nטוניק הבית\n",'140','86'),

        ('42',"אפרול שפריץ טוויסת",'Aperol spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126989826_167563401767396_6919537105507990360_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=ZD1x3XJiAu8AX-2zkn0&_nc_ht=scontent.ftlv8-1.fna&oh=70ca9023329c339a36df11bf3e103d78&oe=60067A87',
        "קלאסי תוסס והדרי.\n\nאפרול\nפרוסקו\nסודה\n",'140','86'),
        ('43',"אפרול שפריץ טוויסת",'Aperol lavender spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127024724_167564791767257_917433651836645455_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=tOMHa7Zazt8AX9RMg__&_nc_ht=scontent.ftlv8-1.fna&oh=ee8dbc890b8880968094ac45d8ca6faf&oe=60085788',
        "מתוק, פרחי עם מרירות של לוונדר, תוסס.\n\nאפרול\nפרוסקו\nמי לוונדר\n",'140','86'),
        ('44',"אפרול שפריץ טוויסת",'Aperol rose spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126455444_167565461767190_866255374477690978_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=MSNLvgDDpKwAX8QXxDZ&_nc_ht=scontent.ftlv8-1.fna&oh=a50a06788f8964c365e32c296b893db6&oe=6006BCF8',
        "מתובל פרחי והדרי, תוסס.\n\nאפרול\nפרוסקו\nמיץ תפוזים\nמי היביסקוס\n",'140','86'),

        ('45',"נגרוני טוויסת",'Negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042700_167562361767500_3009746689503111905_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=JhlVHKDWtvYAX9lOIFv&_nc_ht=scontent.ftlv8-1.fna&oh=3f48be947c5fdea4978b9bee29f37d85&oe=6004C447',
        "טעם קלאסי, מר מתוק וחזק.\n\nג'ין\nקמפרי\nורמוט אדום\n",'140','86'),
        ('46',"נגרוני טוויסת",'Peach negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042619_167566398433763_6362628151006800018_o.jpg?_nc_cat=110&ccb=2&_nc_sid=0debeb&_nc_ohc=vZvf_0F_acYAX9x_Lux&_nc_ht=scontent.ftlv8-1.fna&oh=93845c731bcfb8a31834f02bbbbd6096&oe=60079079',
        "מר וחזק עם טעם פירותי שאחרי.\n\nאינפוזיה ג'ין על אפרסק\nקמפרי\nורמוט אדום\n",'140','86'),
        ('47',"נגרוני טוויסת",'White negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127021870_167566891767047_2595835501233676947_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=E5M6_G9L7PsAX9xBLFq&_nc_ht=scontent.ftlv8-1.fna&oh=5a0ad18928e09b50afa8464f9250bd63&oe=6006DD79',
        "טעם פרחי ומריר מתקתק וחזק.\n\nג'ין צרפתי\n\nסוז\nלילט\n",'140','86'),


        ('24','Авторские коктейли','Forks Of Flame','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127178575_167561488434254_7863771113045448844_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=LJsBI9AdBFMAX9AdqO7&_nc_ht=scontent.ftlv1-1.fna&oh=b7f1ed3c3ce405dcee191f981fd40232&oe=5FFBF7D3',
        'Базиликовый, травянисто пикантный, освежающий текильный напиток.\n\nТекила\nБазилик\nХалапеньо\nЛемонный сок\nКардамоновый сироп\nИмбирный сироп','129','78'),
        ('48','Авторские коктейли','From Madrid to Mexico','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127090082_167561438434259_3305127272068609117_o.jpg?_nc_cat=100&ccb=2&_nc_sid=0debeb&_nc_ohc=ajz8CmsIZCgAX_YNnTm&_nc_ht=scontent.ftlv1-1.fna&oh=8ab7a0439314b390848314c6f9920b7a&oe=5FFCF111',
        'Горько-сладкий, крепкий, пряный, копчено-текильный.\n\nМескаль\nЦитрусовые биттеры\nСпеции\nКрасный вермут\nКампари','129','78'),
        ('49','Авторские коктейли','Asian Fizz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127054347_167561728434230_4404559794589276451_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=-_U1PGUque0AX8aY3ZX&_nc_ht=scontent.ftlv8-1.fna&oh=9273eed41dccf10a6a290cce918519bf&oe=6005DC17',
        'Отличное сочетание эстрагона и юдзо, цитрусово-травяной, газированный.\n\nВодка настоянная на эстрагоне\nАпельсиновый сок\nЛимонный сок\nСахарный сироп\nСодовая','140','86'),
        ('50','Авторские коктейли','Shinobi','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127138798_167563258434077_6964723702178916982_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=hY_AZJwWKwgAX9nI-4-&_nc_ht=scontent.ftlv8-1.fna&oh=6f6ff51aa4ede83f22df99a522813320&oe=6007650D',
        'Сочетание японского джина, саке Юдзо и васаби. Кисло-сладкий, цитрусовый, с оригинальным пикантным послевкусием.\n\nВодка\nВасаби\nсаке Юдзо\nЛимонный сок\nСахарный сироп','129','78'),
        ('51','Авторские коктейли','Slutty Berry','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127052309_167561991767537_699485905314967217_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=XIHm-gjkya8AX8iEmw7&_nc_ht=scontent.ftlv8-1.fna&oh=ffb6c0cd30666bfb476c30e457164ca6&oe=600651DA',
        'Ромовый, ягодный, освежающе-сладкий.\n\nПряный Ром\nЛимонный сок\nЯгодный сироп\nСироп агавы\nЛаймовый кордиал','129','78'),
        ('52','Авторские коктейли','Sweet&sour=)','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127097609_167565098433893_1232703510494097278_o.jpg?_nc_cat=109&ccb=2&_nc_sid=0debeb&_nc_ohc=chAnzB59naoAX_OHcyt&_nc_oc=AQmbE_1_uoO1-1HukY4C_HnXsXnjZ22fh93xfDSiE0pvLtdgTIyot8NuWOKPE65GKkE&_nc_ht=scontent.ftlv8-1.fna&oh=84ce4261f4cdd4eaa448fc9bbca09634&oe=6004A219',
        'Тщательно сбалансированное сочетание, джина, лайма, свежей мяты и сладости.\n\nДжин Рангпур\nЛимонный сок\nСахарный сироп\nМята','129','78'),
        ('53','Авторские коктейли','Raffaello','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127041380_167566178433785_6236730150685643410_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=BVmdFRw5iCoAX8Pd9vb&_nc_ht=scontent.ftlv8-1.fna&oh=fc7e0e1af2dd0cce2804aac69e27106f&oe=60073C87',
        'Десертный, нежный и сладкий, орехово-ванильный напиток.\n\nРом\nОреховый ликер\nВанильный сироп\nКокосовые сливки','129','78'),


        ('54','Классические коктейли','Espresso martini(vanilla)','https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/127081831_167567928433610_6078215503493713555_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=9yTM-Uq1-goAX9Az29R&_nc_ht=scontent.ftlv1-1.fna&oh=a3b92f50644b652506a031379fd369ba&oe=60055613',
        'Заботливо сбалансированный кофейно-ванильный твист на популярный классический напиток.\n\nВанильная водка\nЭспрессо\nЛикёр "Калуа"','129','78'),
        ('55','Классические коктейли','Coke-Fashioned','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127035649_167564045100665_8973953467406726760_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=z3IIZoWsn54AX-r-B6F&_nc_ht=scontent.ftlv8-1.fna&oh=cc94214c50ec4299e9cb104c6eb7e30a&oe=6004D7D3',
        'Крепкий, сладко травяной, свежий взгляд на классическую подачу виски.\n\nБурбон\nСироп кока-кола\nБиттеры','129','78'),
        ('56','Классические коктейли','Banana Daiquiri','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127209815_167567791766957_6855694425986110389_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=NV7SG24ZcPMAX_fbJik&_nc_ht=scontent.ftlv8-1.fna&oh=7fe53fa6e745a0b8a465abe68a069788&oe=6005DB4B',
        'Ромовый, банановый, сбалансированно кислый.\n\nРом\nБанановый ликёр\nЛимонный сок','129','78'),
        ('57','Классические коктейли','Tropical Mule','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033835_167563621767374_7131661679747232016_o.jpg?_nc_cat=108&ccb=2&_nc_sid=0debeb&_nc_ohc=GOamDBoEBLkAX8fKSl1&_nc_ht=scontent.ftlv8-1.fna&oh=6665e9928ffbbeb7e67989b6c9e5be4c&oe=600786AE',
        'Тропическое сочетание цитрусовых, имбиря и ананаса, освежающе-фруктовый, газированный.\n\nАнанасовая водка\nТропические биттеры\nИмбирное пиво','140','86'),
        ('58','Классические коктейли','Bloody Mary','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127033139_167567681766968_8861941791192976825_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=efYTFS-kH4QAX_KqiAU&_nc_ht=scontent.ftlv8-1.fna&oh=7eb15060eff4d6126eb556ce6fd081af&oe=6007A3BC',
        'Насыщенный, пикантно-томатный знаменитый напиток.\n\nВодка\nТоматный сок\nСоль\nПерец\nТабаско\nВорчестерский соус\nСельдерей\nОливковый маринад','129','78'),
        ('59','Классические коктейли','Midori sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127027570_167566758433727_1978145568158997735_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=8tihI8spyoMAX-JvUYP&_nc_ht=scontent.ftlv8-1.fna&oh=1021694206b9d5418cc5d198442f5ea2&oe=6006B90C',
        'Кисло-сладкий, как она любит!\n\nЛикёр "Мидори"\nЛимонный сок\nСахарный сироп','129','78'),
        ('60','Классические коктейли','Amaretto Sour','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127048073_167567028433700_6171345533816315299_o.jpg?_nc_cat=106&ccb=2&_nc_sid=0debeb&_nc_ohc=jmp4UC5d8JYAX997Z9n&_nc_ht=scontent.ftlv8-1.fna&oh=3da99d4104d1600f86d23f03b3ca6387&oe=60075FA1',
        'Сбалансированно-кислый, миндальный, ты точно его знаешь!\n\nЛикёр "Амаретто"\nЛемонный сок\nСахарный сироп','129','78'),

        ('61','Джин и тоник','G&T Rose','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127141915_167562598434143_8646030941808843264_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=kMGuC_DiWfgAX-wd9VY&_nc_ht=scontent.ftlv8-1.fna&oh=5663c4bcae0bc717c308cc515a43eaac&oe=6006B28F',
        'Цветочный, с ароматом дикой розы и винограда, сладкий с горчинкой классического G&T.\n\nФранцузкий джин\nДомашний тоник из дикой розы','140','86'),
        ('62','Джин и тоник','G&T Lavender','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127190154_167562798434123_4004239542483254563_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=7kgVey5uOUcAX9yqM7B&_nc_ht=scontent.ftlv8-1.fna&oh=7f1f7f3d73134c0de0a8ef0a770d4414&oe=600686F6',
        'Пряный, цветочный с ароматом лаванды и цитруса с полноценной горечью присущей классическому G&T.\n\nДжин\nДомашний тоник из лаванды','140','86'),
        ('63','Джин и тоник','G&T Jasmine','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127065963_167563325100737_6234644096169092399_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=oOzuagDEmuUAX_ZzcGU&_nc_ht=scontent.ftlv8-1.fna&oh=7122f996327b46dce338860255589c13&oe=6004D87F',
        'Освежающий и тонизирующий, с ароматом жасмина винограда и цитруса.\n\nФранцузкий джин\nДомашний тоник из жасмина','140','86'),

        ('64','Апероль спритц твисты','Aperol spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126989826_167563401767396_6919537105507990360_o.jpg?_nc_cat=102&ccb=2&_nc_sid=0debeb&_nc_ohc=ZD1x3XJiAu8AX-2zkn0&_nc_ht=scontent.ftlv8-1.fna&oh=70ca9023329c339a36df11bf3e103d78&oe=60067A87',
        'Классический, игристый и цитрусовый\n\nАпероль\nПросекко\nСодовая','140','86'),
        ('65','Апероль спритц твисты','Aperol lavender spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127024724_167564791767257_917433651836645455_o.jpg?_nc_cat=105&ccb=2&_nc_sid=0debeb&_nc_ohc=tOMHa7Zazt8AX9RMg__&_nc_ht=scontent.ftlv8-1.fna&oh=ee8dbc890b8880968094ac45d8ca6faf&oe=60085788',
        'Сладкий с цветочной горчинкой, лавандовый, игристый.\n\nАпероль\nПросекко\nЛавандовая содовая','140','86'),
        ('66','Апероль спритц твисты','Aperol rose spritz','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/126455444_167565461767190_866255374477690978_o.jpg?_nc_cat=101&ccb=2&_nc_sid=0debeb&_nc_ohc=MSNLvgDDpKwAX8QXxDZ&_nc_ht=scontent.ftlv8-1.fna&oh=a50a06788f8964c365e32c296b893db6&oe=6006BCF8',
        'Пряный, цветочно-цитрусовый, игристый.\n\nАпероль\nАпельсиновый сок\nПросекко\nГискусовая содовая','140','86'),


        ('67','Негрони твисты','Negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042700_167562361767500_3009746689503111905_o.jpg?_nc_cat=107&ccb=2&_nc_sid=0debeb&_nc_ohc=JhlVHKDWtvYAX9lOIFv&_nc_ht=scontent.ftlv8-1.fna&oh=3f48be947c5fdea4978b9bee29f37d85&oe=6004C447',
        'Классический, горько-сладкий и крепкий.\n\nДжин\nКампари\nКрасный вермут','140','86'),
        ('68','Негрони твисты','Peach negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127042619_167566398433763_6362628151006800018_o.jpg?_nc_cat=110&ccb=2&_nc_sid=0debeb&_nc_ohc=vZvf_0F_acYAX9x_Lux&_nc_ht=scontent.ftlv8-1.fna&oh=93845c731bcfb8a31834f02bbbbd6096&oe=60079079',
        'Горький, крепкий, с фруктовым послевкусием.\n\nДжин настоянный на персиках\nКампари\n','140','86'),
        ('69','Негрони твисты','White negroni','https://scontent.ftlv8-1.fna.fbcdn.net/v/t1.0-9/127021870_167566891767047_2595835501233676947_o.jpg?_nc_cat=103&ccb=2&_nc_sid=0debeb&_nc_ohc=E5M6_G9L7PsAX9xBLFq&_nc_ht=scontent.ftlv8-1.fna&oh=5a0ad18928e09b50afa8464f9250bd63&oe=6006DD79',
        'Цветочно-горький, сладковатый и крепкий.\n\nФранцузкий джин\nСьюз\nЛилет бланк','140','86')

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