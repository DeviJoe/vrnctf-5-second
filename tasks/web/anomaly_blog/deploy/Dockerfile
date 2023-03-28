FROM python:3.7-slim
RUN pip install flask
WORKDIR /ctf
COPY . .
RUN useradd -M ctf
RUN chown -R root:root /ctf
RUN chmod -R 700 /ctf
RUN pip install -r requirements.txt
CMD ["python", "server.py"]