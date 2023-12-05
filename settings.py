DEFAULT_ANSWEAR = 'Привет, это официальный бот от нашей команды! Нажми на кнопку "Инструкция", чтобы узнать про функционал бота!'
ANSWER_FOR_ADMIN = 'Привет, с помощью этого меню ты можешь добавлять и удалять работников!'
ANSWER_FOR_ADMIN_YARIC = 'Привет, с помощью этого меню ты можешь добавлять и удалять работников, а также принимать и отклонять запросы новых капитанов!'
TOP_ADMIN_ID = 1 #админ добавляющий капитанов
ADMIN_ID = [1] #список всех админов
INTENTS = [
    {
        "name": "Справка о функциях бота",
        "tokens": "Инструкция",
        "scenario": None,
        "answer": """Приветствую! Вы читаете инструкцию по взаимодействию с системой ReStaff!

                    В главном меню Вам предоставляется возможность нажать одну из трёх кнопок: "Инструкция", которую вы сейчас нажали, "Пройти тест", и "Попросить кадра".
                    
                    Если Вы желаете пройти наш тест и попасть в нашу базу данных проверенных кадров — нажимайте кнопку "Пройти тест", Вам выдаст инструкцию о том, как подать заявку на выполнение теста.
                    
                    Если Вы — капитан команды, ведущей свою деятельность на нашем сайте, ReManga.org, первым делом Вам потребуется подтвердить это, отправив ссылку на свою команду. Спустя некоторое время оператор проверит Вашу команду, и, убедившись, что Вы действительно являетесь капитаном, выдаст Вам доступ к возможности "Попросить кадра".
                    
                    Нажав на кнопку "Попросить кадра", капитану нужно будет ответить на череду вопросов, автоматически отправляющихся нашей системой. После того, как будут получены ответы на все вопросы, наша система сгенерирует единый запрос, который отправится всем проверенным нами кадрам в личные сообщение. Кадры, получившие запрос, будут иметь всю информацию, извлечённую из ответов капитана на ранее заданные вопросы. Кадр сможет либо отказаться от запроса, либо принять его.
                    
                    Если кадр принимает запрос, наша система в этот же момент высылает кадру ссылку на капитана, отправившего запрос, а капитану ссылку на кадра, принявшего данный запрос.""",
        "photo": None,
        "access": True
    },
    {
        "name": "Информация для теста",
        "tokens": "Пройти тест",
        "scenario": None,
        "answer": "Для прохождения теста вам нужно зайти на главный экран сообщества, найти в меню кнопку “ТЕСТ”, нажать её, заполнить анкету)",
        "photo": "photo-204183013_457239023",
        "access": True
    },
    {
        "name": "Попросить кадра",
        "tokens": "Попросить кадра",
        "scenario": "ask_for_worker",
        "answer": None,
        "photo": None,
        "access": True
    },
    {
        "name": "Добавить работника",
        "tokens": "Добавить работника",
        "scenario": "add_worker",
        "answer": None,
        "photo": None,
        "access": False
    },
    {
        "name": "Удалить работника",
        "tokens": "Удалить работника",
        "scenario": "delete_worker",
        "answer": None,
        "photo": None,
        "access": False
    }
]

SCENARIOS = {
    "registration": {
        "steps": {
            "step1": {
                "text": "Введите ссылку на вашу команду с реманги",
                "failure_text": "Ваша ссылка неправильна",
                "handler": "check_for_url",
                "next_step": "step2",
                "keyboard": "back"
            },
            "step2": {
                "text": "Пожалуйста, подождите, пока с вами свяжутся",
                "failure_text": None,
                "handler": "base_handler",
                "next_step": None,
                "keyboard": "default",
                "end_of_scenario": "registration"
            }
        }
    },
    "add_worker": {
        "steps": {
            "step1": {
                "text": "Введите роль работника",
                "failure_text": "Введите роль, нажав кнопку в меню бота",
                "handler": "check_for_worker",
                "next_step": "step2",
                "keyboard": "roles"
            },
            "step2": {
                "text": "Введите ссылку на рабочего",
                "failure_text": 'Вы ввели ссылку не правильно!',
                "handler": "check_userid",
                "next_step": "step3",
                "keyboard": "back",
            },
            "step3": {
                "text": "Введите оценку работника",
                "failure_text": None,
                "handler": "base_handler",
                "next_step": "step4",
                "keyboard": "back"
            },
            "step4": {
                "text": "Введите примечание для рабочего",
                "failure_text": None,
                "handler": "base_handler",
                "next_step": "step5",
                "keyboard": "back",
            },
            "step5": {
                "text": "Работник успешно добавлен в базу данных!",
                "failure_text": "",
                "handler": "base_handler",
                "next_step": None,
                "keyboard": "top_admin_panel",
                "end_of_scenario": "scenario_for_add_worker"
            },
        }
    },
    "delete_worker": {
        "steps": {
            "step1": {
                "text": "Введите ссылку на аккаунт работника, которого хотите удалить",
                "failure_text": 'Вы ввели ссылку не правильно или такого работника нет!',
                "handler": "exist_worker",
                "next_step": "step2",
                "keyboard": "back"
            },
            "step2": {
                "text": "Работник успешно удален!",
                "failure_text": None,
                "handler": "base_handler",
                "next_step": None,
                "keyboard": "top_admin_panel",
                "end_of_scenario": "delete_worker"
            }
        }
    },
    "ask_for_worker": {
        "steps": {
            "step1": {
                "text": "Какой кадр нужен?",
                "failure_text": "К сожалению данной роли у нас нет. Пожалуйста, выберите роль из предложенных:",
                "handler": "check_for_worker",
                "keyboard": "roles",
                "next_step": "step2"
            },
            "step2": {
                "text": "Ссылка на проект",
                "failure_text": "Вы ввели некорректную ссылку",
                "handler": "check_for_url",
                "keyboard": "back",
                "next_step": "step3"
            },
            "step3": {
                "text": "Предлагаемая ставка",
                "failure_text": "",
                "handler": "base_handler",
                "keyboard": "back",
                "next_step": "step4"
            },
            "step4": {
                "text": "Временные условия",
                "failure_text": "",
                "handler": "base_handler",
                "keyboard": "back",
                "next_step": "step5"
            },
            "step5": {
                "text": "Примечание ",
                "failure_text": "",
                "handler": "base_handler",
                "keyboard": "back",
                "next_step": "step6"
            },
            "step6": {
                "text": "Спасибо, мы уже занимаемся поиском подходящих работников",
                "failure_text": "",
                "handler": "base_handler",
                "keyboard": "default",
                "next_step": None,
                "end_of_scenario": "ask_for_worker"
            },
        }
    }
}
