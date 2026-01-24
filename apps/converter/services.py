import pandas as pd
from fastkml import kml
import re
import os


def ler_kml_como_texto(caminho_do_arquivo):
    """

    Abre um arquivo KML e retorna seu conteúdo como uma string.

    """  # noqa: D200
    try:
        with open(caminho_do_arquivo, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        return conteudo
    except FileNotFoundError:
        return "Erro: Arquivo não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"


# Exemplo de uso:
texto_kml = ler_kml_como_texto('C:\\Users\\leona\\Documents\\KML_CONVERTER\\KML_CONVERTER\\docs\\kml_exemple.kml')
print(texto_kml)


def mapear_telefones_regex(conteudo_raw):
    """
    Cria um dicionário {Nome_Empresa: Telefone} varrendo o arquivo bruto.
    Necessário pois <phoneNumber> não é uma tag padrão do KML e o FastKML
    pode ignorá-la durante o parse.
    """  # noqa: D205
    mapa_telefones = {}
    # Procura por blocos que tenham <name> seguido (eventualmente) de <phoneNumber>
    # O padrão considera quebras de linha e outros caracteres entre as tags
    padrao = r'<name>(.*?)</name>.*?<phoneNumber>(.*?)</phoneNumber>'

    matches = re.findall(padrao, conteudo_raw, re.DOTALL)

    for nome, telefone in matches:
        # Limpa espaços extras e adiciona ao mapa
        mapa_telefones[nome.strip()] = telefone.strip()

    return mapa_telefones

