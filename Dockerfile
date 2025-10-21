FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ligne ajoutée pour vérifier les fichiers dans /app au moment du build :
RUN ls -l /app

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
