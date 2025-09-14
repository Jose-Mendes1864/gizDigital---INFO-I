import os
import smtplib
import secrets
from django.http import HttpResponse
from django.shortcuts import redirect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from django.template.loader import render_to_string 
import secrets
import threading #assincrona que da pro gasto


def caminho_imagem(instance, filename):
  
    # Pega a extensão do arquivo original
    try:
        extensao = filename.split('.')[-1]
        
        # Garante um nome de arquivo seguro
        nome_formatado = instance.username.replace(' ', '_').lower() + '_Photo'
        caminho = instance.pasta_destino

        # Cria o novo nome do arquivo
        novo_nome = f'{nome_formatado}_{secrets.token_hex(4)}.{extensao}' 

        # Retorna o caminho relativo
        print(os.path.join(caminho, novo_nome))
        return os.path.join(caminho, novo_nome)
    
    except Exception as e:
        print(f'O erro é {e}')

def enviar_email(email_destinatario, codigo_aleatorio):
   
    try:
         # Informações do remetente
        email_remetente = settings.EMAIL_HOST_USER
        senha =  settings.EMAIL_HOST_PASSWORD # veja nota abaixo

        # Informações do destinatário
        assunto = 'Recuperação de senha'

       

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
        
    except Exception as e:
        return f'error+{e}'
    

def enviar_email_async(email_destinatario,codigo_aleatorio):
    thread = threading.Thread(target=enviar_email, args=(email_destinatario,codigo_aleatorio))
    thread.start()

