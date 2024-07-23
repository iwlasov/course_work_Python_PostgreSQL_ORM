Курсовая работа «ТГ-чат-бот «Обучалка английскому языку»» по курсу «Базы данных» EnglishCard

Цель проекта - разработать базу данных Telegram-бота для изучения английского языка.

Сделано:

    спроектирована и реализована база данных (БД) для программы:
    - Users - пользователи бота
    - User_Word - база слов добавляемая пользователем
    - Words - общая база слов для пользователей
    разработана программа-бот на Python:
     - main.py - основной исполняемый модуль
     - models.py - модуль баз данных
    написана документация по использованию программы - README.md.

В результате выполнения этого задания:

    научились работать с чужим кодом;
    получили практический опыт работы с PostgreSQL и Telegram;
    закрепили навыки работы с GitHub и программированием на языке Python;
    разработали программный продукт.

Чек-лист готовности к работе над проектом

    У вас должен быть установлен Python 3 и любая IDE. Рекомендуем работать с Pycharm.
    Настроен компьютер для работы с БД PostgreSQL.
    Установлен Git и создан аккаунт на GitHub.
    Cоздан бот в Telegram:
    
Инструменты/ дополнительные материалы, которые пригодятся для выполнения задания

    Python + IDE(Pycharm).
    Git + GitHub.
    Postgre + PgAdmin.
    Статья по разработке бота в Telegram.
    Инструкция по созданию бота в Telegram.
    pyTelegramBotAPI.
    Основа бота - код из модуля main.py.
    Исходный код в модуле main.py работает. Чтобы запустить бота нужно ввести команду /start в переписке с ним.
    Предварительно необходимо заполнить файл info.json указав:
     - login - логин от БД
     - password - пароль от БД
     - name_bd - имя БД
     - token_bot - токен от телеграм бота

Разработана программа-бота, которая должна выполняет следующие действия.

    Заполнет базу данных общим набором слов для всех пользователей (10 слов). Данные читаются из файла tests_data.json 
    Спрашивает перевод слова, предлагая 4 варианта ответа на английском языке в виде кнопок.
    При правильном ответе подтверждает ответ, при неправильном - предлагает попробовать снова.
    Реализована функция добавления нового слова.
    Реализована функция удаления добавленных слов. Удаление реальзовано персонально для пользователя.
    Новые слова не должны появляться у других пользователей.
    Работа с ботом после запуска начинается с приветственного сообщения.

Правила сдачи работы

    Спроектирована база данных для бота. Есть скрипты для её создания и заполнения.
    Разработан бот и все части кода объединены в главной ветке (master/main).
    Написана документация по использованию программы.
    В личном кабинете отправлена ссылка на репозиторий с решением.

Критерии оценки

Программный продукт соответствует следующим критериям.

    Отсутствуют ошибки (traceback) во время выполнения программы.
    Результат программы записывается в БД. Количество таблиц должно быть не меньше трёх. Приложена схема БД - scheme.PNG.
    Программа добавляет новые слова в БД для каждого пользователя.
    Код программы удовлетворяет PEP8. 

