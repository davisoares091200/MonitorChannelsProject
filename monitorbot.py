import os
import logging
from telethon import TelegramClient, events, types
from dotenv import load_dotenv

load_dotenv('.env')

# Configuração do logger
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,  # Define o nível de log (INFO, DEBUG, ERROR, etc.)
    handlers=[
        logging.FileHandler("bot.log"),  # Log em arquivo
        logging.StreamHandler()         # Log no terminal
    ]
)
logger = logging.getLogger(__name__)

# Credenciais da API do Telegram
API_ID = os.getenv("API_ID", "").strip()
API_HASH = os.getenv("API_HASH", "").strip()

# IDs dos canais para monitorar
CHANNELS_TO_MONITOR = os.getenv("CHANNELS_TO_MONITOR", "").split(",")  # IDs reais
CHANNELS_TO_MONITOR = [int(channel) for channel in CHANNELS_TO_MONITOR]

# Seu canal para envio
TARGET_CHANNEL = int(os.getenv("TARGET_CHANNEL", ""))

# Configuração do cliente
client = TelegramClient('session_name', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS_TO_MONITOR))
async def handler(event):
    # Verifica se é uma mídia (foto ou vídeo)
    if event.message.media:
        logger.info("Mídia detectada. Baixando...")
        media_path = await event.message.download_media()

        try:
            # Verifica se é um vídeo
            if isinstance(event.message.media, types.MessageMediaDocument):
                # Extrai informações de duração e dimensões, se disponíveis
                video_attributes = [
                    attr for attr in event.message.media.document.attributes
                    if isinstance(attr, types.DocumentAttributeVideo)
                ]
                if video_attributes:
                    attributes = video_attributes[0]  # Pega os atributos de vídeo
                    await client.send_file(
                        TARGET_CHANNEL,
                        media_path,
                        attributes=[
                            types.DocumentAttributeVideo(
                                duration=attributes.duration,
                                w=attributes.w,
                                h=attributes.h,
                                supports_streaming=True,
                            )
                        ],
                    )
                    logger.info(f"Vídeo enviado com sucesso: {media_path}")
                else:
                    # Caso não tenha atributos, envia normalmente
                    await client.send_file(TARGET_CHANNEL, media_path)
                    logger.info(f"Arquivo de imagem/GIF enviado: {media_path}")
            else:
                # Envia outros tipos de mídia
                await client.send_file(TARGET_CHANNEL, media_path)
                logger.info(f"Arquivo enviado: {media_path}")
        except Exception as e:
            logger.error(f"Erro ao enviar arquivo: {e}")
        finally:
            # Remove o arquivo local após envio para economizar espaço
            os.remove(media_path)
            logger.info(f"Arquivo local removido: {media_path}")

async def main():
    logger.info("Bot iniciado e monitorando canais...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
