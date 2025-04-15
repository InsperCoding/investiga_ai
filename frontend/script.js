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

// Função para exibir uma mensagem de sucesso
function showUploadSuccessMessage(message) {
    // Verifica se já existe um elemento para a mensagem
    let successDiv = document.getElementById("upload-success");
    if (!successDiv) {
        // Cria o elemento se não existir
        successDiv = document.createElement("div");
        successDiv.id = "upload-success";
        // Estilização básica para exibir a mensagem no canto superior direito
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
    // Define o conteúdo da mensagem e exibe o elemento
    successDiv.textContent = message;
    successDiv.style.display = "block";
    
    // Após 3 segundos, oculta a mensagem
    setTimeout(() => {
        successDiv.style.display = "none";
    }, 3000);
}

// Aguarda o carregamento completo do DOM
document.addEventListener("DOMContentLoaded", () => {
    // Seleciona o formulário pelo id
    const uploadForm = document.getElementById("upload-form");

    // Adiciona o listener para o evento 'submit'
    uploadForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário

        // Seleciona o input do tipo file
        const fileInput = document.getElementById("file-upload");

        // Verifica se há um arquivo selecionado
        if (fileInput.files.length === 0) {
            alert("Por favor, selecione um arquivo.");
            return;
        }

        // Cria um objeto FormData para enviar o arquivo
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // Envia a requisição POST para o backend utilizando fetch
        fetch("http://localhost:8000/upload-pdf/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao enviar o arquivo.");
            }
            return response.json(); // Se o backend retornar JSON
        })
        .then(data => {
            console.log("Upload bem-sucedido:", data);
            // Aqui você pode atualizar a UI conforme a resposta do backend
        })
        .catch(error => {
            console.error("Erro no upload:", error);
            alert("Ocorreu um erro ao enviar o arquivo.");
        });
    });
});