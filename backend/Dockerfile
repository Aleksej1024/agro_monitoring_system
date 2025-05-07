FROM ultralytics/ultralytics
# Установим рабочую директорию
WORKDIR /app
# Копируем файл зависимостей
COPY . .
# Устанавливаем зависимости из файла
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-multipart
# Открываем порт для FastAPI
EXPOSE 8000
# Команда для запуска FastAPI приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Запускаем инициализационный скрипт после установки зависимостей
#RUN python create_admin.py