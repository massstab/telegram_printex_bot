#!/usr/bin/env python

import time
import subprocess
from uuid import uuid4
from telegram import InlineQueryResultCachedPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler


def imagify(usercode):
    """
    Compiles the sends queries from the telegram user to a latex pdf and converts it to a jpg image.
    :param usercode: The LaTeX code to compile
    :return: Return True if the code was compiled without an error and False otherwise.
    """
    head = r"\documentclass[varwidth, border=1]{standalone}" \
           r"\begin{document}"
    tail = r"\end{document}"
    main = head + usercode + tail
    with open('tex/usercode.tex', 'w') as f:
        f.write(main)
    code = subprocess.call(['pdflatex', '-halt-on-error', '-output-directory', 'tex', 'tex/usercode.tex'])
    if code == 0:
        subprocess.call(['convert', '-density', '600', '-bordercolor', 'white', '-border', '0', 'tex/usercode.pdf',
                         'tex/usercode.jpg'])
        return True
    else:
        return False


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
        """
        Creates the handlers and adds them to the dispatcher
        :return:
        """
        texinput_normal_handler = MessageHandler(filters=Filters.text, callback=self.echo_latex_normal)
        texinput_edited_handler = MessageHandler(filters=Filters.update.edited_message, callback=self.echo_latex_edited)
        texinput_inline_handler = InlineQueryHandler(callback=self.echo_latex_inline)

        self.dispatcher.add_handler(texinput_edited_handler)
        self.dispatcher.add_handler(texinput_normal_handler)
        self.dispatcher.add_handler(texinput_inline_handler)

    def echo_latex_normal(self, update, context):
        '''
        This is the callback function for the messagehandler.
        '''
        msg = update.message.text
        firstword = msg.split(' ', 1)[0]
        if firstword == '/tex' or firstword == '/tex@printexifyBot':
            msg = msg.split(' ', 1)[1]
        if imagify(msg):
            with open("tex/usercode.jpg", "rb") as f:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)

    def echo_latex_edited(self, update, context):
        '''
        This is the callback function for the messagehandler when a message is edited.
        '''
        msg = update.edited_message.text
        firstword = msg.split(' ', 1)[0]
        if firstword == '/tex' or firstword == '/tex@printexifyBot':
            msg = msg.split(' ', 1)[1]
        if imagify(msg):
            with open("tex/usercode.jpg", "rb") as f:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)

    def echo_latex_inline(self, update, context):
        '''
        This is the callback function for the handler for messages in inline mode.
        '''
        query = update.inline_query.query
        time.sleep(2)
        if imagify(query):
            privchannID = self.own_id
            infophoto = context.bot.sendPhoto(chat_id=privchannID, photo=open('tex/usercode.jpg', 'rb'), caption=query)
            thumbphoto = infophoto["photo"][0]["file_id"]
            originalphoto = infophoto["photo"][-1]["file_id"]
            results = [
                InlineQueryResultCachedPhoto(
                    id=uuid4(),
                    title="CachedPhoto",
                    photo_file_id=originalphoto
                )
            ]
            update.inline_query.answer(results)
