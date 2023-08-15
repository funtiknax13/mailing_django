Для запуска необходимо создать файл `keys.py` в папке `config` где задать переменные `USERNAME` и `PASSWORD` для подключения к БД postgresql.
Для работы с crontab:
- "python manage.py crontab add"  - запуск задач
- "python manage.py crontab show" - просмотр запущенных задач 
- "python manage.py crontab remove" - остановка задач