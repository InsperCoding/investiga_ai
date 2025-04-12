import React, { useState } from 'react';
import './style.css';

function App() {
  const [language, setLanguage] = useState('pt');
  const [file, setFile] = useState(null);

  const handleLanguageSwitch = () => {
    setLanguage((prev) => (prev === 'pt' ? 'en' : 'pt'));
  };

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      const pdfjsLib = await import('pdfjs-dist');
      const pdf = await pdfjsLib.getDocument(URL.createObjectURL(selectedFile)).promise;
      if (pdf.numPages > 15) {
        alert('O arquivo PDF não pode ter mais de 15 páginas.');
        e.target.value = '';
        setFile(null);
        return;
      }
    }
    setFile(selectedFile);
  };

  const texts = {
    pt: {
      title: 'Procurar IP',
      uploadText: 'Faça upload do arquivo .pdf ou da planilha',
      chooseFile: 'Escolher Arquivo',
      upload: 'Upload',
      flag: 'img/us_flag.png',
      alt: 'English',
      langLabel: 'EN',
    },
    en: {
      title: 'Search IP',
      uploadText: 'Upload the .pdf file or spreadsheet',
      chooseFile: 'Choose File',
      upload: 'Upload',
      flag: 'img/bandeira_brasil.jpg',
      alt: 'Português',
      langLabel: 'PT',
    },
  };

  const t = texts[language];

  return (
    <div className="app">
      <div className="language-switcher">
        <button id="language-button" onClick={handleLanguageSwitch}>
          <img src={t.flag} alt={t.alt} className="flag-icon" /> {t.langLabel}
        </button>
      </div>
      <div className="container">
        <h1 id="title">{t.title}</h1>
        <form method="POST" action="/upload/" encType="multipart/form-data" className="upload-container">
          <span id="upload-text">{t.uploadText}</span>
          <label htmlFor="file-upload" id="custom-file-upload">{t.chooseFile}</label>
          <input
            type="file"
            id="file-upload"
            name="file"
            accept=".pdf,.xls,.xlsx,.csv"
            onChange={handleFileChange}
            required
          />
          <button type="submit" id="upload-button">{t.upload}</button>
        </form>
      </div>
      <footer className="site-footer">
        <img src="img/insper_coding_logo.jpg" alt="Footer Logo" className="footer-logo" />
        <p>Made by <strong>InsperCode</strong></p>
        <p>Wesley Alves Cavalcante</p>
        <p>Gabriel Pradyumna Alencar Costa</p>
        <p>Mateus Moreira Pereira</p>
      </footer>
    </div>
  );
}

export default App;
