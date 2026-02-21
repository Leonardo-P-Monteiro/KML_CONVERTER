import io

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from .services import is_valid_kml, kml_to_xlsx


class ViewTest(View):
    def get(self, request, *args, **kwargs):  # noqa: ARG002
        return render(request, "converter/home.html")

    def post(self, request, *args, **kwargs):  # noqa: ARG002
        # 1. Pega os dados do formulário
        kml_content = request.POST.get("kml_data")

        # 2. Validação básica
        if not kml_content or not is_valid_kml(kml_content):
            erro_message = 'KML inválido ou vazio.'
            return render(request, "converter/home.html", {"erro": erro_message})

        # 3. Cria o arquivo na memória RAM
        excel_buffer = io.BytesIO()

        # 4. Chama o serviço passando o buffer como destino
        sucesso = kml_to_xlsx(kml_content, excel_buffer)

        if not sucesso:
            erro_message = 'Nenhuma empresa encontrada no KML fornecido.'
            return render(request, "converter/home.html", {"erro": erro_message})

        # 5. Prepara o buffer para leitura (volta o ponteiro para o início)
        excel_buffer.seek(0)

        # 6. Retorna o download
        response = FileResponse(
            excel_buffer,
            as_attachment=True,
            filename="empresas_convertidas.xlsx",
        )

        return response
