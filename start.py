import vk_bot.bot as bot
from database.DataBase import DataBase
from secret import TOKEN, GROUP_ID
from vk_bot.settings import TOP_ADMIN_ID
import api.api as api


def start():
    while True:
        try:
            bot.BOT(token=TOKEN, group_id=GROUP_ID, db=db, top_admin_id=TOP_ADMIN_ID).run()
        except Exception as e:
            print('Error! Переподключение...', e)


if __name__ == "__main__":
    db = DataBase()
    api.app.run(host="0.0.0.0", debug=True, port=5001)
    start()
