from peewee import *

db = SqliteDatabase("database.db")


class Question(Model):
    question_text = TextField()
    incorrect_answers = TextField()
    correct_answer = TextField()

    class Meta:
        database = db


class UserScore(Model):
    user_id = IntegerField(unique=True)
    score = IntegerField(default=0)

    class Meta:
        database = db


db.connect()
db.create_tables([Question, UserScore])
