document.addEventListener("DOMContentLoaded", function () {
    const languageButton = document.getElementById("language-button");
    const flagIcon = languageButton.querySelector("img");
    const title = document.getElementById("title");
    const uploadText = document.getElementById("upload-text");
    const customFileUpload = document.getElementById("custom-file-upload");
    const uploadButton = document.getElementById("upload-button");

    languageButton.addEventListener("click", () => {
        const isEnglish = flagIcon.getAttribute("src").includes("us_flag");

        if (isEnglish) {
            // Mudar para português
            flagIcon.setAttribute("src", "/static/img/bandeira_brasil.jpg");
            flagIcon.setAttribute("alt", "Português");
            languageButton.innerHTML = '<img src="/static/img/bandeira_brasil.jpg" alt="Português" class="flag-icon"> PT';
            title.textContent = "Pesquisar IP";
            uploadText.textContent = "Faça upload do arquivo .pdf ou da planilha";
            customFileUpload.textContent = "Escolher Arquivo";
            uploadButton.textContent = "Upload";
        } else {
            // Mudar para inglês
            flagIcon.setAttribute("src", "/static/img/us_flag.png");
            flagIcon.setAttribute("alt", "English");
            languageButton.innerHTML = '<img src="/static/img/us_flag.png" alt="English" class="flag-icon"> EN';
            title.textContent = "Search IP";
            uploadText.textContent = "Upload the .pdf file or spreadsheet";
            customFileUpload.textContent = "Choose File";
            uploadButton.textContent = "Upload";
        }
    });

    // Limitar o upload de PDFs a 15 páginas
    document.getElementById("file-upload").addEventListener("change", async (event) => {
        const file = event.target.files[0];

        if (file && file.type === "application/pdf") {
            const loadingTask = pdfjsLib.getDocument(URL.createObjectURL(file));
            const pdf = await loadingTask.promise;

            if (pdf.numPages > 15) {
                alert("O arquivo PDF não pode ter mais de 15 páginas.");
                event.target.value = ""; // Limpa o campo
            }
        }
    });
});
