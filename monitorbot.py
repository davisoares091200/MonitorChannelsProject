from telethon import TelegramClient, events, types
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Credenciais da API do Telegram
API_ID = os.getenv("API_ID","").strip()  # MINHA CHAVE
API_HASH = os.getenv("API_HASH","").strip()


# IDs dos canais para monitorar
CHANNELS_TO_MONITOR = os.getenv("CHANNELS_TO_MONITOR","").split(",")  # Substitua pelos IDs reais

CHANNELS_TO_MONITOR = [int(channel) for channel in CHANNELS_TO_MONITOR]

# Seu canal para envio
TARGET_CHANNEL = int(os.getenv("TARGET_CHANNEL",""))

# Configuração do cliente
client = TelegramClient('session_name', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS_TO_MONITOR))
async def handler(event):
    # Verifica se é uma mídia (foto ou vídeo)
    if event.message.media:
        print("Peguei uma mídia")
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
                else:
                    # Caso não tenha atributos, envia normalmente
                    await client.send_file(TARGET_CHANNEL, media_path)
            else:
                # Envia outros tipos de mídia
                await client.send_file(TARGET_CHANNEL, media_path)

            print(f'Mídia enviada: {media_path}')
        finally:
            # Remove o arquivo local após envio para economizar espaço
            os.remove(media_path)
            print(f"Mídia removida: {media_path}")

async def main():
    print("Bot iniciado e monitorando canais...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
