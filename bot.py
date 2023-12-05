import settings
from secret import TOKEN
import handlers
import vk_api
from Top_admin import Top_admin
from Worker import Worker
from MyVkBotLongPoll import MyVkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from mykeyboard import createkeyboard
from vk_api.utils import get_random_id
import time


class UserState:
    """Состояние пользователя внутр и сценария"""

    def __init__(self, scenario_name, step_name):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.info = []


class BOT:
    def __init__(self, token, group_id, db, top_admin_id):
        self.vk_session = vk_api.VkApi(token=TOKEN)
        self.longpoll = MyVkBotLongPoll(self.vk_session, group_id)
        self.api = self.vk_session.get_api()
        self.group_id = group_id
        self.token = token
        self.db = db
        self.vk = vk_api.VkApi(token=token)
        self.user_states = dict()
        self.worker_states = dict()
        self.admins = settings.ADMIN_ID
        self.top_admin = Top_admin(top_admin_id, False, db)
        self.update_workers()

    def update_workers(self):
        self.worker_states.clear()
        for i in self.db.get_workers():
            print(i)
            self.worker_states[i[0]] = Worker(i[1], i[2], self.db, self.api)

    def new_message(self, event):
        """Отправка сообщения назад, если сообщение текстовое"""
        user_id = event.object.message['peer_id']
        if event.object.message['attachments'] and event.object.message['attachments'][0]['type'] == 'link':
            text = event.object.message['attachments'][0]['link']['url']
        else:
            text = event.object.message['text']
        text_to_send = settings.DEFAULT_ANSWEAR
        keyboard = createkeyboard()
        print(text, user_id)
        photo_to_send = None

        if user_id in self.user_states:
            text_to_send, keyboard = self.continue_scenario(user_id, text)
        elif user_id in self.admins:
            text_to_send, keyboard = self.admin_panel(text, user_id)

        elif user_id in self.worker_states and text == 'Посмотреть запросы':
            self.worker_states[user_id].status = True
            text_to_send, keyboard = self.start_check_request(user_id)
        elif user_id in self.worker_states:
            if self.worker_states[user_id].status:
                text_to_send, keyboard = self.check_request(user_id, text)
            else:
                text_to_send, keyboard = "Нажмите на кнопку 'Посмотреть запросы', чтобы увидеть доступные заказы", createkeyboard(
                    'view_requests_for_worker')
        else:
            for intent in settings.INTENTS:
                if text == intent["tokens"] and intent["access"] == True:
                    if intent["answer"]:
                        text_to_send = intent["answer"]
                        photo_to_send = intent["photo"]
                    else:
                        text_to_send = self.start_scenario(user_id=user_id, scenario_name=intent["scenario"])
                        keyboard = createkeyboard(
                            settings.SCENARIOS[self.user_states[user_id].scenario_name]["steps"][
                                self.user_states[user_id].step_name]["keyboard"])
                    break
            # search intent
        self.api.messages.send(message=text_to_send,
                               random_id=get_random_id(),
                               peer_id=user_id,
                               keyboard=keyboard,
                               attachment=photo_to_send)

    def run(self):
        events = {VkBotEventType.MESSAGE_NEW: self.new_message}
        for event in self.longpoll.listen():
            if event.type in events:
                # не знаю почему ругается
                events[event.type](event)

    def start_scenario(self, user_id, scenario_name):
        if not self.db.existence_captain(user_id) and scenario_name == "ask_for_worker":
            scenario_name = "registration"
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name="step1")
        return settings.SCENARIOS[scenario_name]["steps"]["step1"]["text"]

    def continue_scenario(self, user_id, text):
        if text == "Назад":
            self.user_states.pop(user_id)
            if user_id == self.top_admin.id:
                keyboard = createkeyboard('top_admin_panel')
            elif user_id in settings.ADMIN_ID:
                keyboard = createkeyboard('admin_panel')
            else:
                keyboard = createkeyboard('default')
            return "Возвращаю назад...", keyboard

        state = self.user_states[user_id]
        step = settings.SCENARIOS[state.scenario_name]['steps'][state.step_name]
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        next_step = steps[step['next_step']]
        handler = getattr(handlers, step['handler'])
        if handler(text, vk_session=self.vk_session, db=self.db):
            state.info.append(text)
            text_to_send = next_step['text']
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
                keyboard = createkeyboard(next_step['keyboard'])
            else:
                info = state.info
                print(info)
                # finish scenario
                self.end_of_scenario(state, user_id)
                if user_id == self.top_admin.id:
                    keyboard = createkeyboard('top_admin_panel')
                elif user_id in settings.ADMIN_ID:
                    keyboard = createkeyboard('admin_panel')
                else:
                    keyboard = createkeyboard('default')
        else:
            text_to_send = step['failure_text']
            keyboard = createkeyboard(step['keyboard'])
            return text_to_send, keyboard
        return text_to_send, keyboard

    def end_of_scenario(self, state, user_id=None):
        function_list = {'ask_for_worker': self.end_ask_for_worker, 'registration': self.end_register,
                         'delete_worker': self.end_delete_worker, 'add_worker': self.end_add_worker}
        function_list[state.scenario_name](state, user_id)

    def check_captain(self, text):
        if text == "Принять запрос":
            self.top_admin.accept()
            self.api.messages.send(message="Теперь ты капитан!",
                                   random_id=get_random_id(),
                                   peer_id=self.top_admin.proverka[0],
                                   keyboard=createkeyboard())
        elif text == "Отклонить запрос":
            self.top_admin.deny()
        else:
            return 'Я вас не понял!'
        return self.start_captain()

    def start_captain(self):
        noCaptain = self.db.get_captains_to_the_check()
        if noCaptain:
            self.top_admin.proverka = noCaptain[0]
            return f'ID пользователя https://vk.com/id{noCaptain[0][0]}\n Ссылка на команду: {noCaptain[0][1]}', createkeyboard(
                'checking_requests')
        else:
            self.top_admin.status = False
            return 'Нет капитанов на проверку!', createkeyboard("top_admin_panel")

    def start_check_request(self, worker):
        worker = self.worker_states[worker]
        requests = self.db.get_requests(worker.role)

        if not requests:
            worker.status = False
            return 'Запросов, пока что, нет!', createkeyboard('view_requests_for_worker')

        if worker.being_checked and worker.being_checked != 'stop':
            if worker.next and worker.next != 'stop':
                worker.being_checked = worker.next
            worker.is_last(requests)
        elif worker.being_checked == 'stop':
            worker.clear()
            return 'Запросы закончились!', createkeyboard('view_requests_for_worker')
        else:
            worker.being_checked = requests[0]
            worker.is_last(requests)
        if worker.being_checked:
            message = f'Нужен {worker.being_checked[2]}! \n' \
                      f'Моя команда - {worker.being_checked[1]}\n' \
                      f'Ставка -  {worker.being_checked[3]}\n' \
                      f'Временные условия -  {worker.being_checked[4]}\n' \
                      f'Примечание - {worker.being_checked[5]}'

            return message, createkeyboard('checking_requests')

    def check_request(self, worker, text):
        if text == 'Принять запрос':
            return self.worker_states[worker].accept(worker)
        elif text == 'Отклонить запрос':
            if self.worker_states[worker].next == 'stop':
                self.worker_states[worker].being_checked = 'stop'
            return self.start_check_request(worker)
        self.worker_states[worker].clear()
        return 'Я вас не понял! Начните проверять заново!', createkeyboard('view_requests_for_worker')

    def end_register(self, state, user_id):
        info = state.info
        if state.scenario_name == "registration":
            self.db.adding_captain_to_the_check(user_id, info[0])
            self.api.messages.send(message='Новый капитан на проверку!',
                                   random_id=get_random_id(),
                                   user_id=str(self.top_admin.id),
                                   keyboard=createkeyboard(type='top_admin_panel'))
        self.user_states.pop(user_id)

    def end_ask_for_worker(self, state, user_id):
        self.update_workers()
        info = state.info
        list_of_answears = info
        print(list_of_answears)
        self.db.add_request(user_id, list_of_answears[1], list_of_answears[0], list_of_answears[2], list_of_answears[3],
                            list_of_answears[4])
        message = 'Новый запрос! Успей забрать!'
        send_to_who = self.db.send_notification_to_worker(list_of_answears[0])
        for url in send_to_who:
            self.api.messages.send(message=message,
                                   random_id=get_random_id(),
                                   user_id=url[0],
                                   keyboard=createkeyboard(type='view_requests_for_worker'))
        self.user_states.pop(user_id)

    def end_delete_worker(self, state, user_id):
        list_of_answears = state.info
        vk_id = self.api.utils.resolveScreenName(screen_name=list_of_answears[0].split('/')[-1])['object_id']
        if self.db.existence_worker(vk_id):
            self.db.delete_worker(vk_id)
            message = 'К сожалению, было принято решение исключить вас из работников!'
            self.api.messages.send(message=message,
                                   random_id=get_random_id(),
                                   user_id=vk_id,
                                   keyboard=createkeyboard(type='default'))
            self.user_states.pop(user_id)
            self.update_workers()
        else:
            message = 'Такого работника нет в базе!'
            self.api.messages.send(message=message,
                                   random_id=get_random_id(),
                                   user_id=user_id,
                                   keyboard=createkeyboard(type='top_admin_panel'))
            self.user_states.pop(user_id)

    def end_add_worker(self, state, user_id):
        list_of_answears = state.info
        vk_worker = \
            self.vk_session.method('utils.resolveScreenName', {'screen_name': list_of_answears[1].split('/')[-1]})[
                'object_id']
        self.db.add_worker(list_of_answears[0], vk_worker, list_of_answears[2], list_of_answears[3])
        self.update_workers()
        message = 'Теперь вы числитесь в официальных работниках!'
        self.api.messages.send(message=message,
                               random_id=get_random_id(),
                               user_id=vk_worker,
                               keyboard=createkeyboard(type='view_requests_for_worker'))
        self.user_states.pop(user_id)

    def admin_panel(self, text, user_id):
        if user_id == settings.TOP_ADMIN_ID:
            text_to_send = settings.ANSWER_FOR_ADMIN_YARIC
            keyboard = createkeyboard('top_admin_panel')
        else:
            text_to_send = settings.ANSWER_FOR_ADMIN
            keyboard = createkeyboard('admin_panel')
        if text == 'Начать проверку' and user_id == settings.TOP_ADMIN_ID:
            self.top_admin.status = True
            text_to_send, keyboard = self.start_captain()
        elif self.top_admin.status:
            text_to_send, keyboard = self.check_captain(text)
        else:
            for intent in settings.INTENTS:
                if text == intent["tokens"]:
                    if intent["answer"]:
                        text_to_send = intent["answer"]
                    else:
                        text_to_send = self.start_scenario(user_id=user_id, scenario_name=intent["scenario"])
                        keyboard = createkeyboard(
                            settings.SCENARIOS[self.user_states[user_id].scenario_name]["steps"][
                                self.user_states[user_id].step_name]["keyboard"])
        return text_to_send, keyboard

# vk_session = vk_api.VkApi(token=TOKEN)
# print(vk_session.method('utils.resolveScreenName', {'screen_name': 'ezzh32'})['object_id'])
