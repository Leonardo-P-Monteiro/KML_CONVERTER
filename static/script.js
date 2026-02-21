document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("kmlForm");
  const convertBtn = document.getElementById("convertBtn");
  const btnText = document.getElementById("btnText");
  const btnLoader = document.getElementById("btnLoader");
  const kmlInput = document.getElementById("kmlInput");
  const alertArea = document.getElementById("alertArea");

  form.addEventListener("submit", function (e) {
    // 1. Limpa alertas anteriores
    alertArea.innerHTML = "";
    const kmlData = kmlInput.value.trim();

    // 2. Validação no Frontend
    if (!kmlData) {
      // Impede o envio se estiver vazio
      e.preventDefault();
      showAlert("Por favor, insira o código KML.", "danger");
      return;
    }

    /* 3. Envio do Formulário
       Não usamos e.preventDefault() aqui para permitir que o formulário 
       faça o POST tradicional para o Django.
    */

    // Ativa o visual de carregamento
    setLoading(true);

    /* 4. Reset Automático (O Pulo do Gato)
       Como o retorno é um download, a página não atualiza.
       Definimos um tempo seguro (ex: 2000ms = 2 segundos) para reativar o botão.
       Isso dá feedback visual de que o sistema processou o pedido.
    */
    setTimeout(() => {
      setLoading(false);
      showAlert(
        "O download do seu Excel deve começar em instantes!",
        "success",
      );
      // Opcional: Limpar o campo após o sucesso
      kmlInput.value = "";
    }, 2000);
  });

  // Função para alternar o estado do botão (Normal / Carregando)
  function setLoading(isLoading) {
    if (isLoading) {
      convertBtn.disabled = true;
      btnText.classList.add("d-none");
      btnLoader.classList.remove("d-none");
    } else {
      convertBtn.disabled = false;
      btnText.classList.remove("d-none");
      btnLoader.classList.add("d-none");
    }
  }

  // Função para exibir alertas Bootstrap
  function showAlert(message, type) {
    alertArea.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
  }
});
