import telebot
from cfg import *
import MukeshAPI
import gtts
import glob
import time


def gen_img(msg):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    try:
        img = MukeshAPI.api.ai_image(msg.text)
        msg = bot.send_photo(msg.chat.id, img, msg.text)
    except:
        msg = bot.send_message(msg.chat.id,"Не удалось отправить изображение")
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к изображениям", callback_data=START_BTNS[0][1])
    keyboard.add(btns)
    bot.send_message(msg.chat.id,"Отправьте запрос",reply_markup=keyboard)
    bot.register_next_step_handler(msg, gen_img)

def send_img(msg):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    try:
        msg = bot.send_photo(msg.chat.id, msg.text)
    except Exception as ex:
        msg = bot.send_message(msg.chat.id,f"Не удалось отправить изображение: {ex}")
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к изображениям", callback_data=START_BTNS[0][1])
    keyboard.add(btns)
    bot.send_message(msg.chat.id,"Отправьте ссылку",reply_markup=keyboard)
    
    bot.register_next_step_handler(msg, send_img)
        
@bot.callback_query_handler(func=lambda call: call.data == IMG_BTNS[1][1])
def link(call:telebot.types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к изображениям", callback_data=START_BTNS[0][1])
    keyboard.add(btns)
    bot.send_message(msg.chat.id,"Отправьте ссылку",reply_markup=keyboard)
    
    bot.register_next_step_handler(msg, send_img)

@bot.callback_query_handler(func=lambda call: call.data == IMG_BTNS[0][1])
def genimg(call:telebot.types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к изображениям", callback_data=START_BTNS[0][1])
    keyboard.add(btns)
    bot.edit_message_text("Отправьте запрос", msg.chat.id,msg.id,reply_markup=keyboard)
    bot.register_next_step_handler(msg, gen_img)
# image
@bot.callback_query_handler(func=lambda call: call.data == START_BTNS[0][1])
def image_btn(call:telebot.types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in IMG_BTNS]
    keyboard.add(*buttons)
    bot.edit_message_text("Работа с изображением", msg.chat.id,msg.id,reply_markup=keyboard)
"""IMAGE END"""


"""AUDIO START"""
def send_audio(msg:telebot.types.Message):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    audio = audio_yt(msg.text.replace(" ","+"))
    try:
        bot.send_audio(chat_id=msg.chat.id,audio=audio[0])
    except Exception as ex:
        bot.send_message(msg.chat.id,f"Не удалось отправить аудио: {ex}")
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к аудио", callback_data=START_BTNS[1][1])
    keyboard.add(btns)
    bot.send_message(msg.chat.id,"Отправьте запрос",reply_markup=keyboard)
    bot.register_next_step_handler(msg, send_audio)

@bot.callback_query_handler(func=lambda call: call.data == AUDIO_BTNS[1][1])
def audios(call:telebot.types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    msg = call.message

    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к аудио", callback_data=START_BTNS[1][1])
    keyboard.add(btns)
    bot.edit_message_text("Отправьте запрос", msg.chat.id,msg.id,reply_markup=keyboard)
    bot.register_next_step_handler(msg, send_audio)


def gen_audio(msg:telebot.types.Message):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    try:
        tts = gtts.gTTS(text=msg.text, lang='en')
        tts.save("req.mp3")
        with open("req.mp3","rb") as f: bot.send_audio(chat_id=msg.chat.id,audio=f)
    except Exception as ex:
        bot.send_message(msg.chat.id,f"Не удалось отправить аудио: {ex}")
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к аудио", callback_data=START_BTNS[1][1])
    keyboard.add(btns)
    bot.send_message(msg.chat.id,"Отправьте text-to-speech",reply_markup=keyboard)
    bot.register_next_step_handler(msg, gen_audio)
    

@bot.callback_query_handler(func=lambda call: call.data == AUDIO_BTNS[0][1])
def tts_audio(call:telebot.types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    btns = telebot.types.InlineKeyboardButton(text="Назад к аудио", callback_data=START_BTNS[1][1])
    keyboard.add(btns)
    bot.edit_message_text("Отправьте text-to-speech", msg.chat.id,msg.id,reply_markup=keyboard)
    bot.register_next_step_handler(msg, gen_audio)

@bot.callback_query_handler(func=lambda call: call.data == START_BTNS[1][1])
def audio_btn(call:telebot.types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in AUDIO_BTNS]
    keyboard.add(*buttons)
    bot.edit_message_text("Работа с аудио", msg.chat.id,msg.id,reply_markup=keyboard)
"""AUDIO END"""
"""REP START"""
@bot.callback_query_handler(func=lambda call: call.data == START_BTNS[2][1])
def scource_btn(call:telebot.types.CallbackQuery):
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text="Перейти в репозиторий", url=REP_URL), telebot.types.InlineKeyboardButton(text="Назад на главную", callback_data="back_to_main")]
    keyboard.add(*buttons)
    bot.edit_message_text(REP_URL, msg.chat.id,msg.id,reply_markup=keyboard)
"""REP END"""
@bot.message_handler(commands=["start"])
def start(msg:telebot.types.Message):
    chat_id = msg.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in START_BTNS]
    keyboard.add(*buttons)
    return bot.send_message(chat_id,
                            START_MSG,
                            reply_markup= keyboard)

@bot.callback_query_handler(func=lambda call: call.data == AUDIO_BTNS[2][1])
def to_main(call:telebot.types.CallbackQuery):
    msg=call.message
    chat_id = msg.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in START_BTNS]
    keyboard.add(*buttons)
    return bot.edit_message_text(START_MSG, chat_id,msg.id,reply_markup= keyboard)
# @bot.message_handler(content_types=START_BTNS)
# def
bot.polling()