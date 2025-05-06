FROM python:3.11-slim
# Установим рабочую директорию
WORKDIR /app
# Копируем файл зависимостей
COPY . .
# Устанавливаем зависимости из файла
RUN pip install --no-cache-dir -r requirements.txt
# Запускаем инициализационный скрипт после установки зависимостей
RUN python create_admin.py
# Открываем порт для FastAPI
EXPOSE 8000
# Команда для запуска FastAPI приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]