import datetime
import sqlite3


class DataBase:
    def __init__(self, db):
        self.con = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.con.cursor()

    def add_worker(self, role, vk, mark='', note=''):
        self.cur.execute(
            f"""INSERT INTO Workers (Role, vk_id, Mark, Note) values (?, ?, ?, ?)""", (role, vk, mark, note))
        self.con.commit()

    def existence_worker(self, vk_id):
        worker = self.cur.execute("""SELECT id FROM Workers WHERE vk_id = ?""", (vk_id,)).fetchall()
        return bool(worker)

    def __str__(self):
        table = self.cur.execute(f"""SELECT * FROM Workers""").fetchall()
        ln = 'ID, Роль, VK, Оценка, Примечание, Дата\n'
        for i in table:
            ln += str(i)[1:-1]
            ln += '\n'
        return ln

    def send_notification_to_worker(self, worker_type):
        list_of_UI = self.cur.execute(f"""SELECT vk_id FROM Workers WHERE Role = ?""", (worker_type,)).fetchall()
        return list_of_UI

    def existence_captain(self, user_id):
        # Тут возвращать рез будем, проверка на наличие в таблице капитанов
        res = self.cur.execute(f"""SELECT EXISTS(SELECT vk_id FROM captains WHERE vk_id = ?)""", (user_id,)).fetchone()[0]
        return bool(res)

    def adding_captain_to_the_check(self, user_id, link):
        self.cur.execute(f"""INSERT INTO queue_captains (vk_id, link) values (?, ?)""", (user_id, link))
        self.con.commit()

    def removal_captain_to_the_check(self, user_id):
        self.cur.execute(f"""DELETE FROM queue_captains WHERE vk_id = ?""", (user_id,))
        self.con.commit()

    def adding_captain(self, user_id, link):
        self.cur.execute(f"""INSERT INTO captains (vk_id, project) values (?, ?)""", (user_id, link))
        self.con.commit()

    def get_captains_to_the_check(self):
        res = self.cur.execute(f"""SELECT vk_id,link FROM queue_captains""").fetchall()
        return res

    def add_request(self, captain, project, worker, bet, condition, other):
        self.cur.execute(
            f"""INSERT INTO requests (captain, project, worker, bet, condition, other) values (?, ?, ?, ?, ?, ?)""",
            (captain, project, worker, bet, condition, other))
        self.con.commit()

    def get_requests(self, worker):
        res = self.cur.execute(
            f"""SELECT captain, project, worker, bet, condition, other, id FROM requests WHERE worker = ?""",
            (worker,)).fetchall()
        return res
    
    def get_all_requests(self):
        res = self.cur.execute(
            f"""SELECT captain, project, worker, bet, condition, other, id FROM requests""").fetchall()
        return res

    def delete_request(self, id):
        self.cur.execute(f"""DELETE FROM requests WHERE id = ?""", (id,))
        self.con.commit()

    def get_workers(self):
        res = self.cur.execute(
            f"""SELECT vk_id, Role, id FROM Workers""").fetchall()
        return res

    def existence_request(self, id):
        res = self.cur.execute(
            f"""SELECT captain, project, worker, bet, condition, other FROM requests WHERE id = ?""", (id,)).fetchall()
        return bool(res)

    def update_date(self, id):
        self.cur.execute(
            f"""UPDATE Workers SET Date = '{datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')}' WHERE id = ?""",
            (str(id),))
        self.con.commit()

    def delete_worker(self, user_id):
        self.cur.execute(f"""DELETE FROM Workers WHERE vk_id = ?""", (user_id,))
        self.con.commit()

# db = DataBase('basa.db')
# for i in range(20):
#    db.add_zapros(192085888, i, 'Эдитор', i, i, i)
