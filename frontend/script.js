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