
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from traceback import print_exc
import cloudmersive_ocr_api_client
from telegram import Update, Bot, ParseMode
from cloudmersive_ocr_api_client.rest import ApiException
import json
CLOUDMERSIVE_API_KEY="enter your cloudmersive api key here"
# Configure API key authorization: Apikey
configuration = cloudmersive_ocr_api_client.Configuration()
configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!\n\nWelcome to Optical character recognition Bot\n\n-->what can this bot do?\n\n-->I can read texts from images and send it to you!\n\nJust send a clear image to me and I will recognize the text in the image and send it as message!!")



def search(update, context):
    filename = "test.jpg"
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    print(update.message.photo)
    newFile.download(filename)
    update.message.reply_text("I got your image...\nJust wait few seconds...")
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY
    try:
        api_response = api_instance.image_ocr_post(filename)
        print(api_response)
        update.message.reply_text('`'+str(api_response.text_result)+'`',parse_mode=ParseMode.MARKDOWN,reply_to_message_id=update.message.message_id)


    except Exception as e:
        print_exc()
        update.message.reply_text("error occured"+e)


def main():
    updater = Updater("enter your bot-token here", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, search))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
