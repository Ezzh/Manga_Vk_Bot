from vk_api.utils import get_random_id

from mykeyboard import createkeyboard


# .ini
class Worker:
    def __init__(self, role, id, db, api):
        self.role = role
        self.id = id
        self.db = db
        self.api = api
        self.status = False
        self.being_checked = None
        self.next = None

    def accept(self, worker):
        pr = self.being_checked
        self.clear()
        if self.db.existence_request(pr[6]):
            self.db.delete_request(pr[6])
            self.db.update_date(self.id)
            self.api.messages.send(
                message=f"Твой запрос приняли! Вот контакты работника! https://vk.com/id{worker}",
                random_id=get_random_id(),
                peer_id=pr[0],
                keyboard=createkeyboard())
            return f'Вот мои контакты: https://vk.com/id{pr[0]} !', createkeyboard('view_requests_for_worker')
        else:
            return f'Запрос уже забрали!', createkeyboard('view_requests_for_worker')

    def clear(self):
        self.status = False
        self.being_checked = None
        self.next = None

    def is_last(self, zaprosi):
        if zaprosi.index(self.being_checked) < len(zaprosi) - 1:
            self.next = zaprosi[zaprosi.index(self.being_checked) + 1]
        else:
            self.next = 'stop'
