import os
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
