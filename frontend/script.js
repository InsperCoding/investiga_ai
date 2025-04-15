let currentLanguage = "pt"; // Define o idioma padrão como português

document.getElementById("language-button").addEventListener("click", () => {
    const languageButton = document.getElementById("language-button");
    const flagIcon = languageButton.querySelector("img");
    const title = document.getElementById("title");
    const uploadText = document.getElementById("upload-text");
    const customFileUpload = document.getElementById("custom-file-upload");
    const uploadButton = document.getElementById("upload-button");

    // Verifica o idioma atual com base no atributo "alt" da bandeira
    if (flagIcon.getAttribute("alt") === "Português") {
        // Mudar para português
        flagIcon.setAttribute("src", "img/bandeira_brasil.jpg");
        flagIcon.setAttribute("alt", "Português");
        languageButton.textContent = " PT";
        languageButton.prepend(flagIcon);
        title.textContent = "Procurar IP";
        uploadText.textContent = "Faça upload do arquivo .pdf ou da planilha";
        customFileUpload.textContent = "Escolher Arquivo";
        uploadButton.textContent = "Upload";
        currentLanguage = "pt";
    } else {
        flagIcon.setAttribute("src", "img/us_flag.png");
        flagIcon.setAttribute("alt", "English");
        languageButton.textContent = " EN";
        languageButton.prepend(flagIcon);
        title.textContent = "Search IP";
        uploadText.textContent = "Upload the .pdf file or spreadsheet";
        customFileUpload.textContent = "Choose File";
        uploadButton.textContent = "Upload";
        currentLanguage = "en";
    }
});

document.getElementById("file-upload").addEventListener("change", async (event) => {
    const file = event.target.files[0];

    if (file && file.type === "application/pdf") {
        const pdfjsModule = await import("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js");
        const pdfjsLib = pdfjsModule.default;
        const loadingTask = pdfjsLib.getDocument(URL.createObjectURL(file));
        const pdf = await loadingTask.promise;

        if (pdf.numPages > 15) {
            const message = currentLanguage === "pt" 
                ? "O arquivo PDF não pode ter mais de 15 páginas." 
                : "The PDF file cannot have more than 15 pages.";
            alert(message);
            event.target.value = "";
        }
    }
});

function showFileSelectedMessage(fileName) {
    let fileMessageDiv = document.getElementById("file-selected-message");
    if (!fileMessageDiv) {
        fileMessageDiv = document.createElement("div");
        fileMessageDiv.id = "file-selected-message";
        fileMessageDiv.style.marginTop = "10px";
        fileMessageDiv.style.fontStyle = "italic";
        fileMessageDiv.style.color = "#ffffff";
        const container = document.querySelector(".container") || document.body;
        container.appendChild(fileMessageDiv);
    }

    const text = currentLanguage === "pt" 
        ? "Arquivo selecionado: " + fileName 
        : "Selected file: " + fileName;
    fileMessageDiv.textContent = text;
}

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

function showCarregando(display) {
    let carregandoDiv = document.getElementById("carregando");
    if (!carregandoDiv) {
        carregandoDiv = document.createElement("div");
        carregandoDiv.id = "carregando";
        carregandoDiv.style.position = "fixed";
        carregandoDiv.style.top = "10px";
        carregandoDiv.style.right = "10px";
        carregandoDiv.style.backgroundColor = "#FF9800";
        carregandoDiv.style.color = "white";
        carregandoDiv.style.padding = "10px 15px";
        carregandoDiv.style.borderRadius = "5px";
        carregandoDiv.style.boxShadow = "0 2px 4px rgba(0,0,0,0.2)";
        carregandoDiv.style.zIndex = "1000";
        carregandoDiv.style.display = "none";
        document.body.appendChild(carregandoDiv);
    }

    carregandoDiv.textContent = currentLanguage === "pt" 
        ? "Carregando..." 
        : "Loading...";
    carregandoDiv.style.display = display;
}

document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-upload");
    const uploadForm = document.getElementById("upload-form");

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            showFileSelectedMessage(fileInput.files[0].name);
        }
    });

    uploadForm.addEventListener("submit", (event) => {
        event.preventDefault();

        if (fileInput.files.length === 0) {
            const msg = currentLanguage === "pt" 
                ? "Por favor, selecione um arquivo." 
                : "Please select a file.";
            alert(msg);
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        showCarregando("block");

        // Envia a requisição POST para o backend
        fetch("http://34.44.247.78:8000/upload-pdf/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Upload failed.");
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "resultado.xlsx";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);

            showCarregando("none");
            const successMessage = currentLanguage === "pt" 
                ? "Upload realizado com sucesso e arquivo baixado!" 
                : "Upload completed successfully and file downloaded!";
            showUploadSuccessMessage(successMessage);
        })
        .catch(error => {
            console.error("Erro no upload:", error);
            const errMsg = currentLanguage === "pt" 
                ? "Ocorreu um erro ao enviar o arquivo." 
                : "An error occurred while uploading the file.";
            alert(errMsg);
            showCarregando("none");
        });
    });
});
