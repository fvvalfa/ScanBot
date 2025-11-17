from telethon import TelegramClient, events,Button
from telethon.tl.types import PeerUser, ReplyKeyboardMarkup, ReplyInlineMarkup, KeyboardButton, KeyboardButtonRow
import os
from dotenv import load_dotenv
import time
conf = load_dotenv()
print(conf)

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]


absolute_path = os.path.dirname(__file__)
relative_path = "sessions"
session = os.path.join(absolute_path, relative_path,'session')

bot = TelegramClient(session, API_ID , API_HASH).start(bot_token= BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not isinstance(event.peer_id, PeerUser):
        await event.respond('Вам сюда нельзя')
        return
    keyboard_button = ReplyKeyboardMarkup(
        [
            KeyboardButtonRow(
                [
                    KeyboardButton(text="PDF цвет. 600dpi"),
                    KeyboardButton(text="PDF серый 600dpi"),
                    KeyboardButton(text="PDF ч/б. 600dpi")
                ]
            ),
            KeyboardButtonRow(
                [
                    KeyboardButton(text="PDF цвет. 300dpi"),
                    KeyboardButton(text="PDF серый 300dpi"),
                    KeyboardButton(text="PDF ч/б. 300dpi")
                ]
            ),
            KeyboardButtonRow(
                [
                    KeyboardButton(text="JPG цвет. 600dpi"),
                    KeyboardButton(text="JPG серый 600dpi"),
                    KeyboardButton(text="JPG ч/б. 600dpi")
                ]
            ),
            KeyboardButtonRow(
                [
                    KeyboardButton(text="JPG цвет. 300dpi"),
                    KeyboardButton(text="JPG серый 300dpi"),
                    KeyboardButton(text="JPG ч/б. 300dpi")
                ]
            )
        ]
    )
    await bot.send_message(
        entity=event.peer_id,
        message="Чтобы начать сканировать нажмите нужную кнопку",
        buttons=keyboard_button
        )
   # raise events.StopPropagation
color_dict={'цвет.':'Color', 'серый':'Gray', 'ч/б.':'Lineart'}
@bot.on(events.NewMessage(pattern="(PDF|JPG)"))
async def echo(event):
    """Echo the user message."""
    params = event.message.text.split(" ")
    format = params[0].lower()
    filename = time.strftime("%Y-%m-%d_%H-%M-%S")
    color = color_dict[params[1]] 
    dpi = params[2].split('dpi')[0]
    print(format, color, dpi)
    myCmd = f"scanimage --device=pixma:04A926B4_SD3009312367Q --resolution {dpi} --mode {color} --format {format} -l 0 -t 0 -x 210 -y 297 -o /srv/ScanBot/{filename}.{format}"
    os.system(myCmd)
    await bot.send_file(event.sender_id,f'/srv/ScanBot/{filename}.{format}')
    #await event.respond(myCmd)

def main():
    
    """Start the bot."""
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
#scanimage --device=pixma:04A926B4_SD3009312367Q --resolution 300 --mode Gray --format pdf -l 0 -t 0 -x 210 -y 297 -o /srv/ScanBot/file.pdf