import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from to_latex import imagify

class SmallHandler(Updater):
    def __init__(self, updater, dispatcher, own_id, bot_token):
        self.own_id = own_id
        self.token = bot_token
        self.updater = updater
        self.dispatcher = dispatcher

    def start_message(self):
        # welcome message
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

    def start(self, update, context):
        print("start")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Hoi, ich heisse printex. Ich bin en Hausgeist!")

    def logfile_sender(self):
        # sends the logfile to my_id
        logfile_handler = MessageHandler(filters=Filters.text(["/logfile"]), callback=self.send_logfile)
        self.dispatcher.add_handler(logfile_handler)

    def send_logfile(self, update, context):
        document = open('logfile.txt', 'rb')
        if update.effective_user['id'] == self.own_id:
            # logtxt = "sending logfile to user {}".format(update.effective_user.id)
            # logging.info(logtxt)
            context.bot.send_document(chat_id=update.effective_chat.id, document=document, disable_notification=True)
        document.close()

    def texify(self):
        # sends raw telegram input code to texify.tex
        texinput_normal_handler = MessageHandler(filters=Filters.text & (~Filters.command), callback=self.echo_latex_normal)
        texinput_edited_handler = MessageHandler(filters=Filters.update.edited_message & (~Filters.command), callback=self.echo_latex_edited)
        self.dispatcher.add_handler(texinput_edited_handler)
        self.dispatcher.add_handler(texinput_normal_handler)


    def echo_latex_normal(self, update, context):
        msg = update.message.text
        if imagify(msg):
            with open("usercode.png", "rb") as f:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)
        os.chdir('../')

    def echo_latex_edited(self, update, context):
        msg = update.edited_message.text
        if imagify(msg):
            with open("usercode.png", "rb") as f:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)
        os.chdir('../')




