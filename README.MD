Для запуска необходимо создать файл `.env` в папке проекта и задать следующие переменные:
- SECRET_KEY=
- DEBUG=

Данные для доступа к БД:
- DB_NAME=
- DB_USERNAME=
- DB_PASSWORD=

Данные почтового сервера:
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=

Данные кэширования:
- CACHE_ENABLED=
- CACHES_LOCATION=



Для работы с периодической отправкой сообщений:
- "python manage.py crontab add"  - запуск задач
- "python manage.py crontab show" - просмотр запущенных задач 
- "python manage.py crontab remove" - остановка задач



Применение миграций:
- python manage.py makemigration
- python manage.py migrate

Для тестирования есть готовые данные в файле db.json, загрузить командой:
- python manage.py loaddata db.json

Пользователи:
user@test.ru	rU4?*~bRtPbq+vv
admin@test.ru	1234 (superuser)

