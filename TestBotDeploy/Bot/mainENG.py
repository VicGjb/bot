import configure
import asyncio
import urllib

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import time
import datetime

from base import up_cocktail
from base import init_user
from base import add_user
from base import add_name
from base import up_name
from base import add_phone
from base import up_phone
from base import add_addres
from base import up_addres
from base import add_order
from base import up_order
from base import add_ord
from base import get_ord
from base import up_cocktail_type
from base import up_users
from base import update_users
 
from beautifultable import BeautifulTable

bot=Bot(configure.config['token'])
client=Dispatcher(bot, storage=MemoryStorage())
#-----constant--------------------------------------
global temp_call
temp_call=' '

global users
users={}
key = init_user(conn='')
for id in key:
    i=id['user_id']
    t_id=i
    t_basket=f'{i}_basket'
    t_cocktail_menu=f'{i}_cocktail_menu'
    t_person=f'{i}_person'
    t_call=f'{i}_call'
    t_orders=f'{i}_last_orders'
    t_language=f'{i}_lang'
    users.update({t_id:'',t_basket:'',t_cocktail_menu:'',t_call:'',t_orders:'',t_language:''})


global type_cocktail
type_cocktail=up_cocktail_type(conn='')


global cocktail_menu
cocktail_menu=up_cocktail(conn='')

global person
temp_all_users=up_users(conn='')
person=BeautifulTable()
person.columns.header=['user_id','name','phone','addres','ord']
for user in temp_all_users:
    user_id=user[0]
    name=user[1]
    phone=user[2]
    addres=user[3]
    ord=user[4]
    person.rows.append([user_id,name, phone, addres, ord],f'{user_id}')

global all_orders
temp_all_orders=get_ord(conn='')
all_orders=BeautifulTable()
all_orders.columns.header=['user_id','time','order']
for order in temp_all_orders:
    all_orders.rows.append(order,header=f'{order[0]}')

global time_to_close
time_to_close = 16

url_types={
           'Signature Cocktails':'https://github.com/VicGjb/testbot/blob/main/sing_ENG.jpg?raw=true',
           'Classic Coktails':'https://github.com/VicGjb/testbot/blob/main/classic_ENG.jpg?raw=true',
           'Gin&Tonic':'https://github.com/VicGjb/testbot/blob/main/g&t_ENG.jpg?raw=true',
           'Spritz':'https://github.com/VicGjb/testbot/blob/main/Aperol_ENG.jpg?raw=true',
           'Negronis':'https://github.com/VicGjb/testbot/blob/main/negroni_ENG.jpg?raw=true',
           
           'Авторские коктейли':'https://github.com/VicGjb/testbot/blob/main/sign_RUS.jpg?raw=true',
           'Классические коктейли':'https://github.com/VicGjb/testbot/blob/main/classic_RUS.jpg?raw=true',
           'Джин и тоник':'https://github.com/VicGjb/testbot/blob/main/g&t_RUS.jpg?raw=true',
           'Апероль спритц твисты':'https://github.com/VicGjb/testbot/blob/main/aperol_RUS.jpg?raw=true',
           'Негрони твисты':'https://github.com/VicGjb/testbot/blob/main/negroni_RUS.jpg?raw=true',
           
           'קוקטיילים הבית':'https://github.com/VicGjb/testbot/blob/main/sing_HEB.jpg?raw=true',
           'קוקטיילים קלאסיים':'https://github.com/VicGjb/testbot/blob/main/classic_HEB.jpg?raw=true',
           "ג'ין וטוניק":'https://github.com/VicGjb/testbot/blob/main/g&t_HEB.jpg?raw=true',
           'אפרול שפריץ טוויסת':'https://github.com/VicGjb/testbot/blob/main/aperol_HEBjpg.jpg?raw=true',
           'נגרוני טוויסת':'https://github.com/VicGjb/testbot/blob/main/negroni_HEB.jpg?raw=true',

           'logo':'https://github.com/VicGjb/testbot/blob/main/LOGO%20MADE%20BY%20TEL.jpg?raw=true',
           
           'down_keyboard_ENG':'https://github.com/VicGjb/testbot/blob/main/down_keyboard_ENG.jpg?raw=true',
           'down_keyboard_HEB':'https://github.com/VicGjb/testbot/blob/main/down_keyboard_HEB.jpg?raw=true',
           'down_keyboard_RUS':'https://github.com/VicGjb/testbot/blob/main/down_keyboard_RUS.jpg?raw=true'
           
           }

global lang_dict
lang_dict={
            'oops_ENG':"Oops, something is wrong🤭 let's start over, press /start",
            'oops_HEB':'\start אופס, משהוא השתבש 🤭 בוא נתחיל שוב מהתחלה, תלחץ',
            'oops_RUS':'Что-то пошло не так,🤭 начнем с начала, нажмите /start',


            'cocktail_type_message_ENG':"We're happy to offer you this cocktails:",
            'cocktail_type_message_HEB':"נשמח להציע לך  את סוגי המשקאות הבאים:",
            'cocktail_type_message_RUS':"Рады предложить вам следующие виды напитков:",

            'payment_ENG':'On the moment we can suggest these paying methods:\n1. By cash in the moment of delivery.\n2. By BIT system 0533067303.',
            'payment_HEB':'ברגע זה אנו יכולים להציע לך שתי יישומים\n1.תשלום במזומן לשליח \n2.תשלום דרך העברה ב ביט: 0533067303',
            'payment_RUS':'На данный моменты мы можем предложить вам два сопособа оплаты:\n1)Наличными при получении.\n2)Перевод через систему BIT: 0533067303.',

            'empty_card_ENG':"The card is empty, let's choose your cocktails: /menu",
            'empty_card_HEB':'הסל ריק, הגיע הזמן לבחור משהו   /menu',
            'empty_card_RUS':'Корзина пуста, самое время что-нибуть выбрать: /menu',

            'add_info_ENG':'Add personal info',
            'add_info_HEB':'נתחיל את ההזמנה',
            'add_info_RUS':'Оформляем заказ',

            'empty_orders_ENG':"You have no orders yet, it's time to order your first cocktail🍸 press /menu",
            'empty_orders_HEB':' אין לך הזמנות,זה הזמן לעשות את ההזמנה הראשונה שלך🍸 תבחר בתפריט למטה או תלחץ כאן /menu',
            'empty_orders_RUS':'У вас пока нет закзав, самое время сделать ваш первый🍸 выберете меню внизу или нажмите /menu',

            'empty_card_call_ENG':"The card is empty, let's choose your cocktails.",
            'empty_card_call_HEB':'הסל ריק, הגיע הזמן לבחור משהו.',
            'empty_card_call_RUS':'Корзина пуста, самое время что-нибуть выбрать.',

            'purchase_ENG':'⬇️   Buy   ⬇️',
            'purchase_HEB':'⬇️   לקניה   ⬇️',
            'purchase_RUS':'⬇️   Купить   ⬇️',

            'history_orders_ENG':'Your last orders:\n\n',
            'history_orders_HEB':'\nההזמנות האחרונות שלך:\n\n',
            'history_orders_RUS':'Ваши последние заказы:\n\n',

            'else_text_ENG':'Press marked button\n or start over: /start',
            'else_text_HEB':'תבחר משהו בתפריט למטה⤵️\n/start או תלחץ כאן',
            'else_text_RUS':'Выберите что-нибудть в меню:⤵️\n или нажми сюда /start',

            'info_ENG':"We're the team of professional bartenders, who will provide you the best drinks for your joy! \n*Contacts:*\n[Facebook](https://www.facebook.com/coctailexpresstlv)\n[Instagram](https://www.instagram.com/cocktailexpresstlv)\nPhone: 053-306-7303",
            'info_HEB':'אנחנו צוות של ברמנים מקצועיים, אנו מכינים משקאות קלאסיים ומקוריים למצב הרוח שלכם!\nליצירת קשר:\n[Facebook](https://www.facebook.com/coctailexpresstlv)\n[Instagram](https://www.instagram.com/cocktailexpresstlv)\nטלפון: 053-306-7303',
            'info_RUS':'Мы команда профессиональных барменов, готовим классические, и оригинальные напитки для вашего настроения.\n*Контакты:*\n[Facebook](https://www.facebook.com/coctailexpresstlv)\n[Instagram](https://www.instagram.com/cocktailexpresstlv)\nТелефон: 053-306-7303',
            
            'ask_name_ENG':'Enter your name.\nOr press the button "Correct" if your name is: ',
            'ask_name_HEB':'הזן את שמך.\n או תלחץ "נכון" עם שמך הוא: ',
            'ask_name_RUS':'Введите ваше имя.\nЛибо нажмите "Верно" если вас зовут: ',
     
            'ask_phone_ENG':'Enter your phone number.\nOr press the button "Correct" if your phone number is: ',
            'ask_phone_HEB':'הזן מספר טלפון שלך.\nאו תלחץ "נכון" עם המספר טלפון שלך הוא: ',
            'ask_phone_RUS':'Введите ваш номер телефона.\nЛибо нажмите "Верно" если ваш номер: ',

            'ask_address_ENG':'*!!!!! Delivery in Tel Aviv-Jaffa, Ramat-Gan, Givatayim !!!*\n\nEnter your address.\nOr press the button "Correct" if your address is:  ',
            'ask_address_HEB':'*!!! משלוחים לתל אביב יפו, רמת גן וגבעתיים!!!*\n\nהזן את הכתובת.\nאו תלחץ "נכון" עם הכתובת היא:  ',
            'ask_address_RUS':'*!!!Доставки по Тель-Авив-Яффо, Рамат-Ган, Гиватаим!!!*\n\nВведите ваш аддрес.\nЛибо нажмите "Верно" если ваш адрес: ',

            'back_to_card_ENG':'back to cart',
            'back_to_card_HEB':'חוזרים לסל קניות',
            'back_to_card_RUS':'возвращаемся в корзину',

            'non_name_ENG':'Type your name',
            'non_name_HEB':'תכתוב את השם שלך',
            'non_name_RUS':'Напишите ваше имя',

            'non_phone_ENG':'Type your phone number (format 0500000000)',
            'non_phone_HEB':'מספר טלפון רק במספרים',
            'non_phone_RUS':'Введите номер только цифрами',

            'non_address_ENG':'Type address: ',
            'non_address':'תכתוב את הכתובת שלך',
            'non_address':'Введите адрес',

            'send_order_else_ENG':'Press one of the buttons below',
            'send_order_else_HEB':'תבחר אחד מהאופציות למטה',
            'send_order_else_RUS':'Нажмите одну из кнопок ниже',

            'send_order_name_ENG':'Your order:\nName: ',
            'send_order_name_HEB':'הזמנה שלך:\nשם: ',
            'send_order_name_RUS':'Ваш закз:\nИмя: ',

            'send_order_phone_ENG':'\nPhone:',
            'send_order_phone_HEB':'\nטלפון:  ',
            'send_order_phone_RUS':'\nТелефон: ',

            'send_order_address_ENG':'\nAddress:',
            'send_order_address_HEB':'\nכתובת: ',
            'send_order_address_RUS':'\nАдрес: ',

            'send_order_total_ENG':'\nTotal:',
            'send_order_total_HEB':'\nסה"כ  לתשלום: ',
            'send_order_total_RUS':'\nВсего: ',

            'tnx_ENG':'Thank you for your order!\nThe package will be delivered today from 20:00 to 23:00',
            'tnx_HEB':'תודה על הזמנתך\nהזמנה תגיעי היום בין השעות 20:00-23:00',
            'tnx_RUS':'Спасибо за заказ!\nДоставим сегодня вечером с 20:00 до 23:00',

            'tnx_next_day_ENG':'Thank you for your order!\nThe package will be delivered tomorrow from 20:00 to 23:00',
            'tnx_next_day_HEB':'תודה על הזמנתך\nהזמנה תגיעי מחר בין השעות 20:00-23:00',
            'tnx_next_day_RUS':'Спасибо за заказ!\nДоставим завтра вечером с 20:00 до 23:00',

            'added_in_card_ENG':' is in the card',
            'added_in_card_HEB':'  הוסף לסל',
            'added_in_card_RUS':' добавлен в корзину',
            
#---------------------------------------------------------------------------------------
            'order_correct_ENG':'✅Correct',
            'order_correct_HEB':'נכון✅',
            'order_correct_RUS':'✅Верно',

            'order_back_ENG':'⬅️Back',
            'order_back_HEB':'חזרה⬅️',
            'order_back_RUS':'⬅️Назад',

            'order_cancel_ENG':'⛔️Cancel',
            'order_cancel_HEB':'ביטול⛔️',
            'order_cancel_RUS':'⛔️Отменить',

            'send_order_ENG':'✅Send Order',
            'send_order_HEB':'לעשות הזמנה✅',
            'send_order_RUS':'✅Заказать',

            'sand_order_back_ENG':'⬅️Back',
            'sand_order_back_HEB':'חזרה⬅️',
            'sand_order_back_RUS':'⬅️Назад',
#-------------------------------------------
            'trade_buy05_ENG':'🛍0.5L',
            'trade_buy05_HEB':'ל0.5🛍',
            'trade_buy05_RUS':'🛍0.5L',

            'trade_buy03_ENG':'🛍0.3L',
            'trade_buy03_HEB':'ל0.3🛍',
            'trade_buy03_RUS':'🛍0.3L',

            'trade_card_ENG':'🛒Go to Card',
            'trade_card_HEB':'לסל🛒',
            'trade_card_RUS':'🛒Перейти в корзину',

            'trade_back_ENG':'◀️Back',
            'trade_back_HEB':'חזרה▶️',
            'trade_back_RUS':'⬅️Назад в меню',
#-----------------------------basket---------------------------------------
            'basket_next_ENG':'next ▶️',
            'basket_next_HEB':'◀️הבא',
            'basket_next_RUS':'след.▶️',

            'basket_back_ENG':'◀️prev.',
            'basket_back_HEB':'הקודם▶️',
            'basket_back_RUS':'◀️пред.',

            'basket_start_order_ENG':'✅Make Order',
            'basket_start_order_HEB':'לעבור להזמנה✅',
            'basket_start_order_RUS':'✅Оформить заказ',

            'basket_back_menu_ENG':'🍸Continue Shopping',
            'basket_back_menu_HEB':'לתפריט🍸',
            'basket_back_menu_RUS':'🍸Продолжить покупку',

            'cocktails_name_keyboard_ENG':'◀️Main menu📜',
            'cocktails_name_keyboard_HEB':'📜תפריט ראשי▶️',
            'cocktails_name_keyboard_RUS':'◀️В меню📜',
            }

class MakeOrder(StatesGroup):
    get_name=State()
    get_phone=State()
    get_addres=State()
    make_order=State()
    back_to_card=State()

#-----------------------------------------Static Keybords-----------------------\
#language keyboard
language_keyboard=types.InlineKeyboardMarkup(row_width=1)
eng_language=types.InlineKeyboardButton(text='🇬🇧ENG🇬🇧', callback_data='ENG')
rus_language=types.InlineKeyboardButton(text='🇮🇱HEB🇮🇱', callback_data='HEB')
heb_language=types.InlineKeyboardButton(text='🇷🇺RUS🇷🇺', callback_data='RUS')
language_keyboard.add(eng_language, rus_language, heb_language)

#message
async def oops_message(chat_id):
    await bot.send_message(chat_id, text=lang_dict[f'oops_ENG'])

async def oops_edit_message(chat_id, message_id, lang):
    cocktailkeyboard=await cocktail_type_keyboard(lang='ENG')
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, reply_markup=cocktailkeyboard,text=lang_dict[f'cocktail_type_message_{lang}'])

#maine keyboard reply
async def main_keyboard_down(lang):
    if lang=='ENG':
        mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        menubutton = types.KeyboardButton ('🍴Menu🍴') 
        basketbutton = types.KeyboardButton('🛒Card🛒')
        aboutus = types.KeyboardButton('💁🏻‍♀️Info💁🏻‍♀️')
        orders = types.KeyboardButton('🧳Orders🧳')
        payment = types.KeyboardButton('💰Payment options💰') 
        language_button=types.KeyboardButton('Change language 🇮🇱 🇬🇧 🇷🇺')
        mainkeyboard.add(menubutton, basketbutton, aboutus, orders, language_button, payment)
        #mainkeyboard.row(language_button)
        return mainkeyboard
    if lang=='RUS':
        mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        menubutton = types.KeyboardButton ('🍴Меню🍴') 
        basketbutton = types.KeyboardButton('🛒Корзина🛒')
        aboutus = types.KeyboardButton('💁🏻‍♀️Контакты💁🏻‍♀️')
        orders = types.KeyboardButton('🧳Заказы🧳')
        payment = types.KeyboardButton('💰Способы оплаты💰') 
        language_button=types.KeyboardButton('Поменять язык 🇮🇱 🇬🇧 🇷🇺')
        mainkeyboard.add(menubutton, basketbutton, aboutus, orders,language_button, payment)
       # mainkeyboard.row(language_button)
        return mainkeyboard
    if lang == 'HEB':
        mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        menubutton = types.KeyboardButton ('🍴תפריט🍴') 
        basketbutton = types.KeyboardButton('🛒סל קניות🛒')
        aboutus = types.KeyboardButton('💁🏻‍♀️עלינו💁🏻‍♀️')
        orders = types.KeyboardButton('🧳הזמנות🧳')
        payment = types.KeyboardButton('💰דרכי תשלום💰') 
        language_button=types.KeyboardButton('🇮🇱 🇬🇧 🇷🇺 שנה שפה')
        mainkeyboard.add(menubutton, basketbutton, aboutus, orders, language_button, payment)
       # mainkeyboard.row(language_button)
        return mainkeyboard

#coctailmenu
async def cocktail_type_keyboard(lang):
    cocktailkeyboard=types.InlineKeyboardMarkup(row_width=1)
    if lang=='ENG':
        sign_type=types.InlineKeyboardButton(text='🍹Signature Cocktails🍹', callback_data='Signature Cocktails')
        classic_type=types.InlineKeyboardButton(text='🍸Classic Coktails🍸',callback_data='Classic Coktails')
        g_t_type=types.InlineKeyboardButton(text='🍋Gin&Tonic🍋',callback_data='Gin&Tonic')
        spritzs_type=types.InlineKeyboardButton(text='🍾Aperol Spritz Twists🍊',callback_data='Spritz')
        negroni_type=types.InlineKeyboardButton(text='🥃Negroni Twists🍊',callback_data='Negronis')
        cocktailkeyboard.add(spritzs_type, g_t_type, classic_type, sign_type, negroni_type)
        return cocktailkeyboard

    elif lang=='RUS':
        sign_type=types.InlineKeyboardButton(text='🍹Авторские коктейли🍹', callback_data='Авторские коктейли')
        classic_type=types.InlineKeyboardButton(text='🍸Классические коктейли🍸',callback_data='Классические коктейли')
        g_t_type=types.InlineKeyboardButton(text='🍋Джин и тоник🍋',callback_data='Джин и тоник')
        spritzs_type=types.InlineKeyboardButton(text='🍾Апероль спритц твисты🍊',callback_data='Апероль спритц твисты')
        negroni_type=types.InlineKeyboardButton(text='🥃Негрони твисты🍊',callback_data='Негрони твисты')
        cocktailkeyboard.add(spritzs_type, g_t_type, classic_type, sign_type, negroni_type)
        return cocktailkeyboard

    if lang=='HEB':
        sign_type=types.InlineKeyboardButton(text='🍹קוקטיילים הבית🍹', callback_data='קוקטיילים הבית')
        classic_type=types.InlineKeyboardButton(text='🍸קוקטיילים קלאסיים🍸',callback_data='קוקטיילים קלאסיים')
        g_t_type=types.InlineKeyboardButton(text="🍋ג'ין וטוניק🍋",callback_data="ג'ין וטוניק")
        spritzs_type=types.InlineKeyboardButton(text='🍾אפרול שפריץ טוויסת🍊',callback_data='אפרול שפריץ טוויסת')
        negroni_type=types.InlineKeyboardButton(text='🥃נגרוני טוויסת🍊',callback_data='נגרוני טוויסת')
        cocktailkeyboard.add(spritzs_type, g_t_type, classic_type, sign_type, negroni_type)
        return cocktailkeyboard

#order keyboard reply
async def keyboard_for_order(lang):
    keyboard_for_order=types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=2,one_time_keyboard=True) 
    correct = types.KeyboardButton (lang_dict[f'order_correct_{lang}']) 
    back_in_order=types.KeyboardButton(lang_dict[f'order_back_{lang}'])
    cancel=types.KeyboardButton(lang_dict[f'order_cancel_{lang}'])
    if lang=='HEB':
        keyboard_for_order.add(back_in_order,correct,cancel)
        return keyboard_for_order
    else:
        keyboard_for_order.add(correct,back_in_order,cancel)
        return keyboard_for_order

#send order keyboard
async def send_order_keyboard(lang):
    last_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=2,one_time_keyboard=True)
    make_order=types.KeyboardButton(lang_dict[f'send_order_{lang}'])
    back_in_order=types.KeyboardButton(lang_dict[f'sand_order_back_{lang}'])
    if lang=='HEB':
        last_keyboard.add(back_in_order, make_order)
        return last_keyboard
    else:
        last_keyboard.add(make_order, back_in_order)
        return last_keyboard

#-----------function for operation in menu-------------------------------------\
#keyboard for coctails in menu
async def keyboard(price05,price03,cocktail_name,tip,lang):
    trade_keyboard=types.InlineKeyboardMarkup(row_width=2)
    text_half_l=lang_dict[f'trade_buy05_{lang}']
    text_thirt_l=lang_dict[f'trade_buy03_{lang}']

    text_for_purchase=types.InlineKeyboardButton (text=lang_dict[f'purchase_{lang}'], callback_data='nts')
    half_litr=types.InlineKeyboardButton (text=f'{text_half_l}\n {price05}₪', callback_data=f'0.5L {cocktail_name}')
    thirt_litr=types.InlineKeyboardButton(text=f'{text_thirt_l}\n {price03}₪', callback_data=f'0.3L {cocktail_name}')
    basket=types.InlineKeyboardButton(text=lang_dict[f'trade_card_{lang}'], callback_data='basket')
    go_to_menu=types.InlineKeyboardButton(text=lang_dict[f'trade_back_{lang}'], callback_data=f'{tip}')
    if lang=='HEB':
        trade_keyboard.row(text_for_purchase)
        trade_keyboard.add(thirt_litr, half_litr, basket)
    else:
        trade_keyboard.row(text_for_purchase)  
        trade_keyboard.add(half_litr, thirt_litr, basket)       
    trade_keyboard.row(go_to_menu)
    return trade_keyboard

async def create_keybord_for_coctails_in_type (tip,call,lang):
    try:
        type_keyboard=types.InlineKeyboardMarkup(row_width=1)
        print(tip)
        
        for cocktail in users[f'{call.message.chat.id}_cocktail']:
            if cocktail[1]==tip:
                cocktail_name=cocktail['name']
                print(f'Im here!!!!{cocktail_name}')
                if cocktail['type']==tip:
                    cocktail_name=cocktail['name']
                    cocktail_type=cocktail['type']
                    cocktail_url=url_types[f'{cocktail_type}']
                    cocktail_description = cocktail['description']
                   
                    text=f'[{cocktail_type}]({cocktail_url})'  
                    button=types.InlineKeyboardButton(text=f'{cocktail_name}',callback_data=f'{cocktail_name}')
                    type_keyboard.add(button) 
                    
        main_menu=types.InlineKeyboardButton(text=lang_dict[f'cocktails_name_keyboard_{lang}'],callback_data='main')
        type_keyboard.add(main_menu)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=type_keyboard, parse_mode='Markdown')
    except NameError:# KeyError:  
        await oops_message(chat_id=call.message.chat.id)
    except KeyError:
        await oops_message(chat_id=call.message.chat.id)


async  def show_cocktail(call,tip):
    try:
        print('Показать коктейли')
        for cocktail in  users[f'{call.message.chat.id}_cocktail']:
            if cocktail[1]==tip:
                name=cocktail['name']
               
                if call.data==name:
                    url=cocktail['url_photo']      
                    cocktail_description=cocktail['description']
                    cocktail_name=cocktail['name']   
                    text=f'[{cocktail_name}]({url})\n{cocktail_description}' 

                    price05=cocktail['price05']
                    price03=cocktail['price03']
                    trade_keyboard= await keyboard(price05, price03, cocktail_name, tip=tip, lang=users[f'{call.message.chat.id}_lang'])
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,\
                                                     text=text, reply_markup=trade_keyboard,parse_mode='Markdown') 
    except KeyError:
        print('!!!!!!!!!!!!!!!!!!!!!Im in show cocktail!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')
        
async def cocktail_size(tip,call):
    try:
        print('размер коктейля')
        print(f'{call} -- {tip}')
        for cocktail in users[f'{call.message.chat.id}_cocktail']:
            if cocktail[1]==tip:
                cocktail_name=cocktail['name']
                name_h=f'0.5L {cocktail_name}'
                name_t=f'0.3L {cocktail_name}'   
                cocktail_photo=cocktail['url_photo']
                price_h=cocktail['price05']
                price_t=cocktail['price03']  
                if call.data == name_h:
                    try:
                        if name_h  in users[f'{call.message.chat.id}_basket'].rows.header:
                            users[f'{call.message.chat.id}_basket'].rows[name_h]['amount']+=1
                            users[f'{call.message.chat.id}_basket'].rows[name_h]['price']+=price_h
                            temp_lang=users[f'{call.message.chat.id}_lang']
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, \
                                                            text=f'{cocktail_name}'+lang_dict[f'added_in_card_{temp_lang}']) 
                        else:
                            temp_lang=users[f'{call.message.chat.id}_lang']          
                            users[f'{call.message.chat.id}_basket'].rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True,\
                                                             text=f'{cocktail_name}'+lang_dict[f'added_in_card_{temp_lang}'])      
                    except AttributeError:
                        print('!!!!!!!!AtE cocktail size!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        await oops_message(chat_id=call.message.chat.id)
                    # except NameError:
                    #     print('!!!!!!!!!!NE cocktail size!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    #     await oops_message(chat_id=call.message.chat.id)
                if call.data == name_t:
                    try:
                        if name_t  in users[f'{call.message.chat.id}_basket'].rows.header:
                            users[f'{call.message.chat.id}_basket'].rows[name_t]['amount']+=1
                            users[f'{call.message.chat.id}_basket'].rows[name_t]['price']+=price_t
                            temp_lang=users[f'{call.message.chat.id}_lang']
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True,\
                                                            text=f'{cocktail_name}'+lang_dict[f'added_in_card_{temp_lang}']) 
                        else:
                            temp_lang=users[f'{call.message.chat.id}_lang']        
                            users[f'{call.message.chat.id}_basket'].rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True,\
                                                             text=f'{cocktail_name}'+lang_dict[f'added_in_card_{temp_lang}']) 
                    except AttributeError:
                        print('atribute error in cocktail size')
                        await oops_message(chat_id=call.message.chat.id)
                    except KeyError:
                        print('name error in cocktail size')
                        await oops_message(chat_id=call.message.chat.id)
    except KeyError:
        print('Im iin coktail size key err last one')
        await oops_message(chat_id=call.message.chat.id)
#------------------------------funtion for operation with cart--------------------------------------------------------\
#keyboard for basket
async def basket_test(count_items,showitem,total,item_price,total_item,lang):

    temp_make_order=lang_dict[f'basket_start_order_{lang}']

    basket_keyboard = types.InlineKeyboardMarkup(row_width=1)
    price_of_item= types.InlineKeyboardButton(text=f'{item_price} ₪ * {count_items}={total_item} ₪',callback_data ='nts')
    more_button = types.InlineKeyboardButton(text = '➕', callback_data='more')
    less_button= types.InlineKeyboardButton(text='➖', callback_data = 'less')
    count_items = types.InlineKeyboardButton(text=f'{count_items}', callback_data = 'nts')
    delete_button = types.InlineKeyboardButton(text='❌', callback_data = 'del')
    next_button = types.InlineKeyboardButton(text=lang_dict[f'basket_next_{lang}'], callback_data= 'next') 
    back_button = types.InlineKeyboardButton(text=lang_dict[f'basket_back_{lang}'], callback_data = 'back')
    showitem_button = types.InlineKeyboardButton(text=f'{showitem}', callback_data='nts')
    start_order = types.InlineKeyboardButton(text=f'{temp_make_order} {total} ₪', callback_data='order')
    back_to_menu = types.InlineKeyboardButton(text=lang_dict[f'basket_back_menu_{lang}'], callback_data='main')

    basket_keyboard.add(price_of_item)
    if lang=='HEB':
        basket_keyboard.row(more_button, count_items, less_button, delete_button)
        basket_keyboard.row(next_button, showitem_button, back_button)
    else:
        basket_keyboard.row(delete_button,less_button,count_items,more_button)    
        basket_keyboard.row(back_button, showitem_button, next_button)
    basket_keyboard.add(start_order,back_to_menu)
    return basket_keyboard

#show basket from Reply keyboard
async def basket_from_message (n, message, lang):
    basketC=f'{message.chat.id}_basket'
    showitem=f'{n+1}/{len(users[basketC].rows)}'
    item=users[f'{message.chat.id}_basket'][n][0]
    total=sum(list(users[f'{message.chat.id}_basket'].columns['price']))
    count_items=users[f'{message.chat.id}_basket'].rows[item]['amount']
    bas_url=users[f'{message.chat.id}_basket'].rows[item]['url']
    name= users[f'{message.chat.id}_basket'].rows[item]['name']
    text=f'*{name}*[_]({bas_url})'  
    item_price=users[f'{message.chat.id}_basket'].rows[item]['price']/count_items
    total_item = count_items*item_price
    basket_keyboard= await basket_test(count_items=count_items,showitem=showitem,total=total,\
                                        item_price=item_price,total_item=total_item, lang=lang)
    await bot.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
   
#show basket from inlain keyboard
async def basket_from_call(n, item, call, lang):
    basketC=f'{call.message.chat.id}_basket'
    showitem=f'{n+1}/{len(users[basketC].rows)}'
    total=sum(list(users[f'{call.message.chat.id}_basket'].columns['price']))
    count_items=users[f'{call.message.chat.id}_basket'].rows[item]['amount']
    bas_url=users[f'{call.message.chat.id}_basket'].rows[item]['url']
    name= users[f'{call.message.chat.id}_basket'].rows[item]['name']
    text=f'*{name}*[_]({bas_url})' 
    item_price=users[f'{call.message.chat.id}_basket'].rows[item]['price']/count_items
    total_item = count_items*item_price
    basket_keyboard=await basket_test(count_items=count_items,showitem=showitem,total=total,\
                                        item_price=item_price,total_item=total_item, lang=lang)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,\
                                text= text,reply_markup=basket_keyboard, parse_mode='Markdown')

async def basket_iter(n,call,lang):
    basketC=f'{call.message.chat.id}_basket'
    item=users[f'{call.message.chat.id}_basket'][n][0]
    showitem=f'{n+1}/{len(users[basketC].rows)}'
    item_price=users[f'{call.message.chat.id}_basket'].rows[item]['price']

    total=sum(list(users[f'{call.message.chat.id}_basket'].columns['price']))
    count_items=users[f'{call.message.chat.id}_basket'].rows[item]['amount']
    bas_url=users[f'{call.message.chat.id}_basket'].rows[item]['url'] 
    name= users[f'{call.message.chat.id}_basket'].rows[item]['name']        
    text=f'{name} [_]({bas_url})'
    item_price=users[f'{call.message.chat.id}_basket'].rows[item]['price']/count_items
    total_item = count_items*item_price
    basket_keyboard=await basket_test(count_items=count_items,showitem=showitem,total=total,\
                                        item_price=item_price,total_item=total_item,lang=lang)
    
    return await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,\
                                        reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

#--------------Functions for custumer initialization---------------------------------------------------------------------------------------\
async def init_customer_from_message(message):
    temp_id=f'{message.chat.id}'
    if message.chat.id in users:
        users[f'{temp_id}_basket']=BeautifulTable()
        users[f'{temp_id}_basket'].columns.header=["name", "url", "amount", "price"]
        users[f'{temp_id}_cocktail']=cocktail_menu
        users[f'{temp_id}_person']=BeautifulTable()
        users[f'{temp_id}_person'].columns.header=['user_id','name','phone','addres','ord']
        personal_info=list(person.rows[f'{temp_id}'])
        users[f'{temp_id}_person'].rows.append(personal_info,header=temp_id)
        users[f'{temp_id}_last_orders']=BeautifulTable()
        users[f'{temp_id}_last_orders'].columns.header=['user_id','time','order']
        for order in range(len(all_orders.rows)):
            if f'{all_orders.rows[order][0]}'==f'{temp_id}':
                t=list(all_orders.rows[order])
                users[f'{temp_id}_last_orders'].rows.append(t ,header=temp_id)
        
      #  print(users[f'{temp_id}_person'])
    else:
        add_user(conn='',user_id=message.chat.id, name=message.from_user.first_name)
        user_id=f'{temp_id}'
        user_basket=f'{temp_id}_basket'
        user_cocktail=f'{temp_id}_cocktail'
        user_person=f'{temp_id}_person'
        user_call=f'{temp_id}_call'
        users.update({user_id:user_id, user_basket:user_basket,user_cocktail:user_cocktail, user_person:user_person, user_call:user_call})
        users[f'{temp_id}_basket']=BeautifulTable()
        users[f'{temp_id}_basket'].columns.header=["name", "url", "amount", "price"]
        users[f'{temp_id}_cocktail']=cocktail_menu
        users[f'{temp_id}_person']=BeautifulTable()
        users[f'{temp_id}_person'].columns.header=['user_id','name','phone','addres','ord']
        users[f'{temp_id}_person'].rows.append((message.chat.id, message.from_user.first_name, 'phone', 'address', 'order'), header=f'{temp_id}')
        person.rows.append((message.chat.id, message.from_user.first_name, 'phone', 'address', 'order'), header=f'{temp_id}') 
        users[f'{temp_id}_last_orders']=BeautifulTable()
        users[f'{temp_id}_last_orders'].columns.header=['user_id','time','order']
        users[f'{temp_id}_last_orders'].rows.header=''
#-----------------------Start of comunication-------------------------------------------------------------------------------------\
#----------------------------Welcome message--------------------------------------------------------------------------------------\
@client.message_handler(commands=['start'])
async def welcome (message):
    #приветствие и основное меню внизу
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('logo.jpg', 'rb')   
   # url='https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
    await bot.send_photo(message.chat.id, img, reply_markup=language_keyboard)  
    await init_customer_from_message(message)

@client.message_handler(commands=['menu'])
async def main_cocktail_menu(message):
    temp_lang=users[f'{message.chat.id}_lang']
    text=lang_dict[f'cocktail_type_message_{temp_lang}']
    cocktailkeyboard=await cocktail_type_keyboard(lang=users[f'{message.chat.id}_lang'])
    await bot.send_message(message.chat.id,text=text, reply_markup=cocktailkeyboard)
#------------------comuticatiom by InlineKeyboard-----------------------------------------------------------------------------------\
@client.callback_query_handler(lambda c: c.data)
async def get_call (call: types.CallbackQuery):

    if call.data=='ENG':
        mainkeyboard=await main_keyboard_down(lang='ENG')
        img_e=open('first_ENG.jpg','rb')
        text="Welcome to the bot of CocktailExpress shop!\nWe're delivering craft cocktails to your homes.\nThe orders are taken every day till 17:00.\
            \nDelivery will be made the same day from 20:00 to 23:00.\n\n*!!!!! Delivery in Tel Aviv-Jaffa, Ramat-Gan, Givatayim !!!*"
        await bot.send_photo(chat_id=call.message.chat.id, photo=img_e, caption=text, reply_markup=mainkeyboard, parse_mode="Markdown")
        # await bot.send_message(chat_id=call.message.chat.id,reply_markup=mainkeyboard,
        #                     text="Welcome to the bot of CocktailExpress shop!\nWe're delivering craft cocktails to your homes.\nThe orders are taken every day till 17:00.\nDelivery will be made the same day from 20:00 to 23:00.")
        users[f'{call.message.chat.id}_lang']='ENG'

    if call.data=='HEB':
        mainkeyboard=await main_keyboard_down(lang='HEB')
        img_h=open('first_HEB.jpg','rb')
        text="ברוכים הבאים לחנות הבוט CocktailExpress!\nאנחנו עושים משלוחים של קראפט קוקטיילים\nטריים ומרעננים עד אליך.\
            \nמקבלים הזמנות כל יום עד השעה 17:00 ההזמנה תגיע\nבאותו היום בין השעות 20:00-23:00.\n\n*!!! משלוחים לתל אביב יפו, רמת גן וגבעתיים!!!*"
        await bot.send_photo(chat_id=call.message.chat.id, photo=img_h, caption=text, reply_markup=mainkeyboard, parse_mode="Markdown")
        users[f'{call.message.chat.id}_lang']='HEB'

    if call.data=='RUS':
        mainkeyboard=await main_keyboard_down(lang='RUS')
        img_r=open('first_RUS.jpg','rb')
        text="Вас приветсвует бот-магазин CocktailExpress!\nМы достовляем к вам свежие, крафтовые коктейли.\nЗаказы принимаеются каждый день до 17:00.\
            \nДоставляем в тот же день с 20:00 до 23:00.\n\n*!!!Доставки по Тель-Авив-Яффо, Рамат-Ган, Гиватаим!!!*"
        await bot.send_photo(chat_id=call.message.chat.id, photo=img_r, caption=text, reply_markup=mainkeyboard, parse_mode="Markdown")
        users[f'{call.message.chat.id}_lang']='RUS'
#------------------------------------------------------------------------------------------------------------------

    if call.data =='menu':
        temp_lang=users[f'{call.message.chat.id}_lang']
        text=lang_dict[f'cocktail_type_message_{temp_lang}']
        cocktailkeyboard=await cocktail_type_keyboard(lang=users[f'{call.message.chat.id}_lang'])
        await bot.edit_message_text(call.message.chat.id, message_id=call.message.message.id, text=text, reply_markup=cocktailkeyboard)
    
    if call.data=='main':
        try:
            temp_lang=users[f'{call.message.chat.id}_lang']
            text=lang_dict[f'cocktail_type_message_{temp_lang}']
            cocktailkeyboard=await cocktail_type_keyboard(lang=users[f'{call.message.chat.id}_lang'])
            #await bot.send_message(call.message.chat.id,text=text, reply_markup=cocktailkeyboard)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=cocktailkeyboard)
        except KeyError:
            await oops_message(chat_id=call.message.chat.id)
    users[call.message.chat.id]=False
    for tip in type_cocktail:
        print(tip)
        if call.data==tip[0]:
            try:

                await create_keybord_for_coctails_in_type(tip=tip[0], call=call, lang=users[f'{call.message.chat.id}_lang'])
                users[f'{call.message.chat.id}_call']=call.data
                users[call.message.chat.id]=True  
            except KeyError:
                await oops_message(chat_id=call.message.chat.id)

    print(users[call.message.chat.id]) 
    if f'{call.message.chat.id}_call' in users:

        if users[call.message.chat.id]==False:
            print(f'{call.data} Я сноваа здесь')
            try:
                # if f'{call.message.chat.id}_call' in users:
                await show_cocktail(call=call, tip=users[f'{call.message.chat.id}_call']) 
                await cocktail_size(tip=users[f'{call.message.chat.id}_call'], call=call)
            except  KeyError:
                print('hey im key error in call cocktail menu')
    else:
        pass
#         #-----------------------Baskect-----------------------------------------------------------------------------------------------\
    
    if call.data == 'basket':
        try:
            if len(users[f'{call.message.chat.id}_basket'].rows)==0:
                temp_lang=users[f'{call.message.chat.id}_lang']
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=lang_dict[f'empty_card_call_{temp_lang}'])   
            else: 
                global n
                n=0
                item=users[f'{call.message.chat.id}_basket'][n][0]
                await basket_from_call(n=n, item=item, call=call, lang=users[f'{call.message.chat.id}_lang'])
        except AttributeError:
            
            print('i am AtributeError im in basket call')    

    if call.data == 'next':
        try:
            n+=1
            if n>len(users[f'{call.message.chat.id}_basket'].rows)-1:
                n-=1
                await basket_iter(n=n,call=call, lang=users[f'{call.message.chat.id}_lang'])
            else:
                await basket_iter(n=n,call=call, lang=users[f'{call.message.chat.id}_lang'])
        except NameError:
            print('im Name error in next')
            if f'{call.message.chat.id}_call' in users:
                pass
            else:     
                await oops_message(chat_id=call.message.chat.id)
    if call.data == 'back':  
        try:
            n=n-1
            if n<0:
                n+=1
                await basket_iter(n=n,call=call, lang=users[f'{call.message.chat.id}_lang'])
            else:
                await basket_iter(n=n,call=call, lang=users[f'{call.message.chat.id}_lang'])      
        except NameError:
            print('I am NemeError in back')

    if call.data=='more':
        try:
            item=users[f'{call.message.chat.id}_basket'][n][0]
            users[f'{call.message.chat.id}_basket'].rows[item]['price']+=users[f'{call.message.chat.id}_basket'].rows[item]['price']/users[f'{call.message.chat.id}_basket'].rows[item]['amount']
            users[f'{call.message.chat.id}_basket'].rows[item]['amount']+=1
            await basket_from_call(n=n, item=item, call=call, lang=users[f'{call.message.chat.id}_lang'])
        except NameError:
            print('im Name Error in more')

    if call.data=='less':
        try:
            item=users[f'{call.message.chat.id}_basket'][n][0]
            price_item=users[f'{call.message.chat.id}_basket'].rows[item]['price']/users[f'{call.message.chat.id}_basket'].rows[item]['amount']
            users[f'{call.message.chat.id}_basket'].rows[item]['amount']-=1
            if users[f'{call.message.chat.id}_basket'].rows[item]['amount']==0:
                users[f'{call.message.chat.id}_basket'].rows[item]['amount']+=1
                users[f'{call.message.chat.id}_basket'].rows[item]['price']+=price_item
            users[f'{call.message.chat.id}_basket'].rows[item]['price']-=price_item
            await basket_from_call(n=n, item=item, call=call, lang=users[f'{call.message.chat.id}_lang'])   
        except NameError:
            print('im Name Error in less')

    if call.data =='del':
        try:
            del users[f'{call.message.chat.id}_basket'].rows[n]
            if len(users[f'{call.message.chat.id}_basket'].rows)==0:
                await oops_edit_message(chat_id=call.message.chat.id, message_id=call.message.message_id, lang=users[f'{call.message.chat.id}_lang'])
            else:
                if n==len(users[f'{call.message.chat.id}_basket'].rows):
                    n-=1   
                item=users[f'{call.message.chat.id}_basket'][n][0]
                await basket_from_call(n=n, item=item, call=call, lang=users[f'{call.message.chat.id}_lang'])
        except AttributeError:
            print('im Name Error in del')

    if call.data=='order':
        try:
            temp_lang=users[f'{call.message.chat.id}_lang']
            url=url_types[f'down_keyboard_{temp_lang}']
            temp_add_info=lang_dict[f'add_info_{temp_lang}']
            text=f'[{temp_add_info}]({url})'
            name=users[f'{call.message.chat.id}_person'].columns['name'][f'{call.message.chat.id}']
            await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                        text=text, parse_mode="MarKdown")
            keyboard_order=await keyboard_for_order(lang=temp_lang)
            await bot.send_message(chat_id=call.message.chat.id, text=lang_dict[f'ask_name_{temp_lang}']+f'{name}', reply_markup=keyboard_order)
            await MakeOrder.get_name.set()
        except NameError:#AttributeError:#NameError: #AttributeError:
            await oops_message(chat_id=call.message.chat.id)
            print(' im name error in order call')

# #---------------comutication by ReplyKeyboard------------------------------------------------------------------------------------------------------\
@client.message_handler(content_types = ['text'])
async def get_text(message):
    temp_lang=users[f'{message.chat.id}_lang']
    if message.text=='🍴Menu🍴' or message.text=='🍴Меню🍴' or message.text=='🍴תפריט🍴':
        try:            
            text=lang_dict[f'cocktail_type_message_{temp_lang}']
            cocktailkeyboard=await cocktail_type_keyboard(lang=users[f'{message.chat.id}_lang'])
            await bot.send_message(message.chat.id,text=text, reply_markup= cocktailkeyboard)
        except KeyError:
            await oops_message(chat_id=message.chat.id)

    elif message.text=='🛒Card🛒' or message.text=='🛒Корзина🛒' or message.text=='🛒סל קניות🛒':
        try:           
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_card_{temp_lang}'])    
            else: 
                global n
                n=0
                await basket_from_message(n=n,message=message, lang=users[f'{message.chat.id}_lang'])
        except AttributeError:
            print('im AtrErorr in card by message')
            await oops_message(chat_id=message.chat.id)
        except NameError:
            print('im Name errorin card by message')
            await oops_message(chat_id=message.chat.id,)  
        except KeyError:
            print('im KeyError in card by message')
            await oops_message(chat_id=message.chat.id)


    elif message.text=='💁🏻‍♀️Info💁🏻‍♀️' or message.text=='💁🏻‍♀️Контакты💁🏻‍♀️' or message.text=='💁🏻‍♀️עלינו💁🏻‍♀️':
        # # url='https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/51087951_2681893448493125_7010877500414754816_o.jpg?_nc_cat=107&ccb=2&_nc_sid=174925&_nc_ohc=Uz2V7AhAKHYAX9Aim7s&_nc_ht=scontent.ftlv1-1.fna&oh=bbfd3f8d62f3a8430b1d5cf45b3afaff&oe=602DFFE5'
        # # chris= open('chris.jpg','wb')
        # # chris.write(urllib.request.urlopen(url).read())
        # chris.close()
        try:

            chris=open('chris.jpg','rb')
            await bot.send_photo(message.chat.id, chris)
            await bot.send_message(message.chat.id, text=lang_dict[f'info_{temp_lang}'], parse_mode='Markdown',disable_web_page_preview=True)
        except KeyError:
            await bot.send_message(message.chat.id, text="[Facebook](https://www.facebook.com/coctailexpresstlv)\n[Instagram](https://www.instagram.com/cocktailexpresstlv)\nPhone: 053-306-7303", parse_mode='Markdown',disable_web_page_preview=True)

    elif message.text=='🧳Orders🧳' or message.text=='🧳Заказы🧳' or message.text=='🧳הזמנות🧳':
        try:
            text=''
            if len(users[f'{message.chat.id}_last_orders'])==0:
                mainkeyboard=await main_keyboard_down(lang=temp_lang)
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_order_{temp_lang}'],reply_markup=mainkeyboard)
            else:
                if len(users[f'{message.chat.id}_last_orders'].rows) <=5:
    
                    for i in range (len(users[f'{message.chat.id}_last_orders'].rows)):
                            time=users[f'{message.chat.id}_last_orders'].rows[i]['time']
                            order=users[f'{message.chat.id}_last_orders'].rows[i]['order']
                            text=text + (f'{time} \n{order}\n--------------------\n')
                else:
                    for i in range (5):
                            time=users[f'{message.chat.id}_last_orders'].rows[i]['time']
                            order=users[f'{message.chat.id}_last_orders'].rows[i]['order']
                            text=text + (f'{time} \n{order}\n--------------------\n')
                mainkeyboard=await main_keyboard_down(lang=temp_lang)

                await bot.send_message(message.chat.id, text=lang_dict[f'history_orders_{temp_lang}']+f'{text}\n',reply_markup=mainkeyboard) 
        except KeyError:
            print('KeyError in orders') 
            try:
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_orders_{temp_lang}']) 
            except KeyError:
                await oops_message(chat_id=message.chat.id)
  
    elif message.text=='Change language 🇮🇱 🇬🇧 🇷🇺' or message.text=='Поменять язык 🇮🇱 🇬🇧 🇷🇺' or message.text=='🇮🇱 🇬🇧 🇷🇺 שנה שפה':
        
        logo=open('logo.jpg','rb')        
        await bot.send_photo(message.chat.id, logo, reply_markup=language_keyboard)

    elif message.text=='💰Payment options💰' or message.text=='💰Способы оплаты💰' or message.text=='💰דרכי תשלום💰':
        try:
            await bot.send_message(message.chat.id, text=lang_dict[f'payment_{temp_lang}'])
        except KeyError:
            print('KeyError in about payments')
            await oops_message(chat_id=message.chat.id)
    else:
        try:
            mainkeyboard=await main_keyboard_down(lang=temp_lang)
            await bot.send_message(message.chat.id, text=lang_dict[f'else_text_{temp_lang}'], reply_markup=mainkeyboard)
        except KeyError:
            print('im keyError in else get_text')
            await oops_message(chat_id=message.chat.id)

# #--------------Validation and order-------------------------------------------------------------------------------------------------

@client.message_handler(state=MakeOrder.get_name, content_types=types.ContentTypes.TEXT)
async def get_name(message, state:FSMContext):
    try:
        temp_lang=users[f'{message.chat.id}_lang']
        if message.text == "✅Correct" or message.text=='✅Верно'  or message.text=='נכון✅':
            phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
            keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
            temp_lang=users[f'{message.chat.id}_lang']
            await bot.send_message(message.chat.id, text=lang_dict['ask_phone_'+users[f'{message.chat.id}_lang']]+f'{phone}', reply_markup=keyboard_order)
            await MakeOrder.get_phone.set()
        
        elif message.text=='⬅️Back' or message.text=='⬅️Назад' or message.text=='חזרה⬅️':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_card_{temp_lang}'])    
            else:
                mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang']) 
                await bot.send_message(message.chat.id, text=lang_dict[f'back_to_card_{temp_lang}'], reply_markup=mainkeyboard)
                await basket_from_message(n=n, message=message, lang=users[f'{message.chat.id}_lang'])
        
        elif message.text == '⛔️Cancel' or message.text=='⛔️Отменить' or message.text=='ביטול⛔️':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_card_{temp_lang}'])    
            else: 
                mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=lang_dict[f'back_to_card_{temp_lang}'], reply_markup=mainkeyboard)
                await basket_from_message(n=n, message=message, lang=users[f'{message.chat.id}_lang'])
        
        elif message.text=='/start':
            await bot.send_chat_action(message.chat.id, 'upload_photo')
            img = open('logo.jpg', 'rb')   
            await bot.send_photo(message.chat.id, img, reply_markup=language_keyboard)  
            await init_customer_from_message(message)
            await state.finish()

        else:
            if message.text == None:
                message.text='Name'
                await bot.send_message(message.chat.id, text=lang_dict[f'none_name_{temp_lang}'])
                await MakeOrder.get_name.set()
            else:
                users[f'{message.chat.id}_person'].rows[f'{message.chat.id}']['name']=f'{message.text}'
                phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
                keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=lang_dict[f'ask_phone_{temp_lang}']+f'{phone}',reply_markup=keyboard_order)
                await MakeOrder.get_phone.set()

    except AttributeError: #NameError: #AttributeError:
            print('AtrError in get_name')
            await oops_message(chat_id= message.chat.id)

@client.message_handler(state=MakeOrder.get_phone, content_types=types.ContentTypes.TEXT)   
async def get_phone (message, state:FSMContext):
    try:
        temp_lang=users[f'{message.chat.id}_lang']
        if message.text == '✅Correct' or message.text=='✅Верно'  or message.text=='נכון✅':
            if users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}'] == None:
                await bot.send_message(message.chat.id, text=lang_dict[f'non_phone_{temp_lang}'])
                await MakeOrder.get_phone.set()

            elif users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}'].isdigit():

                addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
                keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=lang_dict[f'ask_address_{temp_lang}']+f'{addres}',reply_markup=keyboard_order, parse_mode="Markdown")
                await MakeOrder.get_addres.set()
            else:
                await bot.send_message(message.chat.id, text=lang_dict[f'non_phone_{temp_lang}'])
                await MakeOrder.get_phone.set()
        
        elif message.text=='⬅️Back' or message.text=='⬅️Назад' or message.text=='חזרה⬅️':
            name=users[f'{message.chat.id}_person'].columns['name'][f'{message.chat.id}']
            keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
            await bot.send_message(message.chat.id, text=lang_dict[f'ask_name_{temp_lang}']+f'{name}', reply_markup=keyboard_order)
            await MakeOrder.get_name.set()
        
        elif message.text == '⛔️Cancel' or message.text=='⛔️Отменить' or message.text=='ביטול⛔️':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_card_{temp_lang}'])    
            else: 
                mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=lang_dict[f'back_to_card_{temp_lang}'], reply_markup=mainkeyboard)
                await basket_from_message(n=n, message=message, lang=users[f'{message.chat.id}_lang'])
        
        elif message.text=='/start':
            await bot.send_chat_action(message.chat.id, 'upload_photo')
            img = open('logo.jpg', 'rb')   
            await bot.send_photo(message.chat.id, img, reply_markup=language_keyboard)  
            await init_customer_from_message(message)
            await state.finish()

        else:
            if message.text == None:
                await bot.send_message(message.chat.id, text=lang_dict[f'none_phone_{temp_lang}'])
                await MakeOrder.get_phone.set() 
            elif message.text.isdigit():
                users[f'{message.chat.id}_person'].rows[f'{message.chat.id}']['phone']=message.text

                addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
                keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=lang_dict[f'ask_address_{temp_lang}']+f'{addres}',reply_markup=keyboard_order, parse_mode="Markdown")
                await MakeOrder.get_addres.set()             
            else:
                await bot.send_message(message.chat.id, text=lang_dict[f'non_phone_{temp_lang}'])
                await MakeOrder.get_phone.set()
    except NameError:# AttributeError:
            print('im AttrError in get_phone')
            await oops_message(chat_id=message.chat.id)

@client.message_handler(state=MakeOrder.get_addres, content_types=types.ContentTypes.TEXT)
async def get_addres(message, state:FSMContext):
    try:
        temp_lang=users[f'{message.chat.id}_lang']
        if message.text == '✅Correct' or message.text=='✅Верно'  or message.text=='נכון✅':
            order=BeautifulTable()
            order.columns.header=['Name','Amount','Price']
            cocktails=len(users[f'{message.chat.id}_basket'].rows)

            for i in range(cocktails):
                name=users[f'{message.chat.id}_basket'][i]['name']
                amount=users[f'{message.chat.id}_basket'][i]['amount']
                price=users[f'{message.chat.id}_basket'][i]['price']
                order.rows.append([name, amount, price])
            name=users[f'{message.chat.id}_person'].columns['name'][f'{message.chat.id}']
            phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
            addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
            order.set_style(BeautifulTable.STYLE_COMPACT)
            total=(sum(list(order.columns['Price'])))
            last_keyboard=await send_order_keyboard(lang=users[f'{message.chat.id}_lang'])
            text=lang_dict[f'send_order_name_{temp_lang}']+f'{name}'+lang_dict[f'send_order_phone_{temp_lang}']+f'{phone}'+lang_dict[f'send_order_address_{temp_lang}']+f'{addres}'+lang_dict[f'send_order_total_{temp_lang}']+f'{total}'
            await bot.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
            await MakeOrder.make_order.set()   
        
        elif message.text=='⬅️Back' or message.text=='⬅️Назад' or message.text=='חזרה⬅️':
            phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
            keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
            await bot.send_message(message.chat.id, text=lang_dict[f'ask_phone_{temp_lang}']+f'{phone}',reply_markup=keyboard_order)
            await MakeOrder.get_phone.set()
        
        elif message.text == '⛔️Cancel' or message.text=='⛔️Отменить' or message.text=='ביטול⛔️':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id, text=lang_dict[f'empty_card_{temp_lang}'])    
            else: 
                mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=lang_dict[f'back_to_card_{temp_lang}'], reply_markup=mainkeyboard)
                await basket_from_message(n=n, message=message, lang=users[f'{message.chat.id}_lang'])     

        elif message.text=='/start':
            await bot.send_chat_action(message.chat.id, 'upload_photo')
            img = open('logo.jpg', 'rb')   
            await bot.send_photo(message.chat.id, img, reply_markup=language_keyboard)  
            await init_customer_from_message(message)
            await state.finish()

        else:
            if message.text == None:
                message.text='addres'
                await bot.send_message(message.chat.id, text=lang_dict[f'non_address_{temp_lang}'] )
                await bot.register_next_step_handler(message, get_addres)
            else:
             
                users[f'{message.chat.id}_person'].rows[f'{message.chat.id}']['addres']=message.text
                order=BeautifulTable()
                order.columns.header=['Name','Amount','Price']
                cocktails=len(users[f'{message.chat.id}_basket'].rows)
                for i in range(cocktails):
                    name=users[f'{message.chat.id}_basket'][i]['name']
                    amount=users[f'{message.chat.id}_basket'][i]['amount']
                    price=users[f'{message.chat.id}_basket'][i]['price']
                    order.rows.append([name, amount, price])
                name=users[f'{message.chat.id}_person'].columns['name'][f'{message.chat.id}']
                phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
                addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
                order.set_style(BeautifulTable.STYLE_COMPACT)
                total=(sum(list(order.columns['Price'])))
                text=lang_dict[f'send_order_name_{temp_lang}']+f'{name}'+lang_dict[f'send_order_phone_{temp_lang}']+f'{phone}'+lang_dict[f'send_order_address_{temp_lang}']+f'{addres}'+lang_dict[f'send_order_total_{temp_lang}']+f'{total}'
                #text=f'Your order:\nName: {name}\nPhone:{phone}\nAddress:{addres}\nTotal:{total}'
                print(text)
                last_keyboard=await send_order_keyboard(lang=users[f'{message.chat.id}_lang'])
                await bot.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
                await MakeOrder.make_order.set()
    except AttributeError:
        print('AttError get_address')
        await oops_message(chat_id=message.chat.id)

@client.message_handler(state=MakeOrder.make_order, content_types=types.ContentTypes.TEXT)
async def send_order(message, state:FSMContext):
    await state.finish()
    try:
        temp_lang=users[f'{message.chat.id}_lang']
        if message.text == '✅Send Order' or message.text=='✅Заказать' or message.text=='לעשות הזמנה✅':     
            order=BeautifulTable()
            order.columns.header=['Name','Amount','Price']
            cocktails=len(users[f'{message.chat.id}_basket'].rows)
            for i in range(cocktails):
                name=users[f'{message.chat.id}_basket'][i]['name']
                amount=users[f'{message.chat.id}_basket'][i]['amount']
                price=users[f'{message.chat.id}_basket'][i]['price']
                print(name)
                order.rows.append([name, amount, price])
        
            name=users[f'{message.chat.id}_person'].columns['name'][f'{message.chat.id}']
            phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
            addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
            order.set_style(BeautifulTable.STYLE_COMPACT)
            total=(sum(list(order.columns['Price'])))
            text=lang_dict[f'send_order_name_{temp_lang}']+f'{name}'+lang_dict[f'send_order_phone_{temp_lang}']+f'{phone}'+lang_dict[f'send_order_address_{temp_lang}']+f'{addres}'+lang_dict[f'send_order_total_{temp_lang}']+f'{total}'
            mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang'])
            await bot.send_message(message.chat.id, text=lang_dict[f'payment_{temp_lang}'])

            now_time=int(datetime.datetime.now().strftime("%H"))
            if now_time > time_to_close:
                await bot.send_message (message.chat.id, text=lang_dict[f'tnx_next_day_{temp_lang}'], reply_markup=mainkeyboard)
            else:    
                await bot.send_message(message.chat.id, text=lang_dict[f'tnx_{temp_lang}'], reply_markup=mainkeyboard)
            await bot.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')
          
            print('im finish!!!!!!!!!!!!!!')
              
            update_users(conn='',name=name,phone=phone,addres=addres,ord=text,user_id=message.chat.id)
            add_ord(conn='', user_id=message.chat.id, zakaz=text)
            person.rows[f'{message.chat.id}']=(message.chat.id, name, phone, addres, text)
            tm=time.ctime(time.time())
            all_orders.rows.insert(0,[message.chat.id, tm, text], header=f'{message.chat.id}')
            await init_customer_from_message(message)
        
            print('Now im realy finish!!!!!!')

        elif message.text == '⬅️Back' or message.text=='⬅️Назад' or message.text=='חזרה⬅️':
            addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
            keyboard_order=await keyboard_for_order(lang=users[f'{message.chat.id}_lang'])
            await bot.send_message(message.chat.id, text=lang_dict[f'ask_address_{temp_lang}']+f'{addres}',reply_markup=keyboard_order, parse_mode="Markdown")
            await MakeOrder.get_addres.set()


        elif message.text=='/start':
            await bot.send_chat_action(message.chat.id, 'upload_photo')
            img = open('logo.jpg', 'rb')   
            await bot.send_photo(message.chat.id, img, reply_markup=language_keyboard)  
            await init_customer_from_message(message)
            await state.finish()

        else:
            last_keyboard=await send_order_keyboard(lang=users[f'{message.chat.id}_lang'])
            await bot.send_message(message.chat.id, text=lang_dict[f'send_order_else_{temp_lang}'], reply_markup=last_keyboard)
            await MakeOrder.make_order.set()
        
    except AttributeError:#NameError: 
        print('AttrErr Send_order')
        await oops_message(chat_id=message.chat.id)

#  #-------------------Protection from stupid messages---------------------------------------------------------------------------------   
@client.message_handler(content_types = ['voice'])
async def get_audio(message):
    await bot.send_chat_action(message.chat.id, 'upload_voice')
    aud = open('reqe.ogg', 'rb')   
    await bot.send_voice(chat_id=message.chat.id, voice=aud) 
    mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang'])
    await bot.send_message(message.chat.id, text='You have a pleasant voice.\nNow press here /start', reply_markup=mainkeyboard)

@client.message_handler(content_types = ['photo'])
async def get_photo(message):
    mainkeyboard=await main_keyboard_down(lang=users[f'{message.chat.id}_lang'])
    await bot.send_message(message.chat.id, text="Look what I've got", reply_markup=mainkeyboard)
    await bot.send_chat_action(message.chat.id, 'upload_voice')
    ph = open('siski1.jpg', 'rb')   
    await bot.send_photo(message.chat.id, ph, caption="If you wanna see more /start")      

executor.start_polling(client)
 
# if __name__ =="__main__":