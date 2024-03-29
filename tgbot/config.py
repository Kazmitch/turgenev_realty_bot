from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class InfluxDbConfig:
    url: str
    org: str
    bucket: str
    username: str = None
    password: str = None
    token: str = None


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool
    bot_name: str


@dataclass
class Miscellaneous:
    clickhouse_post: str
    clickhouse_port: str
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_db: str
    bot_sender_token: str
    chat_info: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    influxdb: InfluxDbConfig
    redis_host: str = None


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            bot_name=env.str("BOT_NAME")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('POSTGRES_DB')
        ),
        misc=Miscellaneous(
            clickhouse_post=env.str('CLICKHOUSE_HOST'),
            clickhouse_port=env.str('CLICKHOUSE_PORT'),
            clickhouse_user=env.str('CLICKHOUSE_USER'),
            clickhouse_password=env.str('CLICKHOUSE_PASSWORD'),
            clickhouse_db=env.str('CLICKHOUSE_DB'),
            bot_sender_token=env.str('BOT_SENDER_TOKEN'),
            chat_info=env.str('CHAT_INFO')
        ),
        redis_host=env.str('REDIS_HOST'),
        influxdb=InfluxDbConfig(
            url=env.str('INFLUXDB_HOST'),
            org=env.str('INFLUXDB_ORG'),
            bucket=env.str('INFLUXDB_BUCKET'),
            username=env.str('INFLUXDB_USERNAME'),
            password=env.str('INFLUXDB_PASSWORD'),
            token=env.str('INFLUXDB_TOKEN')
        )
    )
