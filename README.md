# sqlalchemy_flask_dash__project
Для запуска желательно использовать venv из репозитория.
Вместо подключения к моему серверу psql перенастроить драйвер на работу с локальной субд Mysql(или любой удобный для вас способ).
В /database/TestingLayer.py есть возможность сразу заполнить базу тестовыми данными.
Далее можно запускать как любой отладочный проект в dash через app.py. Тестовый сервер flask в запустится автоматически. 
