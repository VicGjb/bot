import configure
import telebot
import urllib
# from flask import Flask
# from flask_sslify import SSLify
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
 
#https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B

client=telebot.TeleBot(configure.config['token'])
# app=Flask(__name__)
# sslify=SSLify(app)
global users
users={}
key = init_user(conn='')
for id in key:
    t=id['user_id']
    users.update({t:f'{t}_basket'})

url = 'https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
f = open('out.jpg','wb')
f.write(urllib.request.urlopen(url).read())
f.close()


#mainekeyboard
mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
menubutton = types.KeyboardButton ('🍴Меню🍴') 
basketbutton = types.KeyboardButton('🛍Корзина🛍')
aboutus = types.KeyboardButton('💁🏻‍♀️О нас💁🏻‍♀️')
orders = types.KeyboardButton('🧳Заказы🧳')
#back = types.KeyboardButton('🍴Вернуться🍴')
mainkeyboard.add(menubutton, basketbutton, aboutus, orders)

#coctailmenu
cocktailkeyboard=types.InlineKeyboardMarkup(row_width=1)
sign_type=types.InlineKeyboardButton(text='🍹Авторские коктейли🍹', callback_data='sig')
classic_type=types.InlineKeyboardButton(text='🍸Классические коктейли🍸',callback_data='clas')
g_t_type=types.InlineKeyboardButton(text='🧊Джин-тоник🧊',callback_data='g_t')
spritzs_type=types.InlineKeyboardButton(text='🍾Сприцы🍊',callback_data='spr')
negroni_type=types.InlineKeyboardButton(text='🧊Негрони🧊',callback_data='neg')
cocktailkeyboard.add(sign_type, classic_type, g_t_type, spritzs_type, negroni_type)

#order keyboard
keyboard_for_order =types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True) 
correct = types.KeyboardButton ('✅Правильно') 
back_in_order = types.KeyboardButton('⬅️Назад')
cancel = types.KeyboardButton('⛔️Отменить')
keyboard_for_order.add(correct,back_in_order,cancel)

#last_keyboard
last_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
make_order=types.KeyboardButton('✅Заказать')
last_keyboard.add(make_order, back_in_order)

#keyboard for coctails
def keyboard(price05,price03,cocktail_name):
    trade_keyboard=types.InlineKeyboardMarkup(row_width=2)
    half_litr = types.InlineKeyboardButton (text=f'0.5L\n{price05}NIS', callback_data=f'0.5L {cocktail_name}')
    thirt_litr = types.InlineKeyboardButton(text=f'0.3L\n{price03}NIS', callback_data=f'0.3L {cocktail_name}')
    basket = types.InlineKeyboardButton(text='🛍Оформить заказ', callback_data='basket')
    trade_keyboard.add(half_litr, thirt_litr, basket)
    return trade_keyboard

#keyboard for basket
def basket_test(count_items,showitem,total):

    basket_keyboard = types.InlineKeyboardMarkup(row_width=1)

    more_button = types.InlineKeyboardButton(text = '➕', callback_data='more')
    less_button= types.InlineKeyboardButton(text='➖', callback_data = 'less')
    count_items = types.InlineKeyboardButton(text=f'{count_items}', callback_data = 'nts')
    delete_button = types.InlineKeyboardButton(text='❌', callback_data = 'del')
    next_button = types.InlineKeyboardButton(text='след.▶️', callback_data= 'next')
    back_button = types.InlineKeyboardButton(text='◀️пред.', callback_data = 'back')
    showitem_button = types.InlineKeyboardButton(text=f'{showitem}', callback_data='nts')
    start_order = types.InlineKeyboardButton(text=f'✅Оформить заказ {total} NIS', callback_data='order')
    back_to_menu = types.InlineKeyboardButton(text='🍸Продолжить покупку', callback_data='main')

    basket_keyboard.row(delete_button,less_button,count_items,more_button)
    basket_keyboard.row(back_button, showitem_button, next_button)
    basket_keyboard.add(start_order,back_to_menu)
    return basket_keyboard


def basket_iter(n,call):
   
    item=users[call.message.chat.id][n][0]
    showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
    total=sum(list(users[call.message.chat.id].columns['price']))
    count_items=users[call.message.chat.id].rows[item]['amount']
    bas_url=users[call.message.chat.id].rows[item]['url'] 
    name= users[call.message.chat.id].rows[item]['name']        
    text=f'{name} [_]({bas_url})'
    basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)

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
            text=''.join(f'{cocktail_name} \n{cocktail_description}') 
            price05=cocktail['price05']
            price03=cocktail['price03']
            trade_keyboard=keyboard(price05,price03,cocktail_name)
            
            client.send_photo(call.message.chat.id, pic, reply_to_message_id="Б",caption=text,reply_markup=trade_keyboard)
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
            #init_customer_from_call(call=call)
            if name_h  in users[call.message.chat.id].rows.header:
                users[call.message.chat.id].rows[name_h]['amount']+=1
                users[call.message.chat.id].rows[name_h]['price']+=price_h
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
              
            else:          
                users[call.message.chat.id].rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
               # print(users[call.message.chat.id])
        if call.data == name_t:
            #init_customer_from_call(call=call)
            if name_t  in users[call.message.chat.id].rows.header:
                users[call.message.chat.id].rows[name_t]['amount']+=1
                users[call.message.chat.id].rows[name_t]['price']+=price_t
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
               
            else:        
                users[call.message.chat.id].rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   











#----------------------------------------------------------------------------------------------------------------------------#

@client.message_handler(commands=['start'])
def welcome (message):
    #приветствие и основное меню внизу
    
    client.send_chat_action(message.chat.id, 'upload_photo')
    img = open('out.jpg', 'rb')   
    url='https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
    client.send_photo(message.chat.id, img, reply_to_message_id="Б",caption='Добро пожаловать!',reply_markup=mainkeyboard)  
    
    init_customer_from_message(message)
   
@client.callback_query_handler(func = lambda call:True)
def get_call(call):
    if call.data=='main':
        #init_customer_from_call(call=call)
        client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   reply_markup=cocktailkeyboard,text='Рады предложить вам, следующие виды напитков:')

    if call.data =='sig':
        #init_customer_from_call(call=call)
        m=up_cocktail(conn='',tip='sig')
        for cocktail in m:
            
            addr=cocktail['url_photo']
            pic = open('pic.jpg','wb')
            pic.write(urllib.request.urlopen(addr).read())
            pic.close()
            client.send_chat_action(call.message.chat.id, 'upload_photo')
            pic = open('pic.jpg', 'rb')           
            cocktail_description=cocktail['description']
            cocktail_name=cocktail['name']   
            text=''.join(f'{cocktail_name} \n{cocktail_description}') 
            price05=cocktail['price05']
            price03=cocktail['price03']
            trade_keyboard=keyboard(price05,price03,cocktail_name)
            
            client.send_photo(call.message.chat.id, pic, reply_to_message_id="Б",caption=text,reply_markup=trade_keyboard)
   # print(users)
    m=up_cocktail(conn='',tip='sig')
    for cocktail in m:
        cocktail_name=cocktail['name']
        name_h=f'0.5L {cocktail_name}'
        name_t=f'0.3L {cocktail_name}'   
        cocktail_photo=cocktail['url_photo']
        price_h=cocktail['price05']
        price_t=cocktail['price03']  
        if call.data == name_h:
            #init_customer_from_call(call=call)
            if name_h  in users[call.message.chat.id].rows.header:
                users[call.message.chat.id].rows[name_h]['amount']+=1
                users[call.message.chat.id].rows[name_h]['price']+=price_h
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
              
            else:          
                users[call.message.chat.id].rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
               # print(users[call.message.chat.id])
        if call.data == name_t:
            #init_customer_from_call(call=call)
            if name_t  in users[call.message.chat.id].rows.header:
                users[call.message.chat.id].rows[name_t]['amount']+=1
                users[call.message.chat.id].rows[name_t]['price']+=price_t
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
               
            else:        
                users[call.message.chat.id].rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
               
    if call.data =='clas':
        cocktail_type(tip='clas',call=call)
    cocktail_size(tip='clas',call=call)
    
    # m=up_cocktail(conn='',tip='clas')
    # for cocktail in m:
    #     cocktail_name=cocktail['name']
    #     name_h=f'0.5L {cocktail_name}'
    #     name_t=f'0.3L {cocktail_name}'   
    #     cocktail_photo=cocktail['url_photo']
    #     price_h=cocktail['price05']
    #     price_t=cocktail['price03']  
    #     if call.data == name_h:
    #         #init_customer_from_call(call=call)
    #         if name_h  in users[call.message.chat.id].rows.header:
    #             users[call.message.chat.id].rows[name_h]['amount']+=1
    #             users[call.message.chat.id].rows[name_h]['price']+=price_h
    #             client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
              
    #         else:          
    #             users[call.message.chat.id].rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
    #             client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
    #            # print(users[call.message.chat.id])
    #     if call.data == name_t:
    #         #init_customer_from_call(call=call)
    #         if name_t  in users[call.message.chat.id].rows.header:
    #             users[call.message.chat.id].rows[name_t]['amount']+=1
    #             users[call.message.chat.id].rows[name_t]['price']+=price_t
    #             client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
               
    #         else:        
    #             users[call.message.chat.id].rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
    #             client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
    







        
        #client.send_message(call.message.chat.id, 'ахуенный коктейль2', reply_markup=trade_keyboard)
    # if call.data =='g_t':
    #     client.send_message(call.message.chat.id, 'ахуенный коктейль3', reply_markup=trade_keyboard)
    # if call.data =='spr':
    #     client.send_message(call.message.chat.id, 'ахуенный коктейль4', reply_markup=trade_keyboard)
    # if call.data =='neg':
    #     client.send_message(call.message.chat.id, 'ахуенный коктейль5', reply_markup=trade_keyboard)
    # if call.data == 'a':
    #     client.send_message(call.message.chat.id, 'test', reply_markup=trade_keyboard)
    # global n
    # n=0
    
    #-----------------------Baskect====================================================================================================
    if call.data == 'basket':
        if len(users[call.message.chat.id].rows)==0:
            client.send_message(call.message.chat.id, 'empty')    
        else: 
            global n
            n=0
            showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
            item=users[call.message.chat.id][n][0]
            total=sum(list(users[call.message.chat.id].columns['price']))
            count_items=users[call.message.chat.id].rows[item]['amount']
            bas_url=users[call.message.chat.id].rows[item]['url']
            name= users[call.message.chat.id].rows[item]['name']
            text=f'{name}[_]({bas_url})'    
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(call.message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
           
#---------------Basket_iter---------------------------------------------------------------------------------------------=================
    if call.data == 'next':
       # init_customer_from_call(call=call)
        n+=1
        if n>len(users[call.message.chat.id].rows)-1:
            n-=1
            basket_iter(n=n,call=call)
        else:
            basket_iter(n=n,call=call)        
    
    if call.data == 'back':
       # init_customer_from_call(call=call)
        n=n-1
        if n<0:
            n+=1
            basket_iter(n=n,call=call)
        else:
            basket_iter(n=n,call=call)      

    if call.data=='more':
        #init_customer_from_call(call=call)
        item=users[call.message.chat.id][n][0]
        users[call.message.chat.id].rows[item]['price']+=users[call.message.chat.id].rows[item]['price']/users[call.message.chat.id].rows[item]['amount']
        users[call.message.chat.id].rows[item]['amount']+=1
        showitem=f'{n+1}/{len(users[call.message.chat.id].rows)}'
        total=sum(list(users[call.message.chat.id].columns['price']))
        count_items=users[call.message.chat.id].rows[item]['amount']
        bas_url=users[call.message.chat.id].rows[item]['url']
        name= users[call.message.chat.id].rows[item]['name']
        
        text=f'{name}[_]({bas_url})'    
        basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
        client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

    if call.data=='less':
        #init_customer_from_call(call=call)
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
        text=f'{name}[_]({bas_url})'    
        basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
        client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')
    
    if call.data =='del':
        #init_customer_from_call(call=call)
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
            text=f'{name}[_]({bas_url})'            
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

    if call.data=='order':
        name=up_name(conn='', user_id=call.message.chat.id)

        client.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                    text='Начинаем оформлять заказ')
        client.send_message(chat_id=call.message.chat.id, text=f'Как вас зовут?\nCейчас так: {name[0]}', reply_markup=keyboard_for_order)
        client.register_next_step_handler(call.message, get_name)
#---------------------------------------------------------------------------------------------------------------------------------------------
@client.message_handler(content_types = ['text'])
def get_text(message):
    if message.text=='🍴Меню🍴' or message.text=='🍴Вернуться🍴':
        client.send_message(message.chat.id,'Рады предложить вам следующие типы напитков:', reply_markup= cocktailkeyboard)
        init_customer_from_message(message)
    elif message.text == '🛍Корзина🛍':
        #init_customer_from_message(message)
        if len(users[message.chat.id].rows)==0:
            client.send_message(message.chat.id, 'empty')    
        else: 
            global n
            n=0
            showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
            item=users[message.chat.id][n][0]
            total=sum(list(users[message.chat.id].columns['price']))
            count_items=users[message.chat.id].rows[item]['amount']
            bas_url=users[message.chat.id].rows[item]['url']
            name= users[message.chat.id].rows[item]['name']
            text=f'{name}[_]({bas_url})'           
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
    
         
    elif message.text == '💁🏻‍♀️О нас💁🏻‍♀️':
        client.send_message(message.chat.id, 'Мы типо пипeц душевные ебать профессионльные\nты будешь доволен, счастлив и прекрасен')
    elif message.text == '🧳Заказы🧳':
        a=get_ord(conn='',user_id=message.chat.id, limit=5)
        text='\n------------\n'.join([f'{m} \n {n}' for m, n in a])
        print(text)
        client.send_message(message.chat.id, text=f'вот ваши последние заказы:\n\n{text}\n',reply_markup=mainkeyboard)
    else:
        client.send_message(message.chat.id,'Выбери что-нибудть там внизу:⤵️ ')
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# def edit_name(message):
#     name=up_name(conn='', user_id=message.chat.id)
#     client.send_message(message.chat.id, text=f'Как вас зовут?\nCейчас так: {name[0]}',reply_markup=keyboard_for_order)
#     client.register_next_step_handler(message, get_name)

def get_name(message):
    if message.text == "✅Правильно":
        phone=up_phone(conn='', user_id=message.chat.id)
        client.send_message(message.chat.id, text=f'Ваш телефон\nСейчас: {phone[0]}',reply_markup=keyboard_for_order)
        client.register_next_step_handler(message, get_phone)
    elif message.text=='⬅️Назад':
        if len(users[message.chat.id].rows)==0:
            client.send_message(message.chat.id, 'empty')    
        else: 
            showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
            item=users[message.chat.id][n][0]
            total=sum(list(users[message.chat.id].columns['price']))
            count_items=users[message.chat.id].rows[item]['amount']
            bas_url=users[message.chat.id].rows[item]['url']
            name= users[message.chat.id].rows[item]['name']
            text=f'{name}[_]({bas_url})'           
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
    elif message.text == '⛔️Отменить':
        if len(users[message.chat.id].rows)==0:
            client.send_message(message.chat.id, 'empty')    
        else: 
            showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
            item=users[message.chat.id][n][0]
            total=sum(list(users[message.chat.id].columns['price']))
            count_items=users[message.chat.id].rows[item]['amount']
            bas_url=users[message.chat.id].rows[item]['url']
            name= users[message.chat.id].rows[item]['name']
            text=f'{name}[_]({bas_url})'           
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
    
    else:
        client.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        add_name(conn='',name=message.text, user_id=message.chat.id)
        phone=up_phone(conn='', user_id=message.chat.id)
        client.send_message(message.chat.id, text=f'Ваш телефон\nСейчас: {phone[0]}',reply_markup=keyboard_for_order)
        client.register_next_step_handler(message, get_phone)

def get_phone (message):
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
            client.send_message(message.chat.id, 'empty')    
        else: 
            showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
            item=users[message.chat.id][n][0]
            total=sum(list(users[message.chat.id].columns['price']))
            count_items=users[message.chat.id].rows[item]['amount']
            bas_url=users[message.chat.id].rows[item]['url']
            name= users[message.chat.id].rows[item]['name']
            text=f'{name}[_]({bas_url})'           
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
    else:
        add_phone(conn='',phone=message.text, user_id=message.chat.id)
        addres=up_addres(conn='',user_id=message.chat.id)
        client.send_message(message.chat.id, text=f'Адрес:\nСейчас: {addres[0]}',reply_markup=keyboard_for_order)
        client.register_next_step_handler(message, get_addres)

def get_addres(message):
    if message.text == "✅Правильно":
        order=BeautifulTable()
        order.columns.header=['Name','Amount','Price']
        cocktails=len(users[message.chat.id].rows)
        #print(cocktails)
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
        text=f'Ваш заказ:\nИмя:{name[0]}\nТeлефон:{phone[0]}\nАдрес:{addres[0]}\nВсего:{total}\nбудет доставлен сегодня вечером с 20:00 до 23:00'
        client.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
        client.register_next_step_handler(message, send_order)
        
       # client.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')
    elif message.text=='⬅️Назад':
        phone=up_phone(conn='', user_id=message.chat.id)
        client.send_message(message.chat.id, text=f'Ваш телефон\nСейчас: {phone[0]}',reply_markup=keyboard_for_order)
        client.register_next_step_handler(message, get_phone)
    elif message.text == '⛔️Отменить':
        if len(users[message.chat.id].rows)==0:
            client.send_message(message.chat.id, 'empty')    
        else: 
            showitem=f'{n+1}/{len(users[message.chat.id].rows)}'
            item=users[message.chat.id][n][0]
            total=sum(list(users[message.chat.id].columns['price']))
            count_items=users[message.chat.id].rows[item]['amount']
            bas_url=users[message.chat.id].rows[item]['url']
            name= users[message.chat.id].rows[item]['name']
            text=f'{name}[_]({bas_url})'           
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown') 
    else:
        add_addres(conn='',addres=message.text, user_id=message.chat.id)
        order=BeautifulTable()
        order.columns.header=['Name','Amount','Price']
        cocktails=len(users[message.chat.id].rows)
        #print(cocktails)
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
        text=f'Ваш заказ:\nИмя:{name[0]}\nТeлефон:{phone[0]}\nАдрес:{addres[0]}\nВсего:{total}\nбудет доставлен сегодня вечером с 20:00 до 23:00'
        client.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
        client.register_next_step_handler(message, send_order)
       # client.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')

def send_order(message):
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

        client.send_message(message.chat.id, text='Спасибо за заказ', reply_markup=mainkeyboard)
        client.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')
        init_customer_from_message(message)
    if message.text == '⬅️Назад':
        
        addres=up_addres(conn='',user_id=message.chat.id)
        client.send_message(message.chat.id, text=f'Адрес:\nСейчас: {addres[0]}',reply_markup=keyboard_for_order)
        client.register_next_step_handler(message, get_addres)
        # client.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')


client.polling(none_stop= True, interval=1)

# if __name__ =="__main__":
#     print (basket)
#     print (basket[0]['name'])
#     sumtest = 1
#     print (basket[0]['amount']+basket[1]['amount'])