import re  # Import necessário para dividir os blocos de texto

import defusedxml.ElementTree as Et
import pandas as pd
from bs4 import BeautifulSoup
from defusedxml.common import DefusedXmlException

PATH_FILE_KML = "docs\\kml_exemple.kml"
PATH_FILE_XLSX = "docs\\output.xlsx"
# Regex centralizado para garantir que validação e processamento usem a mesma regra
XML_HEADER_REGEX = r"<\?xml.*?\?>"


def kml_to_xlsx_test_no_request(path_kml_file, output_xlsx_file=PATH_FILE_XLSX):
    """
    Explanation.

    Read a KML file exported from Google Earth (even with multiple concatenated files),
    extract company data, and save it to an Excel file.

    Args:
        path_kml_file (str): Path to access the KML file.
        output_xlsx_file (str): Path where the xlsx file will save.

    Returns:
        None: The function saves the file straightforward on hard disc.

    """
    print(f"--- Iniciando processamento de: {path_kml_file} ---")

    # 1. Ler o arquivo KML bruto
    try:
        with open(path_kml_file, encoding="utf-8") as f:  # noqa: PTH123
            conteudo_kml = f.read()
    except FileNotFoundError:
        print("Erro: Arquivo KML não encontrado.")
        return

    kml_to_xlsx(conteudo_kml, output_xlsx_file)


def kml_to_xlsx(kml_content, output_destination):  # noqa: C901
    """
    Explicação.

    Processa KML e salva no destino (arquivo ou buffer de memória).
    Retorna True se sucesso, False se nenhum dado foi encontrado.
    """
    if not kml_content:
        return False

    # 1. Pré-processamento (Mantido igual)
    blocos_kml = re.split(XML_HEADER_REGEX, kml_content)
    lista_empresas = []
    nomes_processados = set()

    # 2. Iterar sobre blocos (Lógica mantida igual)
    for bloco in blocos_kml:
        if not bloco.strip():
            continue

        soup = BeautifulSoup(bloco, "xml")
        placemarks = soup.find_all("Placemark")

        if len(placemarks) > 0:
            for placemark in placemarks:
                tag_name = placemark.find("name")
                nome_empresa = tag_name.text.strip() if tag_name else "N/A"

                if nome_empresa in nomes_processados:
                    continue
                nomes_processados.add(nome_empresa)

                dados_empresa = {}
                dados_empresa["Nome"] = nome_empresa

                tag_address = placemark.find("address")
                dados_empresa["Endereço"] = (
                    tag_address.text.strip() if tag_address else "N/A"
                )

                tag_phone = placemark.find("phoneNumber")
                dados_empresa["Telefone"] = (
                    tag_phone.text.strip() if tag_phone else "N/A"
                )

                link = "N/A"
                extended_data = placemark.find("ExtendedData")
                if extended_data:
                    data_tag = extended_data.find(
                        "Data", attrs={"name": "placepageUri"},
                    )
                    if data_tag:
                        val = data_tag.find("value")
                        if val:
                            link = val.text.strip()
                dados_empresa["Link do Site"] = link
                lista_empresas.append(dados_empresa)

    # Verifica se encontrou algo
    if not lista_empresas:
        return False

    # 3. Gerar Excel no destino informado (Buffer ou Arquivo)
    try:
        df = pd.DataFrame(lista_empresas)
        # O engine openpyxl sabe escrever tanto em arquivo quanto em BytesIO
        df.to_excel(output_destination, index=False, engine="openpyxl")
        return True  # noqa: TRY300
    except Exception as e:  # noqa: BLE001
        print(f"Erro ao gerar Excel: {e}")
        return False


def is_valid_kml(content):
    """
    Verifica se o conteúdo contém estruturas KML válidas.

    Suportando múltiplos arquivos concatenados.

    Args:
        content (str | bytes): O corpo da requisição ou string do POST.

    Returns:
        bool: True se encontrar pelo menos um bloco KML válido.

    """
    if not content:
        return False

    # Garante que content seja string para o Regex funcionar
    if isinstance(content, bytes):
        try:
            content_str = content.decode("utf-8")
        except Exception:  # noqa: BLE001
            return False
    else:
        content_str = content

    # 1. Divide o conteúdo usando a mesma lógica do processador
    # Isso permite isolar cada declaração <?xml ...?> e seu conteúdo
    blocos = re.split(XML_HEADER_REGEX, content_str)

    kml_validos_encontrados = 0

    for bloco in blocos:
        if not bloco.strip():
            continue

        try:
            # 2. Tenta parsear o bloco isolado como XML
            # O defusedxml protege contra ataques, mas exige um XML bem formado (raiz única)
            root = Et.fromstring(bloco.strip())

            # 3. Verifica se a raiz é 'kml'
            # O .tag retorna algo como "{http://www.opengis.net/kml/2.2}kml"
            # Usamos endswith para ignorar o namespace
            if root.tag.strip().lower().endswith("kml"):
                kml_validos_encontrados += 1

        except (Et.ParseError, DefusedXmlException, ValueError):
            # Se falhar o parse deste bloco específico, apenas ignoramos e tentamos o próximo.
            # Isso permite que haja "sujeira" entre os arquivos colados sem invalidar o todo.
            continue
        except Exception:  # noqa: BLE001, S112
            continue

    # Retorna True apenas se encontrou pelo menos uma estrutura KML válida
    return kml_validos_encontrados > 0


# --- Execução ---
if __name__ == "__main__":
    NOME_DO_ARQUIVO_ENTRADA = PATH_FILE_KML
    NOME_DO_ARQUIVO_SAIDA = PATH_FILE_XLSX

    kml_to_xlsx_test_no_request(NOME_DO_ARQUIVO_ENTRADA, NOME_DO_ARQUIVO_SAIDA)
