FROM python:3.9

RUN apt-get update && apt-get install -y curl && apt-get install -y cowsay \
 && rm -rf /var/lib/apt/lists/*

RUN chmod o-x $(which ps)

ENV FLAG="vrnctf{000h_3nv_m4573r_53mp44441}"
RUN useradd -u 999 -G sudo -ms /bin/bash webadmin

USER webadmin:webadmin

COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
RUN chown webadmin /usr/src/app -R

COPY . .

ENTRYPOINT python app.py && source FLAG_2="vrnctf{pr0c_r34d3r_ch4mp10n}"