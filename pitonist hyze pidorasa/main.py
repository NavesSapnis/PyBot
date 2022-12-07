from time import *
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import requests
from bs4 import BeautifulSoup 
import emoji
from string import * 
import requests, json
import pyimgur
import urllib.parse
import urllib.request
import lxml
import top10
import webbrowser
import random
from states import Find
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from Api_and_cfg import *


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()


dp = Dispatcher(bot,storage=storage)



@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    global pic_i
    pic_i=int(pic_i)
    await message.photo[-1].download(f'pictures\\test.jpg')
    await message.photo[-1].download(f'archive\picture{pic_i}.jpg')
    pic_i+=1
    pic_i=str(pic_i)
    with open("config\pic_i.txt", "w") as f:
        f.write(pic_i)
    try:
        im=pyimgur.Imgur(CLIENT_ID)
        uploaded_image=im.upload_image(path,title="test")
        url_test=(uploaded_image.link)
        urlParse = urllib.parse.urlparse(url_test)
        sc="https://yandex.ru/images/search?source=collections&rpt=imageview&url="+uploaded_image.link
        url = sc

        r = requests.get(url)
        sp = BeautifulSoup(r.content,'lxml')
        pictures = sp.findAll('div', class_='JustifierRowLayout-Item')
        i=0
        for picture in pictures:
            if i>=5:
                break
            s=str(picture)
            first=s.find('url(//')
            last=s.find(')\"></div>')
            full=(s[(first+6):last])
            img = requests.get("http://"+full)
            with open('pictures\pic.jpg', 'wb') as file:
                file.write(img.content)
            with open("pictures\pic.jpg","rb") as photo_ans:
                await bot.send_photo(message.chat.id,photo=photo_ans)
            i+=1
    except:
        pass


@dp.message_handler(state=Find.step1)
async def step1(message: types.Message, state:FSMContext):
    if message.text.lower()!='back'+emoji.emojize(":door:"):
        try:
            i=0
            s = requests.session()
            r = s.get(f'https://yandex.by/images/search?from=tabbar&text={message.text}')

            soup = BeautifulSoup(r.text, "html.parser")

            for text in soup.findAll(attrs={'class': 'serp-item__thumb justifier__thumb'}):
                url = "http:"+text.get('src')
                img = requests.get(url)
                with open('pictures\pic.jpg', 'wb') as file:
                    file.write(img.content)
                with open("pictures\pic.jpg","rb") as photo_ans:
                    await bot.send_photo(message.chat.id,photo=photo_ans)
                i+=1
                if i==5:
                    break
                else:
                    pass
        except:
            pass
    else:
        button1 = KeyboardButton('find'+emoji.emojize(":star_of_David:"))
        button2 = KeyboardButton('info'+emoji.emojize(":star:"))
        button3 = KeyboardButton('money'+emoji.emojize(":eyes:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row(button1,button2,button3)
        await message.answer("Вы вернулись в главное меню", reply_markup=markup1)
        await state.finish()



@dp.message_handler(state=Find.step2)
async def step2(message: types.Message, state:FSMContext):
    if message.text.lower()=='go'+emoji.emojize("📈"):
        top10.get_cur()
        await bot.send_document(message.chat.id, open("config\\top.txt", 'rb'))
        button1 = KeyboardButton('find'+emoji.emojize(":star_of_David:"))
        button2 = KeyboardButton('info'+emoji.emojize(":star:"))
        button3 = KeyboardButton('money'+emoji.emojize(":eyes:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row(button1,button2,button3)
        await message.answer("Вы вернулись в главное меню", reply_markup=markup1)
        await state.finish()


    elif message.text.lower()=='back'+emoji.emojize(":door:"):
        button1 = KeyboardButton('find'+emoji.emojize(":star_of_David:"))
        button2 = KeyboardButton('info'+emoji.emojize(":star:"))
        button3 = KeyboardButton('money'+emoji.emojize(":eyes:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row(button1,button2,button3)
        await message.answer("Вы вернулись в главное меню", reply_markup=markup1)
        await state.finish()
    
    else:
        bot.send_message(message.chat.id,"Выбери")


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.lower()=='start' or message.text.lower()=='/start':
        button1 = KeyboardButton('find'+emoji.emojize(":star_of_David:"))
        button2 = KeyboardButton('info'+emoji.emojize(":star:"))
        button3 = KeyboardButton('money'+emoji.emojize(":eyes:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row(button1,button2,button3)
        await message.answer("Вы вернулись в главное меню", reply_markup=markup1)

    elif message.text.lower()=='/help' or message.text.lower()=='help':
        await bot.send_message(message.chat.id,"""Написав "start" вы попадете в главное меню,
        далее вы сожете выбрать что вас инетересует нажимая на соответсвующую кнопку\nFind - найти картинки по запросу
        \ninfo - получить информацию по боту\nMoney - Получить txt файл с топ-10 криптовалютами
        \nТак же вы можете отправить мне картинки и я отправлю вам похожие""")


    elif message.text.lower()=='info'+emoji.emojize(":star:") or message.text.lower()=='info' or message.text.lower()=="/info":
        keys=["Утречка","Шалом","Вечер в хату","Хелоу","Привет","Добрый вечер","Ку","Кулити","Добрый день","Здарова"]
        i=random.randint(0,9)
        await bot.send_message(message.chat.id, f"""{keys[i]} меня зовут Олег, но создатель зовет меня выродок, вот вам список команд,
        возможно будет интересно \n"start" - напишите чтобы появилось меню\n"help" - помощь по меню
        \nИли просто отправьте мне картинку чтобы я прислал вам похожих\nКонтакты разработчика - https://t.me/Naves_Sapnis""")

    elif message.text.lower()=='money'+emoji.emojize(":eyes:"):
        button1 = KeyboardButton('back'+emoji.emojize(":door:"))
        button2 = KeyboardButton('go'+emoji.emojize("📈"))
        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)  
        markup3.row(button1,button2)
        await bot.send_message(message.chat.id,"Вы точно хотите получить этот список ? (процесс ожидания составит примерно 1-2 минуты)",reply_markup=markup3)
        await Find.step2.set()
        
    elif message.text.lower()=="find"+emoji.emojize(":star_of_David:"):
        button1 = KeyboardButton('back'+emoji.emojize(":door:"))
        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)  
        markup3.row(button1)
        await message.answer("Напишите запрос на картинку или же выйдите", reply_markup=markup3)
        await Find.step1.set()

    else:
        await bot.send_message(message.chat.id,"""Не разумею вас напишите /info""")

    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  