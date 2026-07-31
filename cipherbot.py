import telebot

# 1. Сюда вставляешь токен от @BotFather
TOKEN = "8892542621:AAEN3A_tDzGELfA7msuXp6rRYdSb02v_x4k"
bot = telebot.TeleBot(TOKEN)

# 2. БЕЛЫЙ СПИСОК (Впиши сюда числовые ID себя и своих друзей)
ALLOWED_USERS = [
    1029979552,  # Твой ID
    267758514   # ID друга
]

# Алфавиты для фирменного шифрования WAKO CYPHER
RU_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RU_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
EN_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_LOWER = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"

def process_text(text, key, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        text = text[::-1]

    for i, char in enumerate(text):
        shift = i + key 
        if mode == 'decrypt':
            shift = -shift

        if char in RU_UPPER:
            result += RU_UPPER[(RU_UPPER.index(char) + shift) % 33]
        elif char in RU_LOWER:
            result += RU_LOWER[(RU_LOWER.index(char) + shift) % 33]
        elif char in EN_UPPER:
            result += EN_UPPER[(EN_UPPER.index(char) + shift) % 26]
        elif char in EN_LOWER:
            result += EN_LOWER[(EN_LOWER.index(char) + shift) % 26]
        elif char in DIGITS:
            result += DIGITS[(DIGITS.index(char) + shift) % 10]
        else:
            result += char

    if mode == 'encrypt':
        result = result[::-1]

    return result

# Проверка на свой / чужой
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "⛔ Доступ запрещен. Этот бот только для своих.")
        return

    bot.reply_to(message, 
                 "🔐 *WAKO CYPHER BOT активирован*\n\n"
                 "Используй команды:\n"
                 "🔸 /enc КЛЮЧ ТЕКСТ — зашифровать\n"
                 "🔸 /dec КЛЮЧ ТЕКСТ — расшифровать\n\n"
                 "Пример: /enc 7 Привет мир", 
                 parse_mode="Markdown")

# Команда шифрования /enc
@bot.message_handler(commands=['enc'])
def handle_encrypt(message):
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "⛔ Доступ запрещен.")
        return

    try:
        parts = message.text.split(maxsplit=2)
        key = int(parts[1])
        text = parts[2]
        
        res = process_text(text, key, mode='encrypt')
        bot.reply_to(message, f"🔐 *Зашифровано:*\n{res}", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "⚠️ Ошибка! Пиши строго так:\n/enc 7 ТвойТекст", parse_mode="Markdown")

# Команда расшифрования /dec
@bot.message_handler(commands=['dec'])
def handle_decrypt(message):
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "⛔ Доступ запрещен.")
        return

    try:
        parts = message.text.split(maxsplit=2)
        key = int(parts[1])
        text = parts[2]
        
        res = process_text(text, key, mode='decrypt')
        bot.reply_to(message, f"🔓 *Расшифровано:*\n{res}", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "⚠️ Ошибка! Пиши строго так:\n/dec 7 ТвойТекст", parse_mode="Markdown")

print("Бот запущен и охраняет доступ...")
bot.infinity_polling()