from telethon import TelegramClient, events
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]


absolute_path = os.path.dirname(__file__)
relative_path = "sessions"
session = os.path.join(absolute_path, relative_path,'session')

bot = TelegramClient(session, API_ID , API_HASH).start(bot_token= BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Привет как дела')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    """Echo the user message."""
    await event.respond(event.text)

def main():
    """Start the bot."""
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()