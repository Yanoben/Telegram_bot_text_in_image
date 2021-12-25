import pytesseract
from PIL import Image
import os
import telebot
from dotenv import load_dotenv
from bot_transitions import Bot_transition
import time
import logging


load_dotenv()

token = os.getenv('token')

bot = telebot.TeleBot(token)
bot_tran = Bot_transition()

languages = {
    'method_english': 'English',
    'method_russian': 'Русский'
}


def image_to_text(image, lang):
    if lang == 'Русский':
        result = pytesseract.image_to_string(
            Image.open(image).convert("RGB"), lang='rus')
    elif lang == 'English':
        result = pytesseract.image_to_string(
            Image.open(image).convert("RGB"), lang='eng')
    return result


def get_files(path):
    files = []

    directory = os.listdir(path)
    directory.sort(reverse=True)

    for file in directory:
        if file.endswith('.jpg'):
            files.append(file)
    return files


@bot.message_handler(commands=['start', 'restart'])
def start(message):
    bot_tran.new()
    rmk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(telebot.types.KeyboardButton('English'),
            telebot.types.KeyboardButton('Русский'))
    bot.send_message(
        message.chat.id,
        'Hello! I am Bot and I can make text from a picture/photo/image')
    time.sleep(1)
    message = bot.send_message(
        message.chat.id, 'Please choose language for text', reply_markup=rmk)
    bot.register_next_step_handler(message, get_lang)


@bot.message_handler(content_types=['str', 'text'])
def get_lang(message):
    if message.text.lower() == 'english':
        bot_tran.english()
    elif message.text.lower() == 'русский':
        bot_tran.russian()
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Give me photo/image/picture',
                     reply_markup=a)
    bot.register_next_step_handler(message, get_image)


@bot.message_handler(content_types=['photo', 'text'])
def get_image(message):
    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        name = raw+".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)
        img = open(name, 'rb')
        text = image_to_text(img, languages.get(bot_tran.state))
        bot.send_message(message.chat.id, text)
        path = os.path.dirname(os.path.realpath(__file__))
        files = get_files(path)
        for f in files:
            os.remove(os.path.join(path, f))
    elif message.content_type == 'text':
        bot.send_message(message.chat.id, 'I cant talking, so give me image))')


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    try:
        bot.infinity_polling()
    except Exception:
        pass


if __name__ == '__main__':
    main()
