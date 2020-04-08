# coding: utf-8
import requests
import configparser
import telegram
import json
# from telegram import Update
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters
from fugle_realtime import intraday
from reply_tool import ReplyTool as rp

config = configparser.ConfigParser()
config.read('config.ini')
access_token = config['TELEGRAM']['ACCESS_TOKEN']
webhook_url = config['TELEGRAM']['WEBHOOK_URL']
app = Flask(__name__)
bot = telegram.Bot(token=config['TELEGRAM']['ACCESS_TOKEN'])


def set_webhook():
    res = requests.post('https://api.telegram.org/bot' + access_token + '/setWebhook?url=' + webhook_url + '/hook').text
    print(json.loads(res)['description'])


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        raw_res = request.get_json(force=True)
        update = telegram.Update.de_json(raw_res, bot)
        dispatcher.process_update(update)

    return 'ok'


## reply message
def reply_handler(bot, update):
    text = update.message.text
    text = text_helper(text)
    user_id = update.message.from_user.name
    update.message.reply_text(text)


def text_helper(input_text: str) -> str:
    try:
        msg = rp.reply_helper(input_text)
        return msg
    except Exception as e:
        print(e)
        msg = 'Oops, 出了點狀況，我先下班了，改天再來找我 ~'
        return msg


# This class dispatches all kinds of updates to its registered handlers.
dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == '__main__':
    set_webhook()
    app.run()
