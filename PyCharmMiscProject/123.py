import telebot
from bs4 import BeautifulSoup
import requests

# Токен вашего Telegram-бота
TOKEN = "7574322137:AAFhXhZAXK1Er5puFIwuhg2yQJr-RFVuIZE"
bot = telebot.TeleBot(TOKEN)

# URL для парсинга
URL = "https://yandex.ru/pogoda/kemerovo?lat=55.3552&lon=86.086848"

# User-Agent для имитации запроса с браузера
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_sun_times():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Поиск данных о времени восхода и захода солнца
        sun_card = soup.find("div", class_="sun-card__day-duration-value")
        print(sun_card.text)
        if not sun_card:
            return "Не удалось найти данные о восходе и заходе солнца."

        sun_times = sun_card.find_all("div", class_="sun-card__time")
        if len(sun_times) < 2:
            return "Не удалось получить точные данные о времени солнца."

        sunrise = sun_times[0].text.strip()
        sunset = sun_times[1].text.strip()

        return f"Восход солнца: {sunrise}\nЗакат солнца: {sunset}"
    except Exception as e:
        return f"Ошибка при получении данных: {e}"


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши /sun, чтобы узнать время восхода и захода солнца в Кемерово.")


# Обработчик команды /sun
@bot.message_handler(commands=["sun"])
def send_sun_info(message):
    sun_info = get_sun_times()
    bot.reply_to(message, sun_info)


# Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True)
