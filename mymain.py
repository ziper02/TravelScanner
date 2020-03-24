import time
from Flights import EasyJet as ss
from TelegramBot import bot
from threading import Thread
import sys
from ServerTools import ShellCommands as sc
import platform


def update_locations_new_notfication_file_thread():
    while True:
        try:
            ss.update_locations_new_notfication_file()
            time.sleep(10800)
        except Exception as e:
            bot.bot_send_message(e)
            sys.exit()

def mem_info_thread():
    while True:
        try:
            bot.bot_send_message("Memory available :\n"+sc.mem_info(),bot.log_group)
            time.sleep(3600)
        except Exception as e:
            bot.bot_send_message(e)
            sys.exit()



if __name__ == "__main__":
    thread_1 = Thread(target=update_locations_new_notfication_file_thread, args=()).start()
    if platform.system() == 'Linux':
        thread_2 = Thread(target=mem_info_thread, args=()).start()
    bot.start_bot()
