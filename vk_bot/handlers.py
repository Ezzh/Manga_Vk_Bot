#!python3


def check_for_worker(text, **kwargs):
    jobs = ['Эдитор', 'Клинер', 'Клинер звуков', 'Тайпер', 'Редактор', 'Переводчик с английского',
            'Переводчик с корейского', 'Переводчик с японского', 'Переводчик с китайского', 'Переводчик с индонезийского']
    return text in jobs


def check_for_url(text, **kwargs):
    return text.startswith("https://remanga.org/manga/") or text.startswith("https://remanga.org/team/")


def check_userid(text, **kwargs):
    return text.startswith('https://vk.com/') and kwargs['vk_session'].method('users.get', {'user_ids': text[15:]})


def exist_worker(text, **kwargs):
    vk_id = kwargs['vk_session'].method('users.get', {'user_ids': text[15:]})
    return text.startswith('https://vk.com/') and vk_id and kwargs['db'].existence_worker(vk_id[0]['id'])


def base_handler(text, **kwargs):
    return True
