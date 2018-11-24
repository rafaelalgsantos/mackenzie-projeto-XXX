# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler
from urllib.request import urlopen
import traceback

blynk_url = 'http://blynk-cloud.com/'
blynk_token = '84313df847c6411d9fa0e090639e9385'
url = blynk_url + blynk_token
telegram_token = '670562854:AAHl04ZuNmP_XxxG7zmDrVG10_1MTSbVVWM'

def is_hardware_connected(bot, update):
    try:
        handle = urlopen(url + '/isHardwareConnected')
        status = handle.read()
        handle.close()
        print(status)
        if bool(status) == True:
            return True
        reply_text = u"O hardware não está conectado."
        update.message.reply_text(reply_text, quote=True)
        return False
    except:
        traceback.print_exc()
        return False

def solenoid_lock(bot, update):
    try:
        if not is_hardware_connected(bot, update):
            return
        try:
            action = update.message.text.strip().split()[1].lower()
        except:
            action = None
        
        if action == "abrir":
            urlopen(url + '/update/V0?value=0')
            update.message.reply_text(u"A fechadura está aberta!", quote=True)
        elif action == "fechar":
            urlopen(url + '/update/V0?value=1')
            update.message.reply_text(u"A fechadura está fechada!", quote=True)
        else:
            update.message.reply_text(u"Não entendi o que você disse, pode repetir? Suas opções \
            são /fechadura abrir ou /fechadura fechar", quote=True)
    except:
        traceback.print_exc()

updater = Updater(token=telegram_token)
updater.dispatcher.add_handler(CommandHandler('fechadura', solenoid_lock))
updater.start_polling()
updater.idle()