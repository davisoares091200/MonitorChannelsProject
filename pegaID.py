from telethon import TelegramClient
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Substitua pelos seus valores
api_id = os.getenv("API_ID").strip()
api_hash = os.getenv("API_HASH").strip()

# Crie uma sessão do cliente do Telethon
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    # Conecte-se ao Telegram
    await client.start()

    # Lista todos os diálogos (conversas, grupos, canais) disponíveis
    async for dialog in client.iter_dialogs():
        # Pega o nome do diálogo e o ID
        name = dialog.name
        dialog_id = dialog.id
        entity_type = dialog.entity.__class__.__name__

        # Tenta obter o username, se existir
        username = dialog.entity.username if hasattr(dialog.entity, 'username') else 'N/A'

        print(f"Nome: {name}, ID: {dialog_id}, Tipo: {entity_type}, Username: {username}")


with client:
    client.loop.run_until_complete(main())
    channel = int(input("\nDigite o ID do canal que deseja monitorar: "))
    print('\n')