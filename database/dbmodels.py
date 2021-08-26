from playhouse.postgres_ext import *
from decouple import config
from datetime import datetime
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')

db = PostgresqlDatabase('aviasales',
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)


class User(Model):
    name= CharField()
    phone = CharField()
    uid = BigIntegerField()
    username = CharField()
    date=DateTimeField(default=datetime.now)
    application = JSONField(null=True,
                        default={})

    class Meta:
        database = db


if not User.table_exists():
    db.create_tables([User])



