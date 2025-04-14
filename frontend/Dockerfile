# Usa imagem oficial do nginx
FROM nginx:alpine

# Remove o conteúdo padrão do nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia seus arquivos do frontend para o nginx
COPY . /usr/share/nginx/html

# Expondo porta 80
EXPOSE 80

# O Nginx já vai iniciar automático com o ENTRYPOINT padrão
