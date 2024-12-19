from telethon import TelegramClient, types
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from collections import deque
from datetime import datetime
from pegaID import channel
from dotenv import load_dotenv
import os


load_dotenv('.env')
# Configurações do cliente
api_id = int(os.getenv("API_ID").strip())  # Substitua pelo seu
api_hash = os.getenv("API_HASH").strip()  # Substitua pelo seu
source_channel = channel  # ID ou username do canal de origem
target_channel = int(os.getenv("TARGET_CHANNEL").strip())#-1002250175818  # ID ou username do canal de destino
limit = int(input("\nDigite quantas mensagens você deseja monitorar: "))

# Inicializa o cliente do Telethon
client = TelegramClient('session_name', api_id, api_hash)

# Função principal
async def main():
    # Fila para armazenar os IDs das mensagens
    message_queue = deque()

    # Obtém as últimas mensagens do canal de origem
    async for message in client.iter_messages(source_channel, limit=limit):
        # Verifica se a mensagem contém foto, GIF ou vídeo
        if isinstance(message.media, MessageMediaPhoto):
            message_queue.append(message.id)
            print("Foto encontrada")
        elif isinstance(message.media, MessageMediaDocument):
            if getattr(message.media, "document", None):
                for attr in message.media.document.attributes:
                    if isinstance(attr, types.DocumentAttributeVideo) and attr.duration <= 300:
                        message_queue.append(message.id)
                        print(f"Vídeo com {attr.duration} segundos encontrado")
                        break
                else:
                    # GIFs sem atributo de vídeo
                    message_queue.append(message.id)
                    print("GIF encontrado")

    print(f"Encontradas {len(message_queue)} mensagens com mídias (fotos, vídeos, GIFs).")

    # Processa cada mensagem na fila
    while message_queue:
        msg_id = message_queue.popleft()
        try:
            # Obtém a mensagem pelo ID
            message = await client.get_messages(source_channel, ids=msg_id)
            if message.media:
                print(f"Baixando mídia: {datetime.now()}")
                # Baixa a mídia no mesmo diretório do script
                file_path = await client.download_media(message, '.')
                print(f"Mídia {file_path} baixada: {datetime.now()}")

                # Verifica se é vídeo com atributos
                if isinstance(message.media, MessageMediaDocument):
                    attributes = []
                    for attr in message.media.document.attributes:
                        if isinstance(attr, types.DocumentAttributeVideo):
                            # Recria os atributos do vídeo
                            attributes.append(
                                types.DocumentAttributeVideo(
                                    duration=attr.duration,
                                    w=attr.w,
                                    h=attr.h,
                                    supports_streaming=True
                                )
                            )

                    # Envia vídeo com atributos recriados
                    if attributes:
                        await client.send_file(
                            target_channel,
                            file_path,
                            attributes=attributes,
                            caption=""  # Sem legenda
                        )
                        print(f"Vídeo {file_path} enviado para o canal {target_channel}")
                    else:
                        # Envia GIFs
                        await client.send_file(
                            target_channel,
                            file_path,
                            caption=""
                        )
                        print(f"GIF {file_path} enviado para o canal {target_channel}")
                else:
                    # Envia fotos
                    await client.send_file(
                        target_channel,
                        file_path,
                        caption=""
                    )
                    print(f"Foto {file_path} enviada para o canal {target_channel}")

                # Remove o arquivo do disco após o envio
                os.remove(file_path)
                print(f"Mídia apagada: {file_path}")

        except Exception as e:
            print(f"Erro ao processar a mensagem {msg_id}: {e}")

# Executa o cliente
with client:
    client.loop.run_until_complete(main())
    input("Pressione ENTER para finalizar: ")
