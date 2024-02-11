import os, time
from display_progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen

BOT_TOKEN = ""
API_ID = ""
API_HASH = ""

Bot = Client(
    "Thumb-Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}, I am video thumbnail changer Bot.

Send a video/file to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb/thumb-change-bot'),
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


# global variable to store path of the recent sended thumbnail
thumb = ""

@Bot.on_message(filters.private & (filters.video | filters.document))
async def thumb_change(bot, m):
    global thumb
    msg = await m.reply("`Downloading..`")
    c_time = time.time()
    file_dl_path = await bot.download_media(message=m, progress=progress_for_pyrogram, progress_args=("Downloading file..", msg, c_time))
    await msg.delete()
    answer = await bot.ask(m.chat.id,'Now send the thumbnail' + ' or /keep to keep the previous thumb' if thumb else '', filters=filters.photo | filters.text)
    if answer.photo:
        try:
            os.remove(thumb)
        except:
            pass
        thumb = await bot.download_media(message=answer.photo)
    msg = await m.reply("`Uploading..`")
    c_time = time.time()
    if m.document:
        await bot.send_document(chat_id=m.chat.id, document=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    elif m.video:
        await bot.send_video(chat_id=m.chat.id, video=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    await msg.delete()
    os.remove(file_dl_path)



Bot.run()
