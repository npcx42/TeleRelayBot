import json
import requests
import os
from bs4 import BeautifulSoup
import aiocron
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Tuple, List

# Создаем директорию для временных файлов
TEMP_DIR = "temp_media"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Загрузка конфигурации из JSON файла
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

TOKEN_BOT = config["token_bot"]
CHANNEL_URL = config["channel_url"]
DISCORD_BOT_ID = int(config["discord_bot_id"])
DISCORD_CHANNEL_ID = int(config["discord_channel_id"])
DISCORD_THREAD_NAME = config["discord_thread_name"]
DISCORD_DEBUG_ACCESS = config["discord_debug_access_uid"]  # список id в виде строк
MEDIA_SUPPORT = config.get("media_support", False)
DOWNLOAD_MEDIA = config.get("download_media", False)
AUTO_DELETE_MESSAGES = config.get("auto_delete_messages", True)
AUTO_CREATE_THREADS = config.get("auto_create_threads", True)

class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.last_message = None  # Память для последнего отправленного поста
        self.last_media_urls = []

    async def setup_hook(self):
        # Регистрируем slash-команды в дереве команд
        self.tree.add_command(debug_command)
        self.tree.add_command(getmsg_command)
        await self.tree.sync()
        self.start_channel_check()

    def download_media(self, url: str) -> Optional[str]:
        """Скачивает медиафайл и возвращает путь к нему."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Получаем расширение файла из URL
            file_ext = url.split('.')[-1].split('?')[0]
            file_path = os.path.join(TEMP_DIR, f"media_{hash(url)}.{file_ext}")
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return file_path
        except Exception as e:
            print(f"Ошибка при скачивании медиа: {e}")
            return None

    def fetch_latest_message(self, channel_url: str, ignore_cache: bool = False) -> Tuple[Optional[str], List[str]]:
        """Запрашивает страницу канала и возвращает новый пост и медиа URLs."""
        try:
            response = requests.get(channel_url)
            response.raise_for_status()
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None, []

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all message containers
        message_wraps = soup.find_all("div", class_="tgme_widget_message_wrap")
        
        if not message_wraps:
            print("Сообщения не найдены.")
            return None, []
        
        # Get the last message
        latest_message_wrap = message_wraps[-1]
        
        # Extract text
        text_div = latest_message_wrap.find("div", class_="tgme_widget_message_text")
        new_text = text_div.get_text(strip=True) if text_div else ""
        
        # Extract media URLs
        media_urls = []
        if MEDIA_SUPPORT:
            # Images
            images = latest_message_wrap.find_all("a", class_="tgme_widget_message_photo_wrap")
            for img in images:
                style = img.get('style')
                if style:
                    url = style.split('url(\'')[1].split('\')')[0]
                    media_urls.append(url)
            
            # Videos
            videos = latest_message_wrap.find_all("video", class_="tgme_widget_message_video")
            media_urls.extend(video.get('src') for video in videos if video.get('src'))

        # Check cache
        content_hash = f"{new_text}{''.join(media_urls)}"
        if not ignore_cache and content_hash == self.last_message:
            return None, []

        self.last_message = content_hash
        return new_text, media_urls

    def start_channel_check(self):        # Планировщик, запускаемый по расписанию каждые 5 минут
        @aiocron.crontab("*/1 * * * *")
        async def scheduled_check():
            new_text, media_urls = self.fetch_latest_message(CHANNEL_URL)
            if new_text or media_urls:
                channel = self.get_channel(DISCORD_CHANNEL_ID)
                if channel:
                    try:
                        files = []
                        if MEDIA_SUPPORT and DOWNLOAD_MEDIA and media_urls:
                            for url in media_urls:
                                file_path = self.download_media(url)
                                if file_path:
                                    files.append(discord.File(file_path))
                        
                        # Отправляем сообщение с медиа
                        await channel.send(content=new_text if new_text else None, files=files)
                        
                        # Очищаем временные файлы
                        for file in files:
                            try:
                                os.remove(file.fp.name)
                            except:
                                pass
                                
                    except Exception as e:
                        print(f"Ошибка при отправке сообщения: {e}")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message: discord.Message):
        channelId = message.channel.id
        userId = message.author.id
        bot = message.author.bot

        # Проверка, является ли сообщение от бота
        if bot and userId == DISCORD_BOT_ID:
            if channelId == DISCORD_CHANNEL_ID and AUTO_CREATE_THREADS:
                await message.create_thread(
                    name=DISCORD_THREAD_NAME,
                    reason="Разрешение на комментарии под сообщением"
                )
        else:
            if channelId == DISCORD_CHANNEL_ID and AUTO_DELETE_MESSAGES:
                await message.delete()

# Инициализация бота
intents = discord.Intents.all()
bot = MyBot(command_prefix="!", intents=intents)

# Slash-команды

@app_commands.command(name="debug", description="Проверить работу бота и получить последнее сообщение из Telegram")
async def debug_command(interaction: discord.Interaction):
    if str(interaction.user.id) not in DISCORD_DEBUG_ACCESS:
        await interaction.response.send_message("У вас нет прав для выполнения этой команды.", ephemeral=True)
        return
    new_text, media_urls = bot.fetch_latest_message(CHANNEL_URL)
    
    response_msg = "Бот работает.\n"
    response_msg += f"Автоудаление сообщений: {'включено' if AUTO_DELETE_MESSAGES else 'выключено'}\n"
    response_msg += f"Автосоздание веток: {'включено' if AUTO_CREATE_THREADS else 'выключено'}\n"
    if new_text:
        response_msg += f"Последнее сообщение из Telegram:\n{new_text}\n"
    if MEDIA_SUPPORT and media_urls:
        response_msg += f"Найдено медиафайлов: {len(media_urls)}\n"
    response_msg += f"ID канала Discord: {DISCORD_CHANNEL_ID}"
    
    await interaction.response.send_message(response_msg)

@app_commands.command(name="getmsg", description="Получить последнее сообщение из Telegram")
async def getmsg_command(interaction: discord.Interaction):
    if str(interaction.user.id) not in DISCORD_DEBUG_ACCESS:
        await interaction.response.send_message("У вас нет прав для выполнения этой команды.", ephemeral=True)
        return
        
    new_text, media_urls = bot.fetch_latest_message(CHANNEL_URL, ignore_cache=True)
    
    files = []
    if MEDIA_SUPPORT and media_urls:
        for url in media_urls:
            file_path = bot.download_media(url)
            if file_path:
                files.append(discord.File(file_path))
    
    if new_text or files:
        await interaction.response.send_message(content=new_text, files=files)
        # Clean up temporary files
        for file in files:
            try:
                os.remove(file.fp.name)
            except Exception as e:
                print(f"Failed to delete temporary file: {e}")
    else:
        await interaction.response.send_message("Новых сообщений не найдено.", ephemeral=True)

bot.run(TOKEN_BOT)