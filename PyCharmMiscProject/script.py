import telebot
from bs4 import BeautifulSoup
import requests

BOT_TOKEN = '7574322137:AAFhXhZAXK1Er5puFIwuhg2yQJr-RFVuIZE'
WEATHER_API_KEY = '01769eee781485df3d12bc9d793950b5'

bot = telebot.TeleBot(BOT_TOKEN)

URL = "https://yandex.ru/pogoda/kemerovo?lat=55.3552&lon=86.086848"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_sun_times():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        sun_card = soup.find("div", class_="sun-card__day-duration-value")
        print(sun_card)
        if not sun_card:
            return "Не удалось найти данные о восходе и заходе солнца."

        return f"Длина светового дня в Кемерово: {sun_card.text}"
    except Exception as e:
        return f"Ошибка при получении данных: {e}"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот для получения информации о погоде и длине светового дня в Кемерово. Напиши команду /weather [город], чтобы узнать погоду! Напиши /sun, чтобы узнать длину светового дня в Кемерово.")


@bot.message_handler(commands=["sun"])
def send_sun_info(message):
    sun_info = get_sun_times()
    bot.reply_to(message, sun_info)


@bot.message_handler(commands=['weather'])
def send_weather(message):
    try:
        city = message.text.split(maxsplit=1)[1]
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажи город. Пример: /weather Москва")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']

        reply = (f"Погода в {city_name}:\n"
                 f"- Описание: {weather_desc.capitalize()}\n"
                 f"- Температура: {temp}°C\n"
                 f"- Ощущается как: {feels_like}°C")
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, "Не удалось найти информацию о погоде. Проверь название города.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я понимаю только команды. Попробуй /start или /weather [город] или /sun.")


if __name__ == "__main__":
    bot.polling(none_stop=True)