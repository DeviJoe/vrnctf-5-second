FROM python:3.7-slim
RUN apt-get update
RUN apt-get install unzip
WORKDIR /ctf
COPY . .
RUN useradd -M ctf
RUN chown root:root /ctf
RUN chmod 700 /ctf
RUN pip install gdown
RUN gdown --id 1_iioxRNwueao2Nfl67XScbw994VOTj3X
RUN unzip -o images.zip
RUN rm images.zip
RUN pip install -r requirements.txt
CMD ["python", "server.py"]