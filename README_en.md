[📖 Russian version of the guide is available here](https://github.com/npcx42/TeleRelayBot/blob/main/README.md)

# TeleRelayBot

### ⚠️ First update in a while!

## Description  
This bot automatically forwards messages from a Telegram channel to your Discord server.

### ❗ Requirements:  
**Your Telegram channel must be public.**

## Installation

### 1️⃣ Install Python and dependencies  
- The bot works with **Python 3.10 and newer**. You can download it [here](https://www.python.org/downloads/).  
- When installing, make sure to check **"Add to PATH"**, otherwise, the bot won’t work.  
- After installation, **restart your computer** (optional, but recommended).

### 2️⃣ Install dependencies  
Open the terminal in the folder with the bot and run this command:
```sh
pip install -r requirements.txt
```

### 3️⃣ Set up the config file  
Open the `config.json` file and fill it in with your details:
```json
{
    "token_bot": "your_bot_token",
    "channel_url": "https://t.me/s/channel",
    "discord_bot_id": "your_bot_id",
    "discord_channel_id": "channel_id",
    "discord_thread_name": "Comments",
    "discord_debug_access_uid": ["user_id1", "user_id2"],
    "media_support": true,
    "download_media": true,
    "auto_delete_messages": false,
    "auto_create_threads": false
}
```

Keep in mind:
- You can enable/disable media support in the config.
- You can turn off auto-deleting messages and auto-creating threads.

Once everything is set up, just run ```python bot.py``` and enjoy the bot! 🚀

## ❓ Feedback  
If you're having issues with the bot, create an issue on GitHub: [here](https://github.com/npcx42/TeleRelayBot/issues/new).  
~~Discord support is temporarily unavailable. For now.~~ 