import os
import pytesseract
import requests
from PIL import Image
from pyrogram import Client, filters , enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageEmpty
from pyromod import listen
import cv2

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


BOT_TOKEN = os.environ.get("BOT_TOKEN","6117968672:AAGiHeEHZt7MRIXs7jxctixEdatrY3svVvk")
API_ID = os.environ.get("API_ID",17983098)
API_HASH = os.environ.get("API_HASH","ee28199396e0925f1f44d945ac174f64")

Bot = Client(
    "OCRBot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
السلام عليكم يا  {}
أنا بوت تفريغ الصفحات . فقط أرسل الصفحة / الصورة بدون ضغط للحفاظ على الجودة( مستحسن)
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('بقية البوتات', url='https://t.me/sunnay6626/2'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.photo | filters.document)
async def ocr(bot, msg):
    lang_code = "ara"
    data_url = f"https://github.com/tesseract-ocr/tessdata/raw/main/{lang_code}.traineddata"
    dirs = r"/usr/share/tesseract-ocr/4.00/tessdata"
    path = os.path.join(dirs, f"{lang_code}.traineddata")
    if not os.path.exists(path):
        data = requests.get(data_url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
        if data.status_code == 200:
            open(path, 'wb').write(data.content)
        else:
            return await msg.reply("`Either the lang code is wrong or the lang is not supported.`", parse_mode=enums.ParseMode.MARKDOWN)
    message = await msg.reply("`Downloading and Extracting...`", parse_mode=enums.ParseMode.MARKDOWN)
    image = await msg.download(file_name=f"text_{msg.from_user.id}.jpg")    
    img = Image.open(image)
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(img, lang=f"{lang_code}")
    try:
        await msg.reply(text[:-1], quote=True, disable_web_page_preview=True)
    except MessageEmpty:
        return await msg.reply("`Either the image has no text or the text is not recognizable.`", quote=True, parse_mode=enums.ParseMode.MARKDOWN)
    await message.delete()
    os.remove(image)


    
Bot.run()
