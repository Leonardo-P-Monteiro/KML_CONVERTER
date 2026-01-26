import pandas as pd
from bs4 import BeautifulSoup

PATH_FILE_KML = "docs\\kml_exemple.kml"
PATH_FILE_XLSX = 'docs\\output.xlsx'

def kml_to_xlsx(path_kml_file, output_xlsx_file):
    """
    Explanation.

    Read a KML file exported from Google Earth, extract company data,
    and save it to an Excel file.

    Args:
        path_kml_file (str): Path to access the KML file.
        output_xlsx_file (str): Path where the xlsx file will save.

    Returns:
        None: The function saves the file straightforward on hard disc and
        not return any value.

    """
    print(f"--- Iniciando processamento de: {path_kml_file} ---")

    # 1. Ler o arquivo KML
    try:
        with open(path_kml_file, encoding="utf-8") as f: # noqa: PTH123
            conteudo_kml = f.read()
    except FileNotFoundError:
        print("Erro: Arquivo KML não encontrado.")
        return

    # 2. Parsear com BeautifulSoup usando o parser XML (lxml)
    soup = BeautifulSoup(conteudo_kml, "xml")

    # Lista para armazenar os dados extraídos
    lista_empresas = []

    # 3. Encontrar todos os Placemarks (cada empresa)
    placemarks = soup.find_all("Placemark")
    print(f"Encontrados {len(placemarks)} registros para processar.")

    for placemark in placemarks:
        dados_empresa = {}

        # --- Extração do Nome ---
        tag_name = placemark.find("name")
        dados_empresa["Nome"] = tag_name.text.strip() if tag_name else "N/A"

        # --- Extração do Endereço ---
        tag_address = placemark.find("address")
        dados_empresa["Endereço"] = tag_address.text.strip() if tag_address else "N/A"

        # --- Extração do Telefone ---
        # Nota: phoneNumber não é padrão KML, mas existe no seu arquivo
        tag_phone = placemark.find("phoneNumber")
        dados_empresa["Telefone"] = tag_phone.text.strip() if tag_phone else "N/A"

        # --- Extração do Link (Site/URI) ---
        # A URL está dentro de ExtendedData -> Data name="placepageUri" -> value
        link = "N/A"
        extended_data = placemark.find("ExtendedData")
        if extended_data:
            data_tags = extended_data.find_all("Data", attrs={"name": "placepageUri"})
            for data in data_tags:
                val = data.find("value")
                if val:
                    link = val.text.strip()
                    break
        dados_empresa["Link do Site"] = link

        lista_empresas.append(dados_empresa)

    # 4. Criar DataFrame Pandas
    df = pd.DataFrame(lista_empresas)

    # 5. Salvar para Excel
    try:
        df.to_excel(output_xlsx_file, index=False, engine="openpyxl")
        print(f"--- Sucesso! Arquivo gerado: {output_xlsx_file} ---")
        print(df.head())  # Mostra as primeiras linhas para conferência
    except Exception as e: # noqa: BLE001
        print(f"Erro ao salvar Excel: {e}")


# --- Execução ---
# Substitua 'seu_arquivo.kml' pelo nome real do seu arquivo
if __name__ == "__main__":
    # Cria um arquivo dummy para teste baseado no seu exemplo (opcional, se você já tiver o arquivo)
    # Mas assumindo que você tem o arquivo físico:
    NOME_DO_ARQUIVO_ENTRADA = PATH_FILE_KML
    NOME_DO_ARQUIVO_SAIDA = PATH_FILE_XLSX

    kml_to_xlsx(NOME_DO_ARQUIVO_ENTRADA, NOME_DO_ARQUIVO_SAIDA)
