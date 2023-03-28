FROM python:3.7-slim
WORKDIR /ctf
COPY . .
RUN useradd -M ctf
RUN chown root:root /ctf
RUN chmod 700 /ctf
RUN pip install -r requirements.txt
CMD ["python", "server.py"]