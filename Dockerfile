# Usar a imagem oficial do Python como base
FROM python:3.11-slim

# Configurar diretório de trabalho
WORKDIR /AGENDA_PROJECT

# Copiar o arquivo de dependências e instalá-las
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do projeto para o contêiner
COPY . /AGENDA_PROJECT/

# Configurar as variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV=production 

# Rodar collectstatic apenas se o ambiente for produção
RUN if [ "$DJANGO_ENV" = "production" ]; then python manage.py collectstatic --noinput; fi

# Expor a porta padrão do Django
EXPOSE 8000

# Usar Gunicorn para servir a aplicação
CMD ["uvicorn", "project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]