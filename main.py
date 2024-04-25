import telebot
from telebot import types

# Токен вашего бота
API_TOKEN = "6632293001:AAF5nnjoRCt6oKI_fcN81NBvhKSOOMZ28EI"

# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения данных пользователей
user_data = {}

# Функция для старта бота
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("Марафон"), types.KeyboardButton("Полумарафон"))
    bot.send_message(message.chat.id, "Выберите дистанцию:", reply_markup=keyboard)
    user_data[message.from_user.id] = {"step": "choosing_distance"}

# Функция для выбора дистанции
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("step") == "choosing_distance")
def choosing_distance(message):
    user_data[message.from_user.id]["choice"] = message.text
    bot.send_message(message.chat.id, "Введите ваше имя:")
    user_data[message.from_user.id]["step"] = "typing_name"

# Функции для ввода имени, фамилии, отчества и даты рождения
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("step") == "typing_name")
def typing_name(message):
    user_data[message.from_user.id]["name"] = message.text
    bot.send_message(message.chat.id, "Введите вашу фамилию:")
    user_data[message.from_user.id]["step"] = "typing_surname"

# Функция для ввода отчества
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("step") == "typing_surname")
def typing_surname(message):
    user_data[message.from_user.id]["surname"] = message.text
    bot.send_message(message.chat.id, "Введите ваше отчество:")
    user_data[message.from_user.id]["step"] = "typing_patronymic"

# Функция для ввода даты рождения (ранее была без обработчика)
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("step") == "typing_patronymic")
def typing_patronymic(message):
    user_data[message.from_user.id]["patronymic"] = message.text
    bot.send_message(message.chat.id, "Введите вашу дату рождения (ДД.ММ.ГГГГ):")
    user_data[message.from_user.id]["step"] = "typing_birthdate"


# Функция для сохранения данных в файл
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("step") == "typing_birthdate")
def typing_birthdate(message):
    user_data[message.from_user.id]["birthdate"] = message.text
    data = user_data[message.from_user.id]
    with open("registrations.txt", "a") as f:
        f.write(f"{data['choice']}, {data['name']} {data['surname']} {data['patronymic']}, {data['birthdate']}\n")
    bot.send_message(message.chat.id, "Спасибо за регистрацию!")
    del user_data[message.from_user.id]

# Запуск бота
bot.polling()
