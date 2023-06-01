import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Установите ваш API-токен OpenAI
openai.api_key = 'опенаи токен'

# Установите токен вашего Telegram-бота
TELEGRAM_TOKEN = 'телеграм токен'

# Инициализация логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Функция, которая будет вызываться при команде /start
def start(update: Update, context) -> None:
    """Отправляет приветственное сообщение при команде /start"""
    update.message.reply_text('Привет! Я бот, который может ответить на твои вопросы. Просто задай вопрос!')

# Функция, которая будет вызываться для каждого входящего сообщения
def echo(update: Update, context) -> None:
    """Отправляет сообщение в ChatGPT и пересылает ответ обратно в Telegram"""
    question = update.message.text
    response = chat_gpt_response(question)
    update.message.reply_text(response)

# Функция, которая отправляет вопрос в ChatGPT и возвращает ответ
def chat_gpt_response(question: str) -> str:
    """Отправляет вопрос в ChatGPT и возвращает ответ"""
    model_name = 'gpt-3.5-turbo'  # Имя модели GPT-3.5-turbo
    response = openai.Completion.create(
        engine=model_name,
        prompt=question,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

def main() -> None:
    """Главная функция для запуска бота"""
    # Создание экземпляра Updater и передача токена Telegram
    updater = Updater(TELEGRAM_TOKEN)
    
    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Зарегистрировать обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Зарегистрировать обработчик входящих сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()

    # Остановка бота при нажатии Ctrl + C
    updater.idle()

if __name__ == '__main__':
    main()
