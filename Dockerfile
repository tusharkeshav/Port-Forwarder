FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
#RUN mkdir -p "/root/.config/ngrok/"
RUN mkdir -p "/root/.ngrok2/"
ARG authtoken
#RUN echo "version: 2 \nauthtoken: $authtoken \nconsole_ui: false" >> /root/.config/ngrok/ngrok.yml
RUN echo "version: 2 \nauthtoken: $authtoken \nconsole_ui: false" >> /root/.ngrok2/ngrok.yml
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 4039-4050
CMD ["python3", "main.py"]
