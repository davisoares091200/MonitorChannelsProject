from telethon import TelegramClient, errors
from telethon.tl.custom import Button
from interface_send import capturar_dados  # Importa a função para capturar dados da interface
from dotenv import load_dotenv
from time import sleep
import asyncio
import sys
import os

load_dotenv('.env')

# Configurações do Telethon
api_id = os.getenv("API_ID").strip()
api_hash = os.getenv("API_HASH").strip()
canal_id = int(os.getenv("TARGET_CHANNEL").strip())  # ID do canal numérico
bot_username = os.getenv("BOT_USERNAME").strip() # Nome de usuário do bot VIP (sem @)

# Inicializa o cliente Telethon
client = TelegramClient('sessao', api_id, api_hash)

# Função para verificar se o cliente tem acesso ao canal
async def verificar_acesso_canal():
    try:
        await client.get_entity(canal_id)
        print("Acesso ao canal verificado com sucesso!")
        return True
    except errors.ChannelPrivateError:
        print("Erro: o cliente não tem acesso ao canal. Verifique se o cliente é administrador.")
        return False
    except Exception as e:
        print(f"Erro ao verificar acesso ao canal: {e}")
        return False

# Função para enviar a mensagem
async def enviar_mensagem(mensagem, video_path):
    # Cria o link azul com markdown
    mensagem_com_link = f"{mensagem}\n\n[🔥 VEM SER VIP 🔥](https://t.me/{bot_username}?start=vip)\n[🔥 VEM SER VIP 🔥](https://t.me/{bot_username}?start=vip)"

    try:
        if video_path:
            print(f"Tentando enviar um vídeo/imagem com legenda: {mensagem_com_link}")  # Log de envio de vídeo/imagem
            await client.send_file(
                canal_id,
                video_path,
                caption=mensagem_com_link,
                parse_mode='markdown'  # Habilita markdown para formatação do link
            )
            print("Vídeo/imagem enviado com sucesso!")
            sleep(3)
            await client.disconnect()
        else:
            print(f"Tentando enviar uma mensagem de texto: {mensagem_com_link}")  # Log de envio de texto
            await client.send_message(
                canal_id,
                mensagem_com_link,
                parse_mode='markdown'  # Habilita markdown para formatação do link
            )
            print("Mensagem de texto enviada com sucesso!")  # Confirmação de envio de texto
            sleep(3)
            await client.disconnect()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")  # Log de erro detalhado


# Função principal
async def main():
    await client.start()  # Certifica-se de que o cliente está conectado
    print("Cliente conectado!")  # Confirmação de conexão

    # Verifica o acesso ao canal
    if await verificar_acesso_canal():
        # Captura a mensagem e o caminho do arquivo da interface
        mensagem, caminho_arquivo = capturar_dados()
        # Envia a mensagem após confirmar o acesso ao canal
        await enviar_mensagem(mensagem, caminho_arquivo)
        sys.exit()
    else:
        print("A aplicação será encerrada, pois o cliente não tem acesso ao canal.")
        await client.disconnect()

# Executa o loop do Telethon e o programa principal
asyncio.run(main())
