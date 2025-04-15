document.getElementById("language-button").addEventListener("click", () => {
    const languageButton = document.getElementById("language-button");
    const flagIcon = languageButton.querySelector("img");
    const title = document.getElementById("title");
    const uploadText = document.getElementById("upload-text");
    const customFileUpload = document.getElementById("custom-file-upload"); // Label do botão "Escolher Arquivo"
    const uploadButton = document.getElementById("upload-button");

    // Verifica o idioma atual com base no atributo "alt" da bandeira
    if (flagIcon.getAttribute("alt") === "English") {
        // Mudar para português
        flagIcon.setAttribute("src", "img/bandeira_brasil.jpg");
        flagIcon.setAttribute("alt", "Português");
        languageButton.textContent = " PT";
        languageButton.prepend(flagIcon);
        title.textContent = "Search IP";
        uploadText.textContent = "Upload the .pdf file or spreadsheet";
        customFileUpload.textContent = "Choose File"; // Atualiza o texto do botão "Escolher Arquivo"
        uploadButton.textContent = "Upload";
    } else {
        // Mudar para inglês
        flagIcon.setAttribute("src", "img/us_flag.png");
        flagIcon.setAttribute("alt", "English");
        languageButton.textContent = " EN";
        languageButton.prepend(flagIcon);
        title.textContent = "Procurar IP";
        uploadText.textContent = "Faça upload do arquivo .pdf ou da planilha";
        customFileUpload.textContent = "Escolher Arquivo"; 
        uploadButton.textContent = "Upload";
    }
});

document.getElementById("file-upload").addEventListener("change", async (event) => {
    const file = event.target.files[0];

    if (file && file.type === "application/pdf") {
        // Importa o pdf.js dinamicamente
        const pdfjsModule = await import("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js");
        // Acessa o módulo real através da propriedade "default"
        const pdfjsLib = pdfjsModule.default;
        
        // Abre o documento PDF usando a URL do arquivo
        const loadingTask = pdfjsLib.getDocument(URL.createObjectURL(file));
        const pdf = await loadingTask.promise;

        // Verifica se o PDF possui mais de 15 páginas e, se sim, alerta o usuário e limpa o campo
        if (pdf.numPages > 15) {
            alert("O arquivo PDF não pode ter mais de 15 páginas.");
            event.target.value = ""; // Limpa o campo de upload
        }
    }
});

// Função para exibir a mensagem de arquivo selecionado
function showFileSelectedMessage(fileName) {
    let fileMessageDiv = document.getElementById("file-selected-message");
    if (!fileMessageDiv) {
        fileMessageDiv = document.createElement("div");
        fileMessageDiv.id = "file-selected-message";
        // Estilo opcional para a mensagem
        fileMessageDiv.style.marginTop = "10px";
        fileMessageDiv.style.fontStyle = "italic";
        fileMessageDiv.style.color = "#333";
        // Insere a mensagem dentro do container principal (ou no body, se não encontrar o container)
        const container = document.querySelector(".container") || document.body;
        container.appendChild(fileMessageDiv);
    }
    fileMessageDiv.textContent = "Arquivo selecionado: " + fileName;
}

// Função para exibir a mensagem de arquivo selecionado
function showFileSelectedMessage(fileName) {
    let fileMessageDiv = document.getElementById("file-selected-message");
    if (!fileMessageDiv) {
        fileMessageDiv = document.createElement("div");
        fileMessageDiv.id = "file-selected-message";
        // Estilo opcional para a mensagem
        fileMessageDiv.style.marginTop = "10px";
        fileMessageDiv.style.fontStyle = "italic";
        fileMessageDiv.style.color = "#ffffff";
        // Insere a mensagem dentro do container principal (ou no body, se não encontrar o container)
        const container = document.querySelector(".container") || document.body;
        container.appendChild(fileMessageDiv);
    }
    fileMessageDiv.textContent = "Arquivo selecionado: " + fileName;
}

// Função para exibir uma notificação de sucesso no canto superior direito
function showUploadSuccessMessage(message) {
    let successDiv = document.getElementById("upload-success");
    if (!successDiv) {
        // Cria o elemento se não existir
        successDiv = document.createElement("div");
        successDiv.id = "upload-success";
        // Configura a estilização
        successDiv.style.position = "fixed";
        successDiv.style.top = "10px";
        successDiv.style.right = "10px";
        successDiv.style.backgroundColor = "#4CAF50";
        successDiv.style.color = "white";
        successDiv.style.padding = "10px 15px";
        successDiv.style.borderRadius = "5px";
        successDiv.style.boxShadow = "0 2px 4px rgba(0,0,0,0.2)";
        successDiv.style.zIndex = "1000";
        successDiv.style.display = "none";
        document.body.appendChild(successDiv);
    }
    successDiv.textContent = message;
    successDiv.style.display = "block";
    setTimeout(() => {
        successDiv.style.display = "none";
    }, 3000);
}

function showCarregando(display) {
    let carregandoDiv = document.getElementById("carregando");
    if (!carregandoDiv) {
        // Cria o elemento se não existir
        carregandoDiv = document.createElement("div");
        carregandoDiv.id = "carregando";
        // Configura a estilização
        carregandoDiv.style.position = "fixed";
        carregandoDiv.style.top = "10px";
        carregandoDiv.style.right = "10px";
        // mudando pra amarelo
        carregandoDiv.style.backgroundColor = "#FF9800";
        carregandoDiv.style.color = "white";
        carregandoDiv.style.padding = "10px 15px";
        carregandoDiv.style.borderRadius = "5px";
        carregandoDiv.style.boxShadow = "0 2px 4px rgba(0,0,0,0.2)";
        carregandoDiv.style.zIndex = "1000";
        carregandoDiv.style.display = "none";
        document.body.appendChild(carregandoDiv);
    }
    carregandoDiv.textContent = "Carregando...";
    carregandoDiv.style.display = display;
}

// Aguarda o carregamento completo do DOM para adicionar os eventos
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-upload");
    const uploadForm = document.getElementById("upload-form");

    // Exibe uma mensagem assim que o usuário seleciona um arquivo
    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            showFileSelectedMessage(fileInput.files[0].name);
        }
    });

    // Ao submeter o formulário, envia o arquivo para o backend via fetch
    uploadForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário

        // Verifica se há um arquivo selecionado
        if (fileInput.files.length === 0) {
            alert("Por favor, selecione um arquivo.");
            return;
        }

        // Cria um objeto FormData e adiciona o arquivo
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        showCarregando("block"); // Exibe a mensagem de carregando

        // Envia a requisição POST para o backend
        fetch("http://localhost:8000/upload-pdf/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao enviar o arquivo.");
            }
            // Converte a resposta para Blob (supondo que seja o arquivo Excel)
            return response.blob();
        })
        .then(blob => {
            // Cria uma URL temporária para o Blob recebido
            const url = window.URL.createObjectURL(blob);
            // Cria um elemento <a> para simular o download
            const a = document.createElement("a");
            a.href = url;
            a.download = "resultado.xlsx"; // Define o nome para o arquivo baixado
            document.body.appendChild(a);
            a.click(); // Dispara o download
            a.remove();
            window.URL.revokeObjectURL(url); // Libera recursos

            // Exibe a mensagem de sucesso
            showCarregando("none"); // Esconde a mensagem de carregando
            showUploadSuccessMessage("Upload realizado com sucesso e arquivo baixado!");
        })
        .catch(error => {
            console.error("Erro no upload:", error);
            alert("Ocorreu um erro ao enviar o arquivo.");
            showCarregando("none"); // Esconde a mensagem de carregando
        });
    });
});
