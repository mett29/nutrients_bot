import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from nutritionix.nutritionix import NutritionixClient
import json

nutritionix = NutritionixClient(
        application_id='<app-id>',
        api_key='<api-key>',
        # debug=True, # defaults to False
    )

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi! Send me the food you're searching for: ")


def echo(bot, update):
    
    dict = nutritionix.search(q=update.message.text, limit=2, offset=0, search_nutrient='calories')

    result = str(dict['results'][0]['nutrient_value']) + " kcal for " + str(dict['results'][0]['serving_qty']) + " g"

    bot.sendMessage(chat_id=update.message.chat_id, text=result)

    #print(json.dumps(dict, indent = 4))

def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("<API-KEY>")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(echo_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()




