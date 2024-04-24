from telegram import Update , Bot , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ContextTypes , Application , CommandHandler , MessageHandler , filters , CallbackQueryHandler , InlineQueryHandler
import asyncio
import os 
import warnings
warnings.filterwarnings(action="ignore", category=DeprecationWarning)

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
Webhook_url = os.environ.get('Webhook_url', False)


print('Starting up bot...')

async def setwebhhok():
    try:await bot.set_webhook(Webhook_url + TOKEN)
    except Exception as e:print(e)
        
async def start_command(update: Update, context):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')
  
def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text('Try typing anything, and I will do my best to respond.')

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        if query.data == '1':
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Button 2", callback_data='2'), InlineKeyboardButton("Button 3", callback_data='3')]])
            await query.edit_message_text(text=f'You selected 1',reply_markup=reply_markup)
        if query.data == '2':
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 3", callback_data='3')]])
            await query.edit_message_text(text=f'You selected 2',reply_markup=reply_markup)
        if query.data == '3':
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 2", callback_data='2')]])
            await query.edit_message_text(text=f'You selected 3',reply_markup=reply_markup)
    except Exception as e:
        print("Error while editing message : ",e)

async def handle_messages(update: Update,context: ContextTypes.DEFAULT_TYPE):
    text = "Here are some Buttons"
    keyboard = [[InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 2", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:await context.bot.send_message(chat_id=update.message.chat_id,text=text,reply_markup=reply_markup)
    except Exception as e:print("Error while sending message : ",e)

def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def main(update: Update,context: ContextTypes.DEFAULT_TYPE):
    if Webhook_url and Webhook_url != 'False':
        await setwebhhok()
    else:
        print("Webhook url not found , running normal polling....\n\nApp will stop because currently running as web service")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    bot = Bot(TOKEN)
    loop = asyncio.get_event_loop()
    loop.create_task(main(Update, context=app))

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT , handle_messages))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_error_handler(error)
    print('Polling...')
    if Webhook_url and Webhook_url != 'False':
        app.run_webhook(
            port=PORT,
            listen="0.0.0.0",
            webhook_url=Webhook_url
        )
    else:
        app.run_polling(poll_interval=0)
    
    

    
