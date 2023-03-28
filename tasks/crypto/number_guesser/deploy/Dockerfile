FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
  xinetd build-essential libssl-dev libffi-dev python-dev libgmp-dev libmpfr-dev libmpc-dev \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY . /ctf/

RUN chown -R root:ctf /ctf && \
  chmod -R 750 /ctf

RUN pip3 install pycryptodome

ENTRYPOINT []
CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 5678

