import asyncio
import logging
from telegram import Bot #type: ignore
from telegram.error import TelegramError #type: ignore

class TelegramAlertBot:
    def __init__(self, token: str, user_id: str, merge_pattern: str = None):
        self.token = token
        self.user_id = user_id
        self.message_queue = asyncio.Queue()
        self.merge_pattern = merge_pattern
        self.last_message = None
        self.last_message_id = None
        
    async def send_telegram_message(self, message: str):
        bot = Bot(token=self.token)
        try:
            # Check if message merging is enabled and if the message matches the pattern
            if self.merge_pattern and message.startswith(self.merge_pattern):
                if self.last_message and self.last_message.startswith(self.merge_pattern):
                    # Extract timestamps from both messages
                    current_end_time = message.split(" and ")[1].split(".")[0]
                    last_start_time = self.last_message.split("between ")[1].split(" and ")[0]
                    
                    # Create merged message
                    merged_message = f"{self.merge_pattern} {last_start_time} and {current_end_time}."
                    if "@" in message:
                        merged_message += f"\n{message.split('\n')[1]}"
                    
                    # Edit the last message instead of sending a new one
                    await bot.edit_message_text(
                        chat_id=self.user_id,
                        message_id=self.last_message_id,
                        text=merged_message
                    )
                    self.last_message = merged_message
                    logging.info(f"Edited message: {merged_message}")
                    return
                    
            # If merging is disabled or messages don't match pattern, send as new message
            sent_message = await bot.send_message(chat_id=self.user_id, text=message)
            self.last_message = message
            self.last_message_id = sent_message.message_id
            logging.info(f"Sent message: {message}")
            
        except TelegramError as e:
            logging.error(f"Error handling message: {e}")

    async def background_bot_polling(self):
        logging.info("Starting Telegram bot polling...")
        while True:
            message = await self.message_queue.get()
            if message:
                await self.send_telegram_message(message)
            self.message_queue.task_done()

    async def event_trigger(self, message: str, bot: str):
        message += f"\n@{bot}"
        logging.info(f"Event triggered! Queueing message: {message}")
        await self.message_queue.put(message) 