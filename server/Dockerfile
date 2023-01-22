# 1
FROM python:3.7

# 2
WORKDIR /app
COPY ./* /app

# 3
RUN pip install -r requirements.txt

# 4
ENV PORT 8080
RUN curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/bff5a441-cb47-4d74-9fc0-b20583a074ce/cert

# 5
CMD exec gunicorn --bind :$PORT 'flask_handler:load_app()'