import logging
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройки логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Токен бота
TOKEN = '6128729724:AAFBUpqRFdLd8n0FNyk4svre4QEBULpgnIM'

# Создание объектов бота и апдейтера
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Добро пожаловать в бот записи на марафон! Чтобы продолжить, пожалуйста, введите свое ФИО.')
    context.user_data['fio'] = True

# Обработчик команды /help
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Для записи на марафон, пожалуйста, введите свое ФИО, а затем введите тип забега: полумарафон или марафон.')

# Обработчик ввода пользователем сообщения
def echo(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('fio'):
        fio = update.message.text
        context.user_data['fio'] = False
        context.user_data['run_type'] = True
        update.message.reply_text('Спасибо! Теперь введите тип забега: полумарафон или марафон.')
    elif context.user_data.get('run_type'):
        run_type = update.message.text
        context.user_data['run_type'] = False
        update.message.reply_text(f'Вы успешно записаны на {run_type} марафон! Спасибо за запись.')

# Обработчик ошибок
def error(update: Update, context: CallbackContext) -> None:
    logging.error(f'Update "{update}" caused error "{context.error}"')

# Добавляем обработчики команд и сообщений
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
updater.dispatcher.add_error_handler(error)

# Запускаем бота
updater.start_polling()

# Останавливаем бота перед выходом
updater.idle()
