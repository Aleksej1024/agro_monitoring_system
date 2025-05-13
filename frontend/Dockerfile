FROM nginx
# Установим рабочую директорию
WORKDIR /app
COPY . .
# Копируем файл конфигурации
RUN cp /app/nginx.conf /etc/nginx/sites-enabled/default
# Открываем порт для nginx
EXPOSE 80
# Команда для запуска FastAPI приложения
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]