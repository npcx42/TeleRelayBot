[📖 English version of the guide is available here](https://github.com/npcx42/telegram-to-discord-bot/blob/main/README_en.md)
# TeleRelayBot 

### ⚠️ Первое обновление проекта за долгое время!  

## 📌 Описание  
Этот бот автоматически пересылает сообщения из Telegram-канала на ваш сервер в Discord.  

## 🔧 Установка  

### ❗ Требования:  
✅ **Канал в Telegram должен быть публичным**  

### 1️⃣ Установка Python и библиотек  
- Бот работает с **Python 3.10 и новее**. Скачать можно [здесь](https://www.python.org/downloads/).  
- При установке **отметьте "Add to PATH"**, иначе скрипт не будет работать.  
- После установки **перезагрузите компьютер** (желательно).  

### 2️⃣ Установка зависимостей  
Откройте терминал в папке со скриптом и выполните:  
```sh
pip install -r requirements.txt
```  

### 3️⃣ Настройка конфига  
Откройте файл `config.json` и укажите ваши данные:  
```json
{
  "TOKEN_BOT": "Ваш_токен_бота",
  "CHANNEL_URL": "https://t.me/s/имяканала",
  "DISCORD_CHANNEL_ID": "ID_канала_Discord",
  "DISCORD_BOT_ID": "ID_бота_Discord"
  "discord_debug_access_uid": ["your id", "your friend id"]
}
```  
После этого можно запускать скрипт и пользоваться ботом! 🚀  

## ❓ Обратная связь  
Если бот не работает, создайте issue на GitHub: [тык](https://github.com/npcx42/telegram-to-discord-bot/issues/new).  
~~Поддержка в Discord временно недоступна.~~
