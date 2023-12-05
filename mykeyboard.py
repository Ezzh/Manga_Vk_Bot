from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def createkeyboard(type='default'):
    keyboard = VkKeyboard(one_time=True)
    if type == 'default':
        keyboard.add_button('Инструкция', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Пройти тест', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Попросить кадра', color=VkKeyboardColor.POSITIVE)
    elif type == 'back':
        keyboard.add_button('Назад')
    elif type == 'checking_requests':
        keyboard.add_button('Принять запрос', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Отклонить запрос', color=VkKeyboardColor.SECONDARY)
    elif type == 'roles':
        keyboard.add_button('Эдитор', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Клинер', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Клинер звуков', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Тайпер', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Редактор', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Переводчик с английского', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Переводчик с корейского', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Переводчик с японского', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Переводчик с китайского', color=VkKeyboardColor.POSITIVE)
        # индозийского
        keyboard.add_button('Переводчик с индонезийского', color=VkKeyboardColor.POSITIVE)
    elif type == 'top_admin_panel':
        keyboard.add_button('Начать проверку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Добавить работника', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Удалить работника', color=VkKeyboardColor.POSITIVE)
    elif type == 'admin_panel':
        keyboard.add_button('Добавить работника', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Удалить работника', color=VkKeyboardColor.POSITIVE)
    elif type == 'view_requests_for_worker':
        keyboard.add_button('Посмотреть запросы', color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()
