import customtkinter as ctk
from tkinter import filedialog

# Função para criar a interface e capturar dados
def capturar_dados():
    app = ctk.CTk()
    app.title("Envio de Mensagens para o Canal")
    app.geometry("400x300")

    # Campo de texto para a mensagem
    lbl_mensagem = ctk.CTkLabel(app, text="Digite a Mensagem:")
    lbl_mensagem.pack(pady=10)

    entrada_mensagem = ctk.CTkEntry(app, width=300)
    entrada_mensagem.pack(pady=5)

    # Variável para armazenar o caminho do arquivo selecionado
    dados = {'mensagem': None, 'caminho_arquivo': None}

    # Função para selecionar o arquivo de vídeo ou imagem
    def selecionar_arquivo():
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Arquivos de Vídeo e Imagem", "*.mp4 *.mov *.avi *.jpg *.jpeg *.png")]
        )
        dados['caminho_arquivo'] = caminho_arquivo
        lbl_video_selecionado.configure(text=f"Arquivo selecionado: {caminho_arquivo.split('/')[-1]}")
        print(f"Arquivo selecionado: {caminho_arquivo}")  # Log do arquivo selecionado

    # Botão para selecionar o arquivo
    btn_selecionar_arquivo = ctk.CTkButton(app, text="Selecionar Vídeo/Imagem", command=selecionar_arquivo)
    btn_selecionar_arquivo.pack(pady=10)

    # Label para exibir o nome do arquivo selecionado
    lbl_video_selecionado = ctk.CTkLabel(app, text="Nenhum arquivo selecionado")
    lbl_video_selecionado.pack(pady=5)

    # Função chamada ao clicar no botão "Enviar"
    def enviar_mensagem():
        dados['mensagem'] = entrada_mensagem.get()
        app.quit()  # Fecha a interface ao clicar em "Enviar"

    # Botão de envio
    btn_enviar = ctk.CTkButton(app, text="Enviar", command=enviar_mensagem)
    btn_enviar.pack(pady=20)

    app.mainloop()
    app.destroy()  # Garante que a janela seja destruída após fechar

    return dados['mensagem'], dados['caminho_arquivo']
