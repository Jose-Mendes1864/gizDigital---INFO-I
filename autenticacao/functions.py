import os
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from django.template.loader import render_to_string 

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


def enviar_email(email_destinatario):
   
    try:
         # Informações do remetente
        email_remetente = settings.EMAIL_HOST_USER
        senha =  settings.EMAIL_HOST_PASSWORD # veja nota abaixo

        # Informações do destinatário
        assunto = 'Recuperação de senha'

        codigo_aleatorio = ' '.join(str(secrets.randbelow(10)) for _ in range(6))

        html_content = render_to_string('arquivoEmail.html', {'codigo': codigo_aleatorio})

        mensagem_simples= f'Ola, seu código é {codigo_aleatorio}'


    
        # Criar a mensagem
        msg = MIMEMultipart('alternative') #O tipo 'alternative' indica que as partes do e-mail são alternativas do mesmo conteúdo, preferindo o HTML quando possível.
        msg['From'] = email_remetente
        msg['To'] = email_destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem_simples, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        # Enviar o e-mail

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(email_remetente, senha)
        servidor.send_message(msg)
        servidor.quit()
        return codigo_aleatorio
    except Exception as e:
        return f'error+{e}'