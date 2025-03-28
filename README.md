[📖 English version of the guide is available here](https://github.com/npcx42/TeleRelayBot/blob/main/README_en.md)

# TeleRelayBot

### ⚠️ Первое обновление проекта за долгое время!

## Описание  
Этот бот предназначен для автоматической пересылки сообщений из Telegram-канала на ваш сервер Discord.

### ❗ Требования:  
**Канал в Telegram должен быть публичным.**

## Установка:

### 1️⃣ Установка Python и библиотек  
- Бот работает с **Python 3.10 и новее**. Вы можете скачать Python [здесь](https://www.python.org/downloads/).  
- При установке обязательно отметьте опцию **"Add to PATH"**, иначе бот не будет работать.  
- После установки **перезагрузите компьютер** (по желанию).

### 2️⃣ Установка зависимостей  
Откройте терминал в папке с ботом и выполните следующую команду:
```sh
pip install -r requirements.txt
```

### 3️⃣ Настройка конфигурационного файла  
Откройте файл `config.json` и заполните его вашими данными:
```json
{
    "token_bot": "your_bot_token",
    "channel_url": "https://t.me/s/channel",
    "discord_bot_id": "your_bot_id",
    "discord_channel_id": "channel_id",
    "discord_thread_name": "Comments",
    "discord_debug_access_uid": ["user_id2", "user_id2"],
    "media_support": true,
    "download_media": true,
    "auto_delete_messages": false,
    "auto_create_threads": false
}
```

Обратите внимание:
- В конфиге можно включить/выключить поддержку медиа-файлов.
- Вы можете отключить автоудаление сообщений и автосоздание веток.

После завершения настройки напишите ```python bot.py``` и наслаждайтесь работой бота! 🚀

## ❓ Обратная связь  
Если у вас возникли проблемы с ботом, создайте issue на GitHub: [тык](https://github.com/npcx42/TeleRelayBot/issues/new).  
~~Поддержка в Discord временно недоступна. Пока что.~~ 