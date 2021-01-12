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
    users.update({t_id:'',t_basket:'',t_cocktail_menu:'',t_call:'',t_orders:''})


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

global oops_messege
url_types={
           'Signature Cocktails':'https://github.com/VicGjb/bot/blob/master/Signature%20cocktail.jpg?raw=true',
           'Classic Coktails':'https://github.com/VicGjb/bot/blob/master/classic%20cocktail.jpg?raw=true',
           'Gin&Tonic':'https://github.com/VicGjb/bot/blob/master/Gin&tonic.jpg?raw=true',
           'Spritz':'https://github.com/VicGjb/bot/blob/master/Aperol.jpg?raw=true',
           'Negronis':'https://github.com/VicGjb/bot/blob/master/negroni.jpg?raw=true'
           }

class MakeOrder(StatesGroup):
    get_name=State()
    get_phone=State()
    get_addres=State()
    make_order=State()
    back_to_card=State()

#-----------------------------------------Static Keybords-----------------------\
#maine keyboard reply
mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
menubutton = types.KeyboardButton ('🍴Menu🍴') 
basketbutton = types.KeyboardButton('🛒Card🛒')
aboutus = types.KeyboardButton('💁🏻‍♀️Info💁🏻‍♀️')
orders = types.KeyboardButton('🧳Orders🧳')
mainkeyboard.add(menubutton, basketbutton, aboutus, orders)

#coctailmenu
cocktailkeyboard=types.InlineKeyboardMarkup(row_width=1)
sign_type=types.InlineKeyboardButton(text='🍹Signature Cocktails🍹', callback_data='Signature Cocktails')
classic_type=types.InlineKeyboardButton(text='🍸Classic Coktails🍸',callback_data='Classic Coktails')
g_t_type=types.InlineKeyboardButton(text='🍋Gin&Tonic🍋',callback_data='Gin&Tonic')
spritzs_type=types.InlineKeyboardButton(text='🍾Aperol Spritz Twists🍊',callback_data='Spritz')
negroni_type=types.InlineKeyboardButton(text='🥃Negroni Twists🍊',callback_data='Negronis')
cocktailkeyboard.add(sign_type, classic_type, g_t_type, spritzs_type, negroni_type)

#order keyboard reply
keyboard_for_order =types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True) 
correct = types.KeyboardButton ('✅Correct') 
back_in_order = types.KeyboardButton('⬅️Back')
cancel = types.KeyboardButton('⛔️Cancel')
keyboard_for_order.add(correct,back_in_order,cancel)

#send order keyboard
last_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=2,one_time_keyboard=True)
make_order=types.KeyboardButton('✅Send Order')
last_keyboard.add(make_order, back_in_order)
#-----------function for operation in menu-------------------------------------\
#keyboard for coctails in menu
async def keyboard(price05,price03,cocktail_name,tip):
    trade_keyboard=types.InlineKeyboardMarkup(row_width=2)
    half_litr = types.InlineKeyboardButton (text=f'🛍Buy 0.5L\n {price05}₪', callback_data=f'0.5L {cocktail_name}')
    thirt_litr = types.InlineKeyboardButton(text=f'🛍Buy 0.3L\n {price03}₪', callback_data=f'0.3L {cocktail_name}')
    basket = types.InlineKeyboardButton(text='🛒Go to Card', callback_data='basket')
    go_to_menu = types.InlineKeyboardButton(text='◀️Back', callback_data=f'{tip}')
    trade_keyboard.add(half_litr, thirt_litr, basket)
    trade_keyboard.row(go_to_menu)
    return trade_keyboard

async def create_keybord_for_coctails_in_type (tip,call):
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
                    #text+=(f'\n*{cocktail_name}*  \n{cocktail_description}\n')
                    text=f'[{cocktail_type}]({cocktail_url})'  
                    button=types.InlineKeyboardButton(text=f'{cocktail_name}',callback_data=f'{cocktail_name}')
                    type_keyboard.add(button) 
        main_menu=types.InlineKeyboardButton(text='◀️Main menu📜',callback_data='main')
        type_keyboard.add(main_menu)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=type_keyboard, parse_mode='Markdown')
        #text=f'[{cocktail_type}](https://github.com/VicGjb/bot/blob/master/TestBotDeploy/Bot/for%20bot.jpg?raw=true)'
    except KeyError:
        print('!!!!!!!!!!!!!!im in type cocktail!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
async def show_cocktail(call,tip):
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
                    trade_keyboard= await keyboard(price05,price03,cocktail_name,tip=tip)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=trade_keyboard,parse_mode='Markdown') 
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
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} is in the card') 

                        else:          
                            users[f'{call.message.chat.id}_basket'].rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} is in the card')      
                    except AttributeError:
                        print('!!!!!!!!AtE cocktail size!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
                    except NameError:
                        print('!!!!!!!!!!NE cocktail size!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
                if call.data == name_t:
                    try:
                        if name_t  in users[f'{call.message.chat.id}_basket'].rows.header:
                            users[f'{call.message.chat.id}_basket'].rows[name_t]['amount']+=1
                            users[f'{call.message.chat.id}_basket'].rows[name_t]['price']+=price_t
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} is in the card') 
                        else:        
                            users[f'{call.message.chat.id}_basket'].rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
                            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} is in the card') 
                    except AttributeError:
                        print('atribute error in cocktail size')
                        await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
                    except KeyError:
                        print('name error in cocktail size')
                        await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
    except KeyError:
        print('Im iin coktail size key err last one')
        await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
#------------------------------funtion for operation with card--------------------------------------------------------\
#keyboard for basket
async def basket_test(count_items,showitem,total,item_price,total_item):

    basket_keyboard = types.InlineKeyboardMarkup(row_width=1)
    price_of_item= types.InlineKeyboardButton(text=f'{item_price} ₪ * {count_items}={total_item} ₪',callback_data ='nts')
    more_button = types.InlineKeyboardButton(text = '➕', callback_data='more')
    less_button= types.InlineKeyboardButton(text='➖', callback_data = 'less')
    count_items = types.InlineKeyboardButton(text=f'{count_items}', callback_data = 'nts')
    delete_button = types.InlineKeyboardButton(text='❌', callback_data = 'del')
    next_button = types.InlineKeyboardButton(text='next ▶️', callback_data= 'next') 
    back_button = types.InlineKeyboardButton(text='◀️prev.', callback_data = 'back')
    showitem_button = types.InlineKeyboardButton(text=f'{showitem}', callback_data='nts')
    start_order = types.InlineKeyboardButton(text=f'✅Make Order {total} ₪', callback_data='order')
    back_to_menu = types.InlineKeyboardButton(text='🍸Continue Shopping', callback_data='main')

    basket_keyboard.add(price_of_item)
    basket_keyboard.row(delete_button,less_button,count_items,more_button)
    basket_keyboard.row(back_button, showitem_button, next_button)
    basket_keyboard.add(start_order,back_to_menu)
    return basket_keyboard

#show basket from Reply keyboard
async def basket_from_message (n, message):
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
    basket_keyboard= await basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
    await bot.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
   
#show basket from inlain keyboard
async def basket_from_call(n, item, call):
    basketC=f'{call.message.chat.id}_basket'
    showitem=f'{n+1}/{len(users[basketC].rows)}'
    total=sum(list(users[f'{call.message.chat.id}_basket'].columns['price']))
    count_items=users[f'{call.message.chat.id}_basket'].rows[item]['amount']
    bas_url=users[f'{call.message.chat.id}_basket'].rows[item]['url']
    name= users[f'{call.message.chat.id}_basket'].rows[item]['name']
    text=f'*{name}*[_]({bas_url})' 
    item_price=users[f'{call.message.chat.id}_basket'].rows[item]['price']/count_items
    total_item = count_items*item_price
    basket_keyboard=await basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')

async def basket_iter(n,call):
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
    basket_keyboard=await basket_test(count_items=count_items,showitem=showitem,total=total,item_price=item_price,total_item=total_item)

    return await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

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
    img = open('out.jpg', 'rb')   
    url='https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
    await bot.send_photo(message.chat.id, img, reply_markup=mainkeyboard)  
    await init_customer_from_message(message)

#------------------comuticatiom by InlineKeyboard-----------------------------------------------------------------------------------\
@client.callback_query_handler(lambda c: c.data)
async def get_call (call: types.CallbackQuery):
    if call.data =='menu':
        await bot.send_message(chat_id=call.message.chat.id,reply_markup=cocktailkeyboard,
                            text="We're happy to offer you this cocktails:")
    if call.data=='main':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                            reply_markup=cocktailkeyboard,text="We're happy to offer you this cocktails:")
   
    users[call.message.chat.id]=False
    for tip in type_cocktail:
        print(tip)
        if call.data==tip[0]:
            await create_keybord_for_coctails_in_type(tip=tip[0], call=call)
            users[f'{call.message.chat.id}_call']=call.data
            users[call.message.chat.id]=True  
    print(users[call.message.chat.id])         
    if users[call.message.chat.id]==False:
        print(f'{call.data} Я сноваа здесь')
        try:  
            await show_cocktail(call=call, tip=users[f'{call.message.chat.id}_call']) 
            await cocktail_size(tip=users[f'{call.message.chat.id}_call'], call=call) 
        except KeyError:
            print('hey im key error in call about cocktail menu')
#         #-----------------------Baskect-----------------------------------------------------------------------------------------------\
    if call.data == 'basket':
        try:
            if len(users[f'{call.message.chat.id}_basket'].rows)==0:
                await bot.send_message(call.message.chat.id, "The card is empty, let's choose your cocktails: /start")    
            else: 
                global n
                n=0
                item=users[f'{call.message.chat.id}_basket'][n][0]
                await basket_from_call(n=n, item=item, call=call)
        except AttributeError:
            
            print('i am AtributeError im in basket call')    

    if call.data == 'next':
        try:
            n+=1
            if n>len(users[f'{call.message.chat.id}_basket'].rows)-1:
                n-=1
                await basket_iter(n=n,call=call)
            else:
                await basket_iter(n=n,call=call)
        except NameError:
            print('im Name error in next')     

    if call.data == 'back':  
        try:
            n=n-1
            if n<0:
                n+=1
                await basket_iter(n=n,call=call)
            else:
                await basket_iter(n=n,call=call)      
        except NameError:
            print('I am NemeError in back')

    if call.data=='more':
        try:
            item=users[f'{call.message.chat.id}_basket'][n][0]
            users[f'{call.message.chat.id}_basket'].rows[item]['price']+=users[f'{call.message.chat.id}_basket'].rows[item]['price']/users[f'{call.message.chat.id}_basket'].rows[item]['amount']
            users[f'{call.message.chat.id}_basket'].rows[item]['amount']+=1
            await basket_from_call(n=n, item=item, call=call)
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
            await basket_from_call(n=n, item=item, call=call)   
        except NameError:
            print('im Name Error in less')

    if call.data =='del':
        try:
            del users[f'{call.message.chat.id}_basket'].rows[n]
            if len(users[f'{call.message.chat.id}_basket'].rows)==0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=cocktailkeyboard,text="Oops, something is wrong🤭 let's start over, press /start")
            else:
                if n==len(users[f'{call.message.chat.id}_basket'].rows):
                    n-=1   
                item=users[f'{call.message.chat.id}_basket'][n][0]
                await basket_from_call(n=n, item=item, call=call)

        except AttributeError:
            print('im Name Error in del')

    if call.data=='order':
        try:

            name=users[f'{call.message.chat.id}_person'].columns['name'][f'{call.message.chat.id}']
            await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                        text='Add personal info')
            await bot.send_message(chat_id=call.message.chat.id, text=f'What is your name?\nNow we know you as: {name}', reply_markup=keyboard_for_order)
            await MakeOrder.get_name.set()
        except NameError: #AttributeError:
            await bot.send_message(call.message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
            print(' im name error in order call')

# #---------------comutication by ReplyKeyboard------------------------------------------------------------------------------------------------------\
@client.message_handler(content_types = ['text'])
async def get_text(message):
    if message.text=='🍴Menu🍴' or message.text=='🍴Вернуться🍴':# может пригодиться
        await bot.send_message(message.chat.id,"We're happy to offer you this cocktails:", reply_markup= cocktailkeyboard)


    elif message.text == '🛒Card🛒':
        try:  
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id,"The card is empty, let's choose your cocktails: /start")    
            else: 
                global n
                n=0
                await basket_from_message(n=n,message=message)
        except AttributeError:
            print('im AtrErorr in card by message')
            await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")
        except NameError:
            print('im Name errorin card by message')
            await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")   
        except KeyError:
            print('im KeyError in card by message')
            await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")


    elif message.text == '💁🏻‍♀️Info💁🏻‍♀️':
        url='https://scontent.fhfa1-1.fna.fbcdn.net/v/t1.0-9/51087951_2681893448493125_7010877500414754816_o.jpg?_nc_cat=107&ccb=2&_nc_sid=174925&_nc_ohc=W5-onSfCwL4AX-gsWKY&_nc_ht=scontent.fhfa1-1.fna&oh=d41c099e79bb84248488f1466a085962&oe=600672E5'
        chris= open('chris.jpg','wb')
        chris.write(urllib.request.urlopen(url).read())
        chris.close()
        chris=open('chris.jpg','rb')
        await bot.send_photo(message.chat.id, chris)
        text="We're the team of professional bartenders, who will provide you the best drinks for your joy! \n*Contacts:*\n[Facebook](https://www.facebook.com/coctailexpresstlv)\n[Instagram](https://www.instagram.com/cocktailexpresstlv)\nPhone: 053-306-7303"
        await bot.send_message(message.chat.id, text=text, parse_mode='Markdown',disable_web_page_preview=True)


    elif message.text == '🧳Orders🧳':
        try:
            text=''
            if len(users[f'{message.chat.id}_last_orders'])==0:
                await bot.send_message(message.chat.id, text=f"You have no orders yet, it's time to order your first cocktail🍸 press /start",reply_markup=mainkeyboard)
            else:
                for i in range (len(users[f'{message.chat.id}_last_orders'].rows)):
                        time=users[f'{message.chat.id}_last_orders'].rows[i]['time']
                        order=users[f'{message.chat.id}_last_orders'].rows[i]['order']
                        text=text + (f'{time} \n{order}\n--------------------\n')
                await bot.send_message(message.chat.id, text=f'Your last orders:\n\n{text}\n',reply_markup=mainkeyboard) 
        except KeyError:
            print('KeyError in orders') 
            await bot.send_message(message.chat.id, text=f"You have no orders yet, it's time to order your first cocktail🍸 press /start") 
    else:
        await bot.send_message(message.chat.id,'Press marked button\n or start over: /start', reply_markup=mainkeyboard)
# #--------------Validation and order-------------------------------------------------------------------------------------------------

@client.message_handler(state=MakeOrder.get_name, content_types=types.ContentTypes.TEXT)
async def get_name(message, state:FSMContext):
    try:
        if message.text == "✅Correct":
            phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
            await bot.send_message(message.chat.id, text=f'Your phone number\nNow: {phone}',reply_markup=keyboard_for_order)
            await MakeOrder.get_phone.set()
        
        elif message.text=='⬅️Back':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id,"The card is empty, let's choose your cocktails: /start")    
            else: 
                await bot.send_message(message.chat.id, text= 'back to cart',reply_markup=mainkeyboard)
                await basket_from_message(n=n,message=message)
        
        elif message.text == '⛔️Cancel':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id,"The card is empty, let's choose your cocktails: /start")    
            else: 
                await bot.send_message(message.chat.id, text= 'back to cart',reply_markup=mainkeyboard)
                await basket_from_message(n=n,message=message)
            
        else:
            if message.text == None:
                message.text='Name'
                await bot.send_message(message.chat.id, text= 'Type your name')
                await MakeOrder.get_name.set()

            else:

                users[f'{message.chat.id}_person'].rows[f'{message.chat.id}']['name']=f'{message.text}'
                phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
                await bot.send_message(message.chat.id, text=f'Your phone number\nNow: {phone}',reply_markup=keyboard_for_order)
                await MakeOrder.get_phone.set()

    except AttributeError: #NameError: #AttributeError:
            print('AtrError in get_name')
            await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")

@client.message_handler(state=MakeOrder.get_phone, content_types=types.ContentTypes.TEXT)   
async def get_phone (message, state:FSMContext):
    try:
        if message.text == "✅Correct":
            if users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}'].isdigit():

                addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
                await bot.send_message(message.chat.id, text=f'Your address:\nNow: {addres}',reply_markup=keyboard_for_order)
                await MakeOrder.get_addres.set()
            else:
                await bot.send_message(message.chat.id, text= 'Type your phone number (format 0500000000)')
                await MakeOrder.get_phone.set()
        
        elif message.text=='⬅️Back':
            name=users[f'{message.chat.id}_person'].columns['name'][f'{message.chat.id}']
            await bot.send_message(message.chat.id, text=f'What is your name?\nNow we know you as: {name}',reply_markup=keyboard_for_order)
            await MakeOrder.get_name.set()
        
        elif message.text == '⛔️Cancel':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id,"The card is empty, let's choose your cocktails: /start")    
            else: 
                await bot.send_message(message.chat.id, text= 'back to cart',reply_markup=mainkeyboard)
                await basket_from_message(n=n,message=message)
           
        else:
            if message.text == None:
                await bot.send_message(message.chat.id, text= 'Type your phone number (format 0500000000)')
                await MakeOrder.get_phone.set() 
            elif message.text.isdigit():
                users[f'{message.chat.id}_person'].rows[f'{message.chat.id}']['phone']=message.text

                addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
                await bot.send_message(message.chat.id, text=f'Your address:\nNow: {addres}',reply_markup=keyboard_for_order)
                await MakeOrder.get_addres.set()             
            else:
                await bot.send_message(message.chat.id, text= 'Type your phone number (format 0500000000)')
                await MakeOrder.get_phone.set()
    except AttributeError:
            print('im AttrError in get_phone')
            await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")

@client.message_handler(state=MakeOrder.get_addres, content_types=types.ContentTypes.TEXT)
async def get_addres(message, state:FSMContext):
    try:
        if message.text == "✅Correct":
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
            text=f'Your order:\nName:{name}\nPhone:{phone}\nAddress:{addres}\nTotal:{total}'
            await bot.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
            await MakeOrder.make_order.set()   
        
        elif message.text=='⬅️Back':
            phone=users[f'{message.chat.id}_person'].columns['phone'][f'{message.chat.id}']
            await bot.send_message(message.chat.id, text=f'Your phone number\nNow: {phone}',reply_markup=keyboard_for_order)
            await MakeOrder.get_phone.set()
        
        elif message.text == '⛔️Cancel':
            await state.finish()
            if len(users[f'{message.chat.id}_basket'].rows)==0:
                await bot.send_message(message.chat.id,"The card is empty, let's choose your cocktails: /start")    
            else: 
                await bot.send_message(message.chat.id, text= 'back to cart',reply_markup=mainkeyboard)
                await basket_from_message(n=n,message=message)     
            
        else:
            if message.text == None:
                message.text='addres'
                await bot.send_message(message.chat.id, text= 'Type address:')
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
                text=f'Your order:\nName:{name}\nPhone:{phone}\nAddress:{addres}\nTotal:{total}'
                await bot.send_message(message.chat.id, text=text, reply_markup=last_keyboard)
                await MakeOrder.make_order.set()
    except AttributeError:
        print('AttError get_address')
        await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")

@client.message_handler(state=MakeOrder.make_order, content_types=types.ContentTypes.TEXT)
async def send_order(message, state:FSMContext):
    await state.finish()
    try:

        if message.text == '✅Send Order':     
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
            text=f'Order:\nName:{name}\nPhone:{phone}\nAddress:{addres}\nTotal:{total}\n'
            await bot.send_message(message.chat.id, text='Thank you for your order!\nThe package will be delivered today from 20:00 to 23:00', reply_markup=mainkeyboard)
            await bot.send_message(197634497, text=f'новый заказ:\n{text}\nзаказали\n{order}')
          
            print('im finish!!!!!!!!!!!!!!')
              
            update_users(conn='',name=name,phone=phone,addres=addres,ord=text,user_id=message.chat.id)
            add_ord(conn='', user_id=message.chat.id, zakaz=text)
            person.rows[f'{message.chat.id}']=(message.chat.id, name, phone, addres, text)
            tm=time.ctime(time.time())
            all_orders.rows.insert(0,[message.chat.id, tm, text],header=f'{message.chat.id}')
            await init_customer_from_message(message)
        
            print('Now im realy finish!!!!!!')

        elif message.text == '⬅️Back': 
            addres=users[f'{message.chat.id}_person'].columns['addres'][f'{message.chat.id}']
            await bot.send_message(message.chat.id, text=f'Your address:\nNow: {addres}',reply_markup=keyboard_for_order)
            await MakeOrder.get_addres.set()

        else:
            await bot.send_message(message.chat.id, text='Press one of the buttons below', reply_markup=last_keyboard)
            await MakeOrder.make_order.set()
        
    except AttributeError:#NameError: 
        print('AttrErr Send_order')
        await bot.send_message(message.chat.id, text= "Oops, something is wrong🤭 let's start over, press /start")

#  #-------------------Protection from stupid messages---------------------------------------------------------------------------------   
@client.message_handler(content_types = ['voice'])
async def get_audio(message):
    await bot.send_chat_action(message.chat.id, 'upload_voice')
    aud = open('reqe.ogg', 'rb')   
    await bot.send_voice(chat_id=message.chat.id, voice=aud) 
    await bot.send_message(message.chat.id, text='You have a pleasant voice.\nNow press here /start', reply_markup=mainkeyboard)

@client.message_handler(content_types = ['photo'])
async def get_photo(message):
    await bot.send_message(message.chat.id, text="Look what I've got", reply_markup=mainkeyboard)
    await bot.send_chat_action(message.chat.id, 'upload_voice')
    ph = open('siski1.jpg', 'rb')   
    await bot.send_photo(message.chat.id, ph, caption="If you wanna see more /start")      

executor.start_polling(client)
 
# if __name__ =="__main__":