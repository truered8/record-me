# 1
FROM python:3.7

# 2
WORKDIR /app
COPY ./* /app

# 3
RUN pip install -r requirements.txt

# 4
ENV PORT 8080
RUN curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/14a38e6a-82e2-4308-86c5-8124ef6268e9/cert

# 5
CMD exec gunicorn --bind :$PORT 'flask_handler:run_app()'