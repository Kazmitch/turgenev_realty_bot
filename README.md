# Бот для продажи квартир в новостройках

## Используемы технологии

---

- [Python](https://www.python.org/): Язык программирования, на котором написан бот.
- [aiogram](https://docs.aiogram.dev/en/latest/index.html#): фреймворк для создания ботов.
- [Django](https://www.djangoproject.com/): фреймворк, используемый в качестве [ORM](https://ru.wikipedia.org/wiki/ORM) и админки.
- [Docker](https://docs.docker.com/) и [Docker Compose](https://docs.docker.com/compose/): упаковка бота в контейнер.
- [PostgreSQL](https://www.postgresql.org/): СУБД для хранения данных.
- [InfluxDB](https://www.influxdata.com/): СУБД, оптимизированная для работы с данными, содержащими [отметки времени](https://www.influxdata.com/time-series-database/)
- [Grafana](https://grafana.com/): технология для визуализации данных


### Установка

---

### Переменные окружения

Создайте файл `.env` на основе файла `.env.dist`. Для запуска бота локально, константы, который заканчиваются на `_HOST`
заполните `localhost`, для запуска в контейнере, заполните названиями сервисов из файла `docker-compose.yml`

### Grafana

После запуска контейнеров, откройте в браузере страницу `http://127.0.0.1:3000`. В появившемся окне введите логин и
пароль по умолчанию `admin`. Добавьте базы данных, подключите **PostgreSQL** и **InfluxDB** в разделе *Add data source*
Далее создайте дашборд, сделайте импорт файла *grafana_dashboard.json* из корня проекта.