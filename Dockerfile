FROM python:3.11-slim

LABEL maintainer="ndinhbaoquang@gmail.com"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# install dependencies for browsers
RUN playwright install
RUN playwright install-deps

ENV PATH "$PATH:/app/scripts"

WORKDIR /app

CMD ["streamlit", "run", "streamlit_app.py", "--server.enableCORS=false"]
