# config.py

import os


class Config:
    """
    Classe de configuração para a aplicação Flask.
    Define variáveis de ambiente e caminhos importantes.
    """
    SECRET_KEY = os.environ.get(
        'Gallifrey#Falls') or 'sua_chave_secreta_muito_segura'
    DATABASE = 'instance/banco.db'
    # Caminho para o diretório de upload de imagens de imóveis
    UPLOAD_FOLDER = os.path.join('static', 'img', 'imoveis')
    # Certifica-se de que o diretório de upload existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
