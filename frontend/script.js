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

// Limitar o upload de PDFs a 15 páginas
document.getElementById("file-upload").addEventListener("change", async (event) => {
    const file = event.target.files[0];

    if (file && file.type === "application/pdf") {
        const pdfjsLib = await import("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js");
        const pdf = await pdfjsLib.getDocument(URL.createObjectURL(file)).promise;

        if (pdf.numPages > 15) {
            alert("O arquivo PDF não pode ter mais de 15 páginas.");
            event.target.value = ""; // Limpa o campo de upload
        }
    }
});

// Função para exibir uma mensagem de sucesso no canto superior direito
function showUploadSuccessMessage(message) {
    let successDiv = document.getElementById("upload-success");
    if (!successDiv) {
        successDiv = document.createElement("div");
        successDiv.id = "upload-success";
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

// Aguarda o carregamento do DOM
document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");

    // Intercepta o envio do formulário
    uploadForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Impede o comportamento padrão do formulário

        // Recupera o arquivo selecionado
        const fileInput = document.getElementById("file-upload");
        if (fileInput.files.length === 0) {
            alert("Por favor, selecione um arquivo.");
            return;
        }

        // Cria um objeto FormData e adiciona o arquivo
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // Envia a requisição POST para o backend
        fetch("http://localhost:8000/upload-pdf/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao enviar o arquivo.");
            }
            // Obtém a resposta como Blob (arquivo Excel)
            return response.blob();
        })
        .then(blob => {
            // Cria uma URL para o Blob recebido
            const url = window.URL.createObjectURL(blob);
            // Cria um elemento <a> para acionar o download
            const a = document.createElement("a");
            a.href = url;
            // Define o nome do arquivo para download (pode ser personalizado)
            a.download = "resultado.xlsx";
            document.body.appendChild(a);
            a.click(); // Simula o clique para iniciar o download
            a.remove();
            window.URL.revokeObjectURL(url); // Libera a URL criada

            // Exibe a mensagem de upload concluído com sucesso
            showUploadSuccessMessage("Upload realizado com sucesso e arquivo baixado!");
        })
        .catch(error => {
            console.error("Erro no upload:", error);
            alert("Ocorreu um erro ao enviar o arquivo.");
        });
    });
});