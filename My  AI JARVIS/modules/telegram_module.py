"""
JARVIS Telegram Module
Bridge for mobile interaction and remote control
"""

import asyncio
import threading
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

class TelegramBridge:
    """Bridge between Telegram and JARVIS brain."""
    
    def __init__(self, brain_callback=None):
        self.token = TELEGRAM_TOKEN
        self.authorized_chat_id = TELEGRAM_CHAT_ID
        self.brain_callback = brain_callback
        self.app = None
        self.loop = None
        self.thread = None

    async def _start_async(self):
        """Internal async start method."""
        if not self.token:
            print("⚠️ Telegram token not found. Skipping Telegram Bridge.")
            return

        self.app = ApplicationBuilder().token(self.token).build()

        # Handlers
        start_handler = CommandHandler('start', self._start_command)
        msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self._handle_message)
        
        self.app.add_handler(start_handler)
        self.app.add_handler(msg_handler)

        print("🚀 Telegram Bridge is ready!")
        await self.app.initialize()
        await self.app.start_polling()
        
        # Keep it running
        while True:
            await asyncio.sleep(3600)
    
    async def _stop_async(self):
        """Internal async stop method."""
        if self.app:
            await self.app.stop()
            await self.app.shutdown()

    def start(self):
        """Start the Telegram bridge in a background thread."""
        if not self.token:
            return

        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()

    def _run_event_loop(self):
        """Run the asyncio event loop."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._start_async())

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        chat_id = str(update.effective_chat.id)
        if self.authorized_chat_id and chat_id != self.authorized_chat_id:
            await update.message.reply_text("⛔ Access Denied. This assistant is private.")
            return
            
        await update.message.reply_text(f"Hello Sir! JARVIS is online and ready for mobile commands. Your Chat ID is: {chat_id}")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Forward messages to JARVIS brain."""
        chat_id = str(update.effective_chat.id)
        
        # Authorization check
        if self.authorized_chat_id and chat_id != self.authorized_chat_id:
            await update.message.reply_text("⛔ Unauthorized access.")
            return

        user_text = update.message.text
        print(f"📱 Telegram Command: {user_text}")
        
        if self.brain_callback:
            # Execute the command via the brain
            response = self.brain_callback(user_text)
            if response:
                await update.message.reply_text(response)
        else:
            await update.message.reply_text("⚠️ JARVIS Brain is not connected.")

    def send_notification(self, message):
        """Send a proactive notification to the mobile device."""
        if self.app and self.authorized_chat_id and self.loop:
            asyncio.run_coroutine_threadsafe(
                self.app.bot.send_message(chat_id=self.authorized_chat_id, text=f"🔔 JARVIS Alert: {message}"),
                self.loop
            )

# Singleton instance
_bridge_instance = None

def get_telegram_bridge(brain_callback=None):
    """Get the singleton Telegram bridge instance."""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = TelegramBridge(brain_callback)
    return _bridge_instance
