import configure
import telebot
import urllib
from telebot import types
from telebot import TeleBot
from base import up_cocktail
from base import init_user
from base import add_user
from beautifultable import BeautifulTable
 
#https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B

client=telebot.TeleBot(configure.config['token'])

#Таблица корзины
global basket
basket=BeautifulTable()
basket.columns.header = ["name", "url", "amount", "price"]

global n
n=0

url = 'https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
f = open('out.jpg','wb')
f.write(urllib.request.urlopen(url).read())
f.close()


#mainekeyboard
mainkeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
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
    next_button = types.InlineKeyboardButton(text='▶️', callback_data= 'next')
    back_button = types.InlineKeyboardButton(text='◀️', callback_data = 'back')
    showitem_button = types.InlineKeyboardButton(text=f'{showitem}', callback_data='nts')
    start_order = types.InlineKeyboardButton(text=f'✅Оформить заказ {total} NIS', callback_data='order')
    back_to_menu = types.InlineKeyboardButton(text='🍸Продолжить покупку', callback_data='main')

    basket_keyboard.row(delete_button,less_button,count_items,more_button)
    basket_keyboard.row(back_button, showitem_button, next_button)
    basket_keyboard.add(start_order,back_to_menu)
    return basket_keyboard

def basket_iter(n,call):
   
    item=basket[n][0]
    showitem=f'{n+1}/{len(basket.rows)}'
    total=sum(list(basket.columns['price']))
    count_items=basket.rows[item]['amount']
    bas_url=basket.rows[item]['url'] 
    name= basket.rows[item]['name']        
    text=f'{name} [_]({bas_url})'
    basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)

    return client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')
#def add_less_item(call):

#----------------------------------------------------------------------------------------------------------------------------#

@client.message_handler(commands=['start'])
def welcome (message):
    #приветствие и основное меню внизу
    client.send_chat_action(message.chat.id, 'upload_photo')
    img = open('out.jpg', 'rb')   
    url='https://scontent.ftlv1-1.fna.fbcdn.net/v/t1.0-9/126903084_166685105188559_8109647350154471887_o.jpg?_nc_cat=105&ccb=2&_nc_sid=e3f864&_nc_ohc=d9xEBNdQ7kMAX81gdwG&_nc_ht=scontent.ftlv1-1.fna&oh=5de60ff811edb764f388dfbffed63fad&oe=5FFA7B7B'
    client.send_photo(message.chat.id, img, reply_to_message_id="Б",caption='Добро пожаловать!',reply_markup=mainkeyboard)  

@client.callback_query_handler(func = lambda call:True)
def get_call(call):
    if call.data=='main':
         client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=cocktailkeyboard,text='Рады предложить вам, следующие виды напитков:')

    if call.data =='sig':
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

    m=up_cocktail(conn='',tip='sig')
    for cocktail in m:
        cocktail_name=cocktail['name']
        name_h=f'0.5L {cocktail_name}'
        name_t=f'0.3L {cocktail_name}'   
        cocktail_photo=cocktail['url_photo']
        price_h=cocktail['price05']
        price_t=cocktail['price03']  
        if call.data == name_h:
            if name_h  in basket.rows.header:
                basket.rows[name_h]['amount']+=1
                basket.rows[name_h]['price']+=price_h
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
              
            else:          
                basket.rows.append([name_h,cocktail_photo,1,price_h],header=name_h)
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
               
        if call.data == name_t:
            if name_t  in basket.rows.header:
                basket.rows[name_t]['amount']+=1
                basket.rows[name_t]['price']+=price_t
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину') 
               
            else:        
                basket.rows.append([name_t,cocktail_photo,1,price_t],header=name_t)
                client.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'{cocktail_name} добавлен в корзину')   
               
    # if call.data =='clas':
    #     client.send_message(call.message.chat.id, 'ахуенный коктейль2', reply_markup=trade_keyboard)
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
        if len(basket.rows)==0:
            client.send_message(call.message.chat.id, 'empty')    
        else: 
            global n
            n=0
            showitem=f'{n+1}/{len(basket.rows)}'
            item=basket[n][0]
            total=sum(list(basket.columns['price']))
            count_items=basket.rows[item]['amount']
            bas_url=basket.rows[item]['url']
            name= basket.rows[item]['name']
            text=f'{name}[_]({bas_url})'    
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(call.message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
            print(basket)
#---------------Basket_iter---------------------------------------------------------------------------------------------=================
    if call.data == 'next':
        n+=1
        if n>len(basket.rows)-1:
            n-=1
            basket_iter(n=n,call=call)
        else:
            basket_iter(n=n,call=call)        
    
    if call.data == 'back':
        n=n-1
        if n<0:
            n+=1
            basket_iter(n=n,call=call)
        else:
            basket_iter(n=n,call=call)      

    if call.data=='more':
        item=basket[n][0]
        basket.rows[item]['price']+=basket.rows[item]['price']/basket.rows[item]['amount']
        basket.rows[item]['amount']+=1
        showitem=f'{n+1}/{len(basket.rows)}'
        total=sum(list(basket.columns['price']))
        count_items=basket.rows[item]['amount']
        bas_url=basket.rows[item]['url']
        name= basket.rows[item]['name']
        
        text=f'{name}[_]({bas_url})'    
        basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
        client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')

    if call.data=='less':
        item=basket[n][0]
        price_item=basket.rows[item]['price']/basket.rows[item]['amount']
        basket.rows[item]['amount']-=1
        if basket.rows[item]['amount']==0:
            basket.rows[item]['amount']+=1
            basket.rows[item]['price']+=price_item
        basket.rows[item]['price']-=price_item
        showitem=f'{n+1}/{len(basket.rows)}'
        total=sum(list(basket.columns['price']))
        count_items=basket.rows[item]['amount']
        bas_url=basket.rows[item]['url']
        name= basket.rows[item]['name']
        text=f'{name}[_]({bas_url})'    
        basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
        client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')
    
    if call.data =='del':
        #item=basket[n][0]
        del basket.rows[n]
        if len(basket.rows)==0:
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=cocktailkeyboard,text='Корзина пуста, выберете что нибудть')
        else:
            n-=1   
            item=basket[n][0]
            showitem=f'{n+1}/{len(basket.rows)}'
            total=sum(list(basket.columns['price']))
            count_items=basket.rows[item]['amount']
            bas_url=basket.rows[item]['url']
            name= basket.rows[item]['name']
            text=f'{name}[_]({bas_url})'            
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=basket_keyboard,text=text, parse_mode='Markdown')



@client.message_handler(content_types = ['text'])
def get_text(message):
    if message.text=='🍴Меню🍴' or message.text=='🍴Вернуться🍴':
        client.send_message(message.chat.id,'Рады предложить вам следующие типы напитков:', reply_markup= cocktailkeyboard)
    
    elif message.text == '🛍Корзина🛍':
        if len(basket.rows)==0:
            client.send_message(message.chat.id, 'empty')    
        else: 
            global n
            n=0
            showitem=f'{n+1}/{len(basket.rows)}'
            item=basket[n][0]
            total=sum(list(basket.columns['price']))
            count_items=basket.rows[item]['amount']
            bas_url=basket.rows[item]['url']
            name= basket.rows[item]['name']
            text=f'{name}[_]({bas_url})'           
            basket_keyboard=basket_test(count_items=count_items,showitem=showitem,total=total)
            client.send_message(message.chat.id, text= text,reply_markup=basket_keyboard, parse_mode='Markdown')
         
    elif message.text == '💁🏻‍♀️О нас💁🏻‍♀️':
        client.send_message(message.chat.id, 'Мы типо пипeц душевные ебать профессионльные\nты будешь доволен, счастлив и прекрасен')
    elif message.text == '🧳Заказы🧳':
         client.send_message(message.chat.id, 'ты заказал вот эту штуку, она по дроге к тебе')
    else:
        client.send_message(message.chat.id,'Выбери что-нибудть там внизу:⤵️ ')
    
client.polling(none_stop= True, interval=0)

# if __name__ =="__main__":
#     print (basket)
#     print (basket[0]['name'])
#     sumtest = 1
#     print (basket[0]['amount']+basket[1]['amount'])