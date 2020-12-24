import configure
import telebot
import urllib
from telebot import types
from telebot import TeleBot
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
from beautifultable import BeautifulTable
import psycopg2
 
#https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B

client=telebot.TeleBot(configure.config['token'])
# app=Flask(__name__)
# sslify=SSLify(app)
global users
users={}
key = init_user(conn='')
print(key)
for id in key:
    t=id['user_id']
    users.update({t:f'{t}_basket'})

#mainekeyboard
mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=False)
menubutton = types.KeyboardButton ('🍴Меню🍴') 
basketbutton = types.KeyboardButton('🛍Корзина🛍')
aboutus = types.KeyboardButton('💁🏻‍♀️О нас💁🏻‍♀️')
orders = types.KeyboardButton('🧳Заказы🧳')
#back = types.KeyboardButton('🍴Вернуться🍴')
mainkeyboard.add(menubutton, basketbutton, aboutus, orders)

#coctailmenu
cocktailkeyboard=types.InlineKeyboardMarkup(row_width=1)
cocktail_map=types.InlineKeyboardButton(text='📜Коктейльное меню📜', callback_data='cocktail_map')
sign_type=types.InlineKeyboardButton(text='🍹Авторские коктейли🍹', callback_data='sig')
classic_type=types.InlineKeyboardButton(text='🍸Классические коктейли🍸',callback_data='clas')
g_t_type=types.InlineKeyboardButton(text='🍋Джин-тоник🍋',callback_data='g_t')
spritzs_type=types.InlineKeyboardButton(text='🍾Сприцы🍊',callback_data='spr')
negroni_type=types.InlineKeyboardButton(text='🥃Негрони🍊',callback_data='neg')
cocktailkeyboard.add(cocktail_map, sign_type, classic_type, g_t_type, spritzs_type, negroni_type)

#order keyboard
keyboard_for_order =types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True) 
correct = types.KeyboardButton ('✅Правильно') 
back_in_order = types.KeyboardButton('⬅️Назад')
cancel = types.KeyboardButton('⛔️Отменить')
keyboard_for_order.add(correct,back_in_order,cancel)

#last_keyboard
last_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=2,one_time_keyboard=True)
make_order=types.KeyboardButton('✅Заказать')
last_keyboard.add(make_order, back_in_order)

#keyboard for coctails
def keyboard(price05,price03,cocktail_name):
    trade_keyboard=types.InlineKeyboardMarkup(row_width=2)
    half_litr = types.InlineKeyboardButton (text=f'0.5L\n {price05}NIS', callback_data=f'0.5L {cocktail_name}')
    thirt_litr = types.InlineKeyboardButton(text=f'0.3L\n {price03}NIS', callback_data=f'0.3L {cocktail_name}')
    basket = types.InlineKeyboardButton(text='🛍Оформить заказ', callback_data='basket')
    go_to_menu = types.InlineKeyboardButton(text='🍸Меню', callback_data='menu')
    trade_keyboard.add(half_litr, thirt_litr, basket)
    trade_keyboard.row(go_to_menu)
    return trade_keyboard

#keyboard for basket
def basket_test(count_items,showitem,total,item_price,total_item):

    basket_keyboard = types.InlineKeyboardMarkup(row_width=1)
    price_of_item= types.InlineKeyboardButton(text=f'{item_price} NIS * {count_items}={total_item} NIS',callback_data ='nts')
    more_button = types.InlineKeyboardButton(text = '➕', callback_data='more')
    less_button= types.InlineKeyboardButton(text='➖', callback_data = 'less')
    count_items = types.InlineKeyboardButton(text=f'{count_items}', callback_data = 'nts')
    delete_button = types.InlineKeyboardButton(text='❌', callback_data = 'del')
    next_button = types.InlineKeyboardButton(text='след.▶️', callback_data= 'next')
    back_button = types.InlineKeyboardButton(text='◀️пред.', callback_data = 'back')
    showitem_button = types.InlineKeyboardButton(text=f'{showitem}', callback_data='nts')
    start_order = types.InlineKeyboardButton(text=f'✅Оформить заказ {total} NIS', callback_data='order')
    back_to_menu = types.InlineKeyboardButton(text='🍸Продолжить покупку', callback_data='main')
    

    basket_keyboard.add(price_of_item)
    basket_keyboard.row(delete_button,less_button,count_items,more_button)
    basket_keyboard.row(back_button, showitem_button, next_button)
    basket_keyboard.add(start_order,back_to_menu)
    return basket_keyboard


def basket_iter(n,call):

    item=users[call.message.chat.id][n][0]
    showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
    item_price=users[call.message.chat.id].rows[item]['price']

    total=sum(list(users[call.message.chat.id].columns['price']))
    count_items=users[call.message.chat.id].rows[item]['amount']
    bas_url=users[call.message.chat.id].rows[item]['url'] 
    name= users[call.message.chat.id].rows[item]['name']        
    text=f'{name} [_]({bas_url})'
    item_price=users[call.message.chat.id].rows[item]['price']/count_items
    total_item = count_items*item_price
    basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)

    return client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

def init_customer_from_message(message):
    if message.chat.id in users:
        users[message.chat.id]=BeautifulTable()
        users[message.chat.id].columns.header=["name", "url", "amount", "price"]
    else:
    # print ('not work')
        add_user(conn='',user_id=message.chat.id, name=message.from_user.first_name)
        key = init_user(conn='')
        for id in key:
            print(id['user_id'])
            t=id['user_id']
            users.update({t:f'{t}_basket'})
        #print (users)
        users[message.chat.id]=BeautifulTable()
        users[message.chat.id].columns.header=["name", "url", "amount", "price"]
        #print(users[message.chat.id])
    return users[message.chat.id]

def init_customer_from_call(call):
    if call.message.chat.id in users:
        users[call.message.chat.id]=BeautifulTable()
        users[call.message.chat.id].columns.header=["name", "url", "amount", "price"]
    else:
        #print ('not work')
        add_user(conn='',user_id=call.message.chat.id, name=call.message.from_user.first_name)
        key = init_user(conn='')
        for id in key:
            t=id['user_id']
            users.update({t:f'{t}_basket'})
        #print (users)
        users[call.message.chat.id]=BeautifulTable()
        users[call.message.chat.id].columns.header=["name", "url", "amount", "price"]
        #print(users[call.message.chat.id])
    return users[call.message.chat.id]

def cocktail_type(tip,call):
    if call.data == tip:
            #init_customer_from_call(call=call)
        m=up_cocktail(conn='',tip=tip)
        for cocktail in m:
            
            addr=cocktail['url_photo']
            pic = open('pic.jpg','wb')
            pic.write(urllib.request.urlopen(addr).read())
            pic.close()
            client.send_chat_action(call.message.chat.id, 'upload_photo')
            pic = open('pic.jpg', 'rb')           
            cocktail_description=cocktail['description']
            cocktail_name=cocktail['name']   
            text=''.join(f'<strong>{cocktail_name}:</strong> \n{cocktail_description}') 
            price05=cocktail['price05']
            price03=cocktail['price03']
            trade_keyboard=keyboard(price05,price03,cocktail_name)
            
            client.send_photo(call.message.chat.id, pic, reply_to_message_id="Б",caption=text,reply_markup=trade_keyboard,parse_mode='HTML')
# print(users)
def cocktail_size(tip,call):
    m=up_cocktail(conn='',tip=tip)
    for cocktail in m:
        cocktail_name=cocktail['name']
        name_h=f'0.5L {cocktail_name}'
        name_t=f'0.3L {cocktail_name}'   
        cocktail_photo=cocktail['url_photo']
        price_h=cocktail['price05']
        price_t=cocktail['price03']  
        if call.data == name_h:
            try:
                #init_customer_from_call(call=call)
                if name_h  in users[call.message.chat.id].rows.header:
                    users[call.message.chat.id].rows[name_h]['amount']+=1
                    users[call.message.chat.id].rows[name_h]['price']+=price_h
                    client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
                
                else:          
                    users[call.message.chat.id].rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
                    client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
                # print(users[call.message.chat.id])
            except AttributeError:
                client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
        if call.data == name_t:
            try:
                #init_customer_from_call(call=call)
                if name_t  in users[call.message.chat.id].rows.header:
                    users[call.message.chat.id].rows[name_t]['amount']+=1
                    users[call.message.chat.id].rows[name_t]['price']+=price_t
                    client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
                
                else:        
                    users[call.message.chat.id].rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
                    client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
            except AttributeError:
                client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')

#----------------------------------------------------------------------------------------------------------------------------#

@client.message_handler(commands=['start'])
def welcome (message):
    #приветствие и основное меню внизу
    
    client.send_chat_action(message.chat.id, 'upload_photo')
    img = open('out.jpg', 'rb')   
    url='https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
    client.send_photo(message.chat.id, img,reply_markup=mainkeyboard)  
    
    init_customer_from_message(message)

@client.callback_query_handler(func = lambda call:True)
def get_call(call):
    if call.data=='menu':
        client.send_message(chat_id=call.message.chat.id,reply_markup=cocktailkeyboard,text='Рады предложить вам, следующие виды напитков:')
    if call.data=='main':
        #init_customer_from_call(call=call)
        client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=cocktailkeyboard,text='Рады предложить вам, следующие виды напитков:')
    if call.data=='cocktail_map':
        map1 = open('for bot.jpg', 'rb') 
        client.send_photo(call.message.chat.id, map1 ,caption='Это наша карта, чтобы приобрести коктейль выберите категорию:',reply_markup=cocktailkeyboard)  

    if call.data =='sig':
        cocktail_type(tip='sig',call=call)
    cocktail_size(tip='sig',call=call)
    
    if call.data =='clas':
        cocktail_type(tip='clas',call=call)
    cocktail_size(tip='clas',call=call)
    
    if call.data =='g_t':
        cocktail_type(tip='g_t',call=call)
    cocktail_size(tip='g_t',call=call)
    
    if call.data =='spr':
        cocktail_type(tip='spr',call=call)
    cocktail_size(tip='spr',call=call)
    
    if call.data =='neg':
        cocktail_type(tip='neg',call=call)
    cocktail_size(tip='neg',call=call)  
    #-----------------------Baskect====================================================================================================
    if call.data == 'basket':
        try:
            if len(users[call.message.chat.id].rows)==0:
                client.send_message(call.message.chat.id, 'Корзина пуста, самое время что-нибуть выбрать: /start')    
            else: 
                global n
                n=0
                showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
                item=users[call.message.chat.id][n][0]
                total=sum(list(users[call.message.chat.id].columns['price']))
                count_items=users[call.message.chat.id].rows[item]['amount']
                bas_url=users[call.message.chat.id].rows[item]['url']
                name= users[call.message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})' 
                item_price=users[call.message.chat.id].rows[item]['price']/count_items
                total_item = count_items*item_price
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
                client.send_message(call.message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
        except AttributeError:
            client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
        
#---------------Basket_iter---------------------------------------------------------------------------------------------=================
    if call.data == 'next':
        try:
            n+=1
            if n>len(users[call.message.chat.id].rows)-1:
                n-=1
                basket_iter(n=n,call=call)
            else:
                basket_iter(n=n,call=call)
        except NameError:
            client.send_message(call.message.chat.id, text= '/start')       

    if call.data == 'back':  
        try:
            n=n-1
            if n<0:
                n+=1
                basket_iter(n=n,call=call)
            else:
                basket_iter(n=n,call=call)      
        except NameError:
            client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
    if call.data=='more':
        try:

            item=users[call.message.chat.id][n][0]
            users[call.message.chat.id].rows[item]['price']+=users[call.message.chat.id].rows[item]['price']/users[call.message.chat.id].rows[item]['amount']
            users[call.message.chat.id].rows[item]['amount']+=1
            showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
            total=sum(list(users[call.message.chat.id].columns['price']))
            count_items=users[call.message.chat.id].rows[item]['amount']
            bas_url=users[call.message.chat.id].rows[item]['url']
            name= users[call.message.chat.id].rows[item]['name']
            
            text=f'*{name}*[_]({bas_url})' 
            item_price=users[call.message.chat.id].rows[item]['price']/count_items
            total_item = count_items*item_price
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

        except NameError:
            client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')


    if call.data=='less':
        try:
            item=users[call.message.chat.id][n][0]
            price_item=users[call.message.chat.id].rows[item]['price']/users[call.message.chat.id].rows[item]['amount']
            users[call.message.chat.id].rows[item]['amount']-=1
            if users[call.message.chat.id].rows[item]['amount']==0:
                users[call.message.chat.id].rows[item]['amount']+=1
                users[call.message.chat.id].rows[item]['price']+=price_item
            users[call.message.chat.id].rows[item]['price']-=price_item
            showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
            total=sum(list(users[call.message.chat.id].columns['price']))
            count_items=users[call.message.chat.id].rows[item]['amount']
            bas_url=users[call.message.chat.id].rows[item]['url']
            name= users[call.message.chat.id].rows[item]['name']
            text=f'*{name}*[_]({bas_url})'  
            item_price=users[call.message.chat.id].rows[item]['price']/count_items
            total_item = count_items*item_price
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')
        except NameError:
            client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')

    if call.data =='del':
        try:
            del users[call.message.chat.id].rows[n]
            if len(users[call.message.chat.id].rows)==0:
                client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=cocktailkeyboard,text='Корзина пуста, выберете что нибудть')
            else:
                if n==len(users[call.message.chat.id].rows):
                    n-=1   
                item=users[call.message.chat.id][n][0]
                showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
                total=sum(list(users[call.message.chat.id].columns['price']))
                count_items=users[call.message.chat.id].rows[item]['amount']
                bas_url=users[call.message.chat.id].rows[item]['url']
                name= users[call.message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})' 
                item_price=users[call.message.chat.id].rows[item]['price']/count_items
                total_item = count_items*item_price
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
                client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')
        except AttributeError:
            client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
    if call.data=='order':
        try:
            name=up_name(conn='', user_id=call.message.chat.id)

            client.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                        text='Начинаем оформлять заказ')
            client.send_message(chat_id=call.message.chat.id, text=f'Как вас зовут?\nCейчас так: {name[0]}', reply_markup=keyboard_for_order)
            client.register_next_step_handler(call.message, get_name)
        except AttributeError:
            client.send_message(call.message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
#---------------------------------------------------------------------------------------------------------------------------------------------
@client.message_handler(content_types = ['text'])
def get_text(message):
    if message.text=='🍴Меню🍴' or message.text=='🍴Вернуться🍴':
        client.send_message(message.chat.id,'Рады предложить вам следующие типы напитков:', reply_markup= cocktailkeyboard)
        init_customer_from_message(message)
    elif message.text == '🛍Корзина🛍':
        try:
                
            if len(users[message.chat.id].rows)==0:
                client.send_message(message.chat.id, 'Корзина пуста, самое время что-нибуть выбрать: /start')    
            else: 
                global n
                n=0
                showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
                item=users[message.chat.id][n][0]
                total=sum(list(users[message.chat.id].columns['price']))
                count_items=users[message.chat.id].rows[item]['amount']
                bas_url=users[message.chat.id].rows[item]['url']
                name= users[message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})' 
                item_price=users[call.message.chat.id].rows[item]['price']/count_items
                total_item = count_items*item_price
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
        except AttributeError:
            client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')   
        except NameError:
            client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')   
        except KeyError:
            client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
    elif message.text == '💁🏻‍♀️О нас💁🏻‍♀️':
        url='https://scontent.fhfa1-1.fna.fbcdn.net/v/t1.0-9/51087951_2681893448493125_7010877500414754816_o.jpg?_nc_cat=107&ccb=2&_nc_sid=174925&_nc_ohc=W5-onSfCwL4AX-gsWKY&_nc_ht=scontent.fhfa1-1.fna&oh=d41c099e79bb84248488f1466a085962&oe=600672E5'
        chris= open('chris.jpg','wb')
        chris.write(urllib.request.urlopen(url).read())
        chris.close()
        chris=open('chris.jpg','rb')
        client.send_photo(message.chat.id, chris)
        text='Мы команда профессиональных барменов, готовим классические, и оригинальные напитки для вашего настроения.\n*Контакты:*\n[Facebook](https://www.facebook.com/coctailexpresstlv)\n[Instagram](https://www.instagram.com/cocktailexpresstlv)\nТелефон: 053-306-7303'
        client.send_message(message.chat.id, text=text, parse_mode='Markdown',disable_web_page_preview=True)
    elif message.text == '🧳Заказы🧳':
        a=get_ord(conn='',user_id=message.chat.id, limit=5)
        text='\n------------\n'.join([f'{m} \n {n}' for m, n in a])
        print(text)
        client.send_message(message.chat.id, text=f'вот ваши последние заказы:\n\n{text}\n',reply_markup=mainkeyboard)
    else:
        client.send_message(message.chat.id,'Выбери что-нибудть там внизу:⤵️\n или нажми сюда /start', reply_markup=mainkeyboard)
#------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_name(message):
    try:
        if message.text == "✅Правильно":
            phone=up_phone(conn='', user_id=message.chat.id)
            client.send_message(message.chat.id, text=f'Ваш телефон\nСейчас: {phone[0]}',reply_markup=keyboard_for_order)
            client.register_next_step_handler(message, get_phone)
        elif message.text=='⬅️Назад':
            if len(users[message.chat.id].rows)==0:
                client.send_message(message.chat.id, 'Корзина пуста, самое время что-нибуть выбрать: /start')    
            else: 
                showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
                item=users[message.chat.id][n][0]
                total=sum(list(users[message.chat.id].columns['price']))
                count_items=users[message.chat.id].rows[item]['amount']
                bas_url=users[message.chat.id].rows[item]['url']
                name= users[message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})'  
                item_price=users[message.chat.id].rows[item]['price']/count_items
                total_item = count_items*item_price
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
                client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
        elif message.text == '⛔️Отменить':
            if len(users[message.chat.id].rows)==0:
                client.send_message(message.chat.id, 'Корзина пуста, самое время что-нибуть выбрать: /start')    
            else: 
                showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
                item=users[message.chat.id][n][0]
                total=sum(list(users[message.chat.id].columns['price']))
                count_items=users[message.chat.id].rows[item]['amount']
                bas_url=users[message.chat.id].rows[item]['url']
                name= users[message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})'           
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
                client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown') 
        else:
            if message.text == None:
                message.text='Name'
                add_name(conn='', name=message.text, user_id=message.chat.id)
                client.send_message(message.chat.id, text= 'Веди имя буквами')
                client.register_next_step_handler(message, get_name)
            else:
                client.clear_step_handler_by_chat_id(chat_id=message.chat.id)
                add_name(conn='',name=message.text, user_id=message.chat.id)
                phone=up_phone(conn='', user_id=message.chat.id)
                client.send_message(message.chat.id, text=f'Ваш телефон\nСейчас: {phone[0]}',reply_markup=keyboard_for_order)
                client.register_next_step_handler(message, get_phone)
    except AttributeError:
            client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
    # finally:
    #         print(message.chat.id)
    #         message.text='debil'
    #         add_name(conn='', name=message.text, user_id=message.chat.id)
    #         client.send_message(message.chat.id, text= 'Веди имя буквами')
    #         client.register_next_step_handler(message, get_phone)
def get_phone (message):
    try:
        if message.text == "✅Правильно":
            addres=up_addres(conn='',user_id=message.chat.id)
            client.send_message(message.chat.id, text=f'Адрес:\nСейчас: {addres[0]}',reply_markup=keyboard_for_order)
            client.register_next_step_handler(message, get_addres)
        elif message.text=='⬅️Назад':
            name=up_name(conn='', user_id=message.chat.id)
            client.send_message(message.chat.id, text=f'Как вас зовут?\nCейчас так: {name[0]}',reply_markup=keyboard_for_order)
            client.register_next_step_handler(message, get_name)
        elif message.text == '⛔️Отменить':
            if len(users[message.chat.id].rows)==0:
                client.send_message(message.chat.id, 'Корзина пуста, самое время что-нибуть выбрать: /start')    
            else: 
                showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
                item=users[message.chat.id][n][0]
                total=sum(list(users[message.chat.id].columns['price']))
                count_items=users[message.chat.id].rows[item]['amount']
                bas_url=users[message.chat.id].rows[item]['url']
                name= users[message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})'
                item_price=users[message.chat.id].rows[item]['price']/count_items
                total_item = count_items*item_price
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
                client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
        else:
            if message.text == None:
                message.text='phone'
                add_name(conn='', name=message.text, user_id=message.chat.id)
                client.send_message(message.chat.id, text= 'Веди телефон цифрами')
                client.register_next_step_handler(message, get_phone)
            elif message.text.isalpha():
                message.text='phone'
                add_name(conn='', name=message.text, user_id=message.chat.id)
                client.send_message(message.chat.id, text= 'Веди телефон цифрами')
                client.register_next_step_handler(message, get_phone)
            else:
                add_phone(conn='',phone=message.text, user_id=message.chat.id)
                addres=up_addres(conn='',user_id=message.chat.id)
                client.send_message(message.chat.id, text=f'Адрес:\nСейчас: {addres[0]}',reply_markup=keyboard_for_order)
                client.register_next_step_handler(message, get_addres)
    except AttributeError:
            client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
def get_addres(message):
    try:
        if message.text == "✅Правильно":
            order=BeautifulTable()
            order.columns.header=['Name','Amount','Price']
            cocktails=len(users[message.chat.id].rows)

            for i in range(cocktails):
                name=users[message.chat.id][i]['name']
                amount=users[message.chat.id][i]['amount']
                price=users[message.chat.id][i]['price']
                order.rows.append([name, amount, price])
            name=up_name(conn='', user_id=message.chat.id)
            phone=up_phone(conn='', user_id=message.chat.id)
            addres=up_addres(conn='',user_id=message.chat.id)
            order.set_style(BeautifulTable.STYLE_COMPACT)
            total=(sum(list(order.columns['Price'])))
            text=f'Ваш заказ:\nИмя:{name[0]}\nТeлефон:{phone[0]}\nАдрес:{addres[0]}\nВсего:{total}'
            client.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
            client.register_next_step_handler(message, send_order)
            
        elif message.text=='⬅️Назад':
            phone=up_phone(conn='', user_id=message.chat.id)
            client.send_message(message.chat.id, text=f'Ваш телефон\nСейчас: {phone[0]}',reply_markup=keyboard_for_order)
            client.register_next_step_handler(message, get_phone)
        elif message.text == '⛔️Отменить':
            if len(users[message.chat.id].rows)==0:
                client.send_message(message.chat.id, 'Корзина пуста, самое время что-нибуть выбрать: /start')    
            else: 
                showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
                item=users[message.chat.id][n][0]
                total=sum(list(users[message.chat.id].columns['price']))
                count_items=users[message.chat.id].rows[item]['amount']
                bas_url=users[message.chat.id].rows[item]['url']
                name= users[message.chat.id].rows[item]['name']
                text=f'*{name}*[_]({bas_url})'           
                basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
                client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown') 
        else:
            if message.text == None:
                message.text='addres'
                add_name(conn='', name=message.text, user_id=message.chat.id)
                client.send_message(message.chat.id, text= 'Веди адрес')
                client.register_next_step_handler(message, get_addres)
            else:
                add_addres(conn='',addres=message.text, user_id=message.chat.id)
                order=BeautifulTable()
                order.columns.header=['Name','Amount','Price']
                cocktails=len(users[message.chat.id].rows)
                for i in range(cocktails):
                    name=users[message.chat.id][i]['name']
                    amount=users[message.chat.id][i]['amount']
                    price=users[message.chat.id][i]['price']
                    order.rows.append([name, amount, price])
                name=up_name(conn='', user_id=message.chat.id)
                phone=up_phone(conn='', user_id=message.chat.id)
                addres=up_addres(conn='',user_id=message.chat.id)
                order.set_style(BeautifulTable.STYLE_COMPACT)
                total=(sum(list(order.columns['Price'])))
                text=f'Ваш заказ:\nИмя:{name[0]}\nТeлефон:{phone[0]}\nАдрес:{addres[0]}\nВсего:{total}'
                client.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
                client.register_next_step_handler(message, send_order)
    except AttributeError:
            client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
def send_order(message):
    try:
        if message.text == '✅Заказать':
                    
            order=BeautifulTable()
            order.columns.header=['Name','Amount','Price']
            cocktails=len(users[message.chat.id].rows)

            for i in range(cocktails):
                name=users[message.chat.id][i]['name']
                amount=users[message.chat.id][i]['amount']
                price=users[message.chat.id][i]['price']
                order.rows.append([name, amount, price])
            name=up_name(conn='', user_id=message.chat.id)
            phone=up_phone(conn='', user_id=message.chat.id)
            addres=up_addres(conn='',user_id=message.chat.id)
            order.set_style(BeautifulTable.STYLE_COMPACT)
            total=(sum(list(order.columns['Price'])))

            text=f'Заказ:\nИмя:{name[0]}\nТeлефон:{phone[0]}\nАдрес:{addres[0]}\nВсего:{total}\n'
            add_order(conn='', user_id=message.chat.id, order=text)
            add_ord(conn='', user_id=message.chat.id, zakaz=text)
            client.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')
            init_customer_from_message(message)
            client.send_message(message.chat.id, text='Спасибо за заказ!\nВаш заказ будет доставлен сегодня вечером с 20:00 до 23:00', reply_markup=mainkeyboard)           
        if message.text == '⬅️Назад':
            addres=up_addres(conn='',user_id=message.chat.id)
            client.send_message(message.chat.id, text=f'Адрес:\nСейчас: {addres[0]}',reply_markup=keyboard_for_order)
            client.register_next_step_handler(message, get_addres)
    except AttributeError:
        client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')
    #except psycopg2.errors.NotNullViolation:        
    # except psycopg2.errors.NotNullViolation:
    #     client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start') 
    # finally:
    #     client.send_message(message.chat.id, text= 'Что-то пошло не так,🤭 начнем с начала, нажмите /start')


@client.message_handler(content_types = ['voice'])
def get_audio(message):
    client.send_chat_action(message.chat.id, 'upload_voice')
    aud = open('reqe.ogg', 'rb')   
    client.send_voice(chat_id=message.chat.id, voice=aud) 
    
    client.send_message(message.chat.id, text='У тебя приятный голос\nНажми сюда /start', reply_markup=mainkeyboard)

@client.message_handler(content_types = ['photo'])
def get_photo(message):
    
    client.send_message(message.chat.id, text='Смотри какие у меня', reply_markup=mainkeyboard)
    client.send_chat_action(message.chat.id, 'upload_voice')
    ph = open('siski1.jpg', 'rb')   
    client.send_photo(message.chat.id, ph, caption="хочешь больше нажми /start")  
    
    
client.polling(none_stop= True, interval=0)


# if __name__ =="__main__":
#     print (basket)
#     print (basket[0]['name'])
#     sumtest = 1
#     print (basket[0]['amount']+basket[1]['amount'])