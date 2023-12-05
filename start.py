import bot
from DataBase import DataBase
from secret import TOKEN, GROUP_ID
from settings import TOP_ADMIN_ID


def start():
    while True:
        try:
            bot.BOT(token=TOKEN, group_id=GROUP_ID, db=DataBase('basa.db'), top_admin_id=TOP_ADMIN_ID).run()
        except Exception as e:
            print('Error! Переподключение...', e)


if __name__ == "__main__":
    start()
