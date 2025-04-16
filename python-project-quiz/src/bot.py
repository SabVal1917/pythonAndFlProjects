import telebot
import requests
import random
import re
from peewee import *
from telebot.types import ReplyKeyboardMarkup

from .models import Question, UserScore
from .config import API_TOKEN, TRIVIA_API_URL, START_MESSAGE

bot = telebot.TeleBot(API_TOKEN)
QUESTIONS_AMOUNT = 0
user_data_setter = {}
current_user_questions = {}


def get_correct_trivia_format(question_text):
    pattern = r'&.*?;'
    cleaned_text = re.sub(pattern, '', question_text)
    return cleaned_text


@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_id = message.from_user.id
    user, created = UserScore.get_or_create(user_id=user_id)
    bot.send_message(message.chat.id,
                     f"Добро пожаловать в викторину, {message.from_user.first_name}!\n" + START_MESSAGE)
    global QUESTIONS_AMOUNT
    QUESTIONS_AMOUNT = 0
    Question.delete().execute()
    user.score = 0
    user.save()


# Команда для установки количества вопросов
@bot.message_handler(commands=['set_amount_q'])
def set_amount_questions(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите количество вопросов:")
    user_data_setter[chat_id] = {'state': 'WAITING_FOR_NUMBER'}
    # UserScore.delete().execute()


@bot.message_handler(
    func=lambda message: (len(user_data_setter) != 0))
def set_amount_questions(message):
    chat_id = message.chat.id
    if chat_id in user_data_setter and user_data_setter[chat_id].get('state') == 'WAITING_FOR_NUMBER':
        try:
            # Пробуем преобразовать ввод в число
            amount = int(message.text)

            global QUESTIONS_AMOUNT
            QUESTIONS_AMOUNT = amount

            user_data_setter[chat_id] = {'state': None, 'amount': amount}

            load_questions()
            bot.send_message(chat_id, f"Количество вопросов установлено: {amount}")
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите корректное число.")
    else:
        bot.send_message(chat_id,
                         "Неизвестная команда. Попробуйте /set_amount_questions для установки количества вопросов.")
    user_data_setter.clear()


# function for loading some questions to our database
def load_questions():
    global QUESTIONS_AMOUNT
    if Question.select().count() >= QUESTIONS_AMOUNT:
        return
    QUESTIONS_AMOUNT -= Question.select().count()
    TRIVIA_API_URL = "https://opentdb.com/api.php?amount=" + str(QUESTIONS_AMOUNT)
    response = requests.get(TRIVIA_API_URL)
    if response.status_code == 200:
        data = response.json()['results']
        for item in data:
            Question.create(
                question_text=get_correct_trivia_format(item['question']),
                correct_answer=item['correct_answer'],
                incorrect_answers='|'.join(item['incorrect_answers'])
            )


@bot.message_handler(commands=['quiz'])
def send_question(message):
    user_id = message.from_user.id
    question = Question.select().order_by(fn.Random()).get()
    incorrect_answers = question.incorrect_answers
    answer_list = incorrect_answers.split('|')
    answer_list.append(question.correct_answer)
    random.shuffle(answer_list)
    current_user_questions[user_id] = question.id
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for answer in answer_list:
        markup.add(answer)
    bot.send_message(message.chat.id, question.question_text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: (message.from_user.id in current_user_questions))
def check_answer(message):
    user_id = message.from_user.id
    question_id = current_user_questions.pop(user_id)
    selected_answer = message.text
    question = Question.get(Question.id == question_id)

    if selected_answer == question.correct_answer:
        user = UserScore.get(UserScore.user_id == user_id)
        user.score += 1
        user.save()
        bot.send_message(message.chat.id, f"Правильно! Ваш счет: {user.score}")
    else:
        bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {question.correct_answer}")
    bot.send_message(message.chat.id, "Напишите /quiz, чтобы продолжить.")

    global QUESTIONS_AMOUNT
    QUESTIONS_AMOUNT -= 1
    # question.delete_instance()


@bot.message_handler(commands=['score'])
def show_score(message):
    user_id = message.from_user.id
    user, created = UserScore.get_or_create(user_id=user_id)
    bot.send_message(message.chat.id, "Ваш текущий счет: {}".format(user.score))


@bot.message_handler(commands=['clear'])
def clear_chat(message):
    chat_id = message.chat.id
    message_id = message.message_id

    try:
        i = 0
        while (True):
            bot.delete_message(chat_id, message_id - i)
            i += 1
    except:
        pass


bot.infinity_polling(timeout=10, long_polling_timeout=5)
