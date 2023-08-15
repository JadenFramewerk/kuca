import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from plate import token

bot_token = token  # Replace with your actual bot token from the BotFather
chat_id = '900448027'

file_ku = 'output.txt'
file_bin = 'p2p_data.txt'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Asynchronous function to read file contents and send it to the specified chat_id in chunks
async def send_large_message(chat_id, message_content):
    max_message_length = 4096  # Adjust this value based on your platform's message size limit

    # Split the message_content into chunks of max_message_length
    chunks = [message_content[i:i + max_message_length] for i in range(0, len(message_content), max_message_length)]

    for chunk in chunks:
        await bot.send_message(chat_id, chunk)

async def send_file_content():
    with open(file_ku, 'r', encoding='utf-8') as file_k:
        content_k = file_k.read()
    with open(file_bin, 'r', encoding='utf-8') as file_b:
        content_b = file_b.read()

    # Send the content of file_ku first
    await send_large_message(chat_id, "KUCOIN FINANCE STATS:\n")
    await send_large_message(chat_id, content_k)

    # Send the content of file_bin next
    await send_large_message(chat_id, "\n\nBINANSE FINANCE STATS:\n")
    await send_large_message(chat_id, content_b)

# Asynchronous function to schedule the sending of file content every minute
async def schedule_send_file_content():
    while True:
        await send_file_content()
        await asyncio.sleep(60)  # 60 seconds = 1 minute

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_send_file_content())
    executor.start_polling(dp, skip_updates=True)
