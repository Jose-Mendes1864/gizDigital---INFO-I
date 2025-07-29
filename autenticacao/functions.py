import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
def caminho_imagem(instance, filename):
    # Pega a extensão do arquivo original
    extensao = filename.split('.')[-1]
    
    # Garante um nome de arquivo seguro
    nome_formatado = instance.nome.replace(' ', '_').lower() + '_Photo'
    caminho = instance.pasta_destino
    # Cria o novo nome do arquivo
    novo_nome = f"{nome_formatado}_{instance.id}.{extensao}" #deixando

    # Retorna o caminho relativo
    return os.path.join(caminho, novo_nome)


def enviar_email():
    # Informações do remetente
    email_remetente = settings.EMAIL_HOST_USER
    senha =  settings.EMAIL_HOST_PASSWORD # veja nota abaixo

    # Informações do destinatário
    email_destinatario = 'spamendes0501@gmail.com'
    assunto = 'Assunto do E-mail'
    mensagem = 'Olá, este é um e-mail enviado pelo Python!'
    print(email_remetente)
    # Criar a mensagem
    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    # Enviar o e-mail
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(email_remetente, senha)
        servidor.send_message(msg)
        servidor.quit()
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar o e-mail: {e}')